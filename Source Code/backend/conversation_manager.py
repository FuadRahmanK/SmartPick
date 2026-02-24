from decision_engine import DecisionEngine
from input_parser import InputParser
from ai_layer import generate_ai_response, generate_recommendation_text


class ConversationManager:
    def __init__(self, dataset_path="phones.json"):
        self.engine = DecisionEngine(dataset_path)
        self.parser = InputParser()

        self.state = {
            "greeted": False,
            "budget": None,
            "os_preference": None,
            "brand_preference": None,
            "weights": {
                "camera": 3,
                "battery": 3,
                "performance": 3,
                "display": 3,
                "software": 3,
                "value": 3
            },
            "clarified_features": {},
            "awaiting_feature": None,
            "recommendation_shown": False,
            "min_features_required": 3
        }

    # ----------------------------------------------------
    # Main Entry
    # ----------------------------------------------------
    def handle_message(self, user_message):
        self.update_state(user_message)
        return self.decide_next_step()

    # ----------------------------------------------------
    # Update State
    # ----------------------------------------------------
    def update_state(self, user_message):
        parsed = self.parser.parse(user_message)

        if parsed["budget"]:
            self.state["budget"] = parsed["budget"]

        if parsed["os_preference"]:
            self.state["os_preference"] = parsed["os_preference"]

        if parsed["brand_preference"]:
            self.state["brand_preference"] = parsed["brand_preference"]

        # Handle behavioral clarification
        if self.state["awaiting_feature"]:
            inferred = self.infer_rating_from_behavior(user_message)

            if inferred:
                feature = self.state["awaiting_feature"]

                # Feature interaction
                if feature == "performance" and inferred >= 4:
                    self.state["weights"]["battery"] += 1

                if feature == "display" and inferred >= 4:
                    self.state["weights"]["battery"] += 1

                self.state["weights"][feature] = inferred
                self.state["clarified_features"][feature] = inferred
                self.state["awaiting_feature"] = None

            else:
                numeric = self.parser.extract_importance_rating(user_message)
                if numeric:
                    feature = self.state["awaiting_feature"]
                    self.state["weights"][feature] = numeric
                    self.state["clarified_features"][feature] = numeric
                    self.state["awaiting_feature"] = None

        # If already recommended and user changes something → reset
        if self.state["recommendation_shown"]:
            self.state["recommendation_shown"] = False

    # ----------------------------------------------------
    # Behavioral Inference
    # ----------------------------------------------------
    def infer_rating_from_behavior(self, text):
        text = text.lower()

        high = ["daily", "regularly", "very often", "a lot", "heavy", "everyday", "frequently", "yes", "yeah", "yup"]
        medium = ["sometimes", "occasionally", "moderate"]
        low = ["rarely", "not much", "almost never", "no"]

        if any(w in text for w in high):
            return 5

        if any(w in text for w in medium):
            return 3

        if any(w in text for w in low):
            return 1

        return None

    # ----------------------------------------------------
    # Ask Feature
    # ----------------------------------------------------
    def ask_feature(self, feature_key):

        behavioral_questions = {
            "performance": "Do you play heavy games regularly, occasionally, or rarely?",
            "battery": "Do you use your phone heavily throughout the day?",
            "camera": "Do you take a lot of photos and videos?",
            "display": "Do you watch movies or YouTube frequently on your phone?",
            "software": "Do you care about clean software and long-term updates?"
        }

        self.state["awaiting_feature"] = feature_key
        base_question = behavioral_questions.get(feature_key)

        question = generate_ai_response(
            f"""
Rewrite the following question naturally and professionally.
Do NOT add greetings.
Do NOT repeat.
Keep it concise.

Question:
{base_question}
"""
        )

        return {
            "type": "question",
            "message": question
        }

    # ----------------------------------------------------
    # Generate Summary
    # ----------------------------------------------------
    def generate_summary(self):
        summary = f"""
Budget: ₹{self.state['budget']}
OS Preference: {self.state['os_preference']}
"""

        for feature, rating in self.state["clarified_features"].items():
            summary += f"{feature.capitalize()}: {rating}/5\n"

        if self.state["brand_preference"]:
            summary += f"Brand Preference: {self.state['brand_preference']}\n"

        return generate_ai_response(
            f"""
Summarize the following clearly and professionally.
Do NOT add greetings.

{summary}
"""
        )

    # ----------------------------------------------------
    # Decision Flow
    # ----------------------------------------------------
    def decide_next_step(self):

        if not self.state["budget"]:
            return {
                "type": "question",
                "message": "What is your budget range?"
            }

        if not self.state["os_preference"]:
            return {
                "type": "question",
                "message": "Do you prefer Android or iOS?"
            }

        # OS-aware feature order
        if self.state["os_preference"] == "iOS":
            feature_order = ["camera", "performance", "battery", "display"]
        else:
            feature_order = ["performance", "camera", "battery", "display", "software"]

        for feature in feature_order:
            if feature not in self.state["clarified_features"]:
                return self.ask_feature(feature)

        # Recommendation
        recommendations = self.engine.recommend(
            budget=self.state["budget"],
            weights=self.state["weights"],
            os_preference=self.state["os_preference"]
        )

        explanation = generate_recommendation_text(
            recommendations,
            self.state
        )

        self.state["recommendation_shown"] = True

        return {
            "type": "recommendation",
            "summary": self.generate_summary(),
            "data": recommendations,
            "ai_text": explanation,
            "follow_up": "Would you like to adjust anything? You can modify budget, OS, or preferences."
        }