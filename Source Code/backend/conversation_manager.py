from decision_engine import DecisionEngine
from input_parser import InputParser
from ai_layer import (
    normalize_user_input,
    extract_structured_info_with_ai,
    infer_rating_with_ai,
    generate_recommendation_text
)


class ConversationManager:
    def __init__(self, dataset_path="phones.json"):
        self.engine = DecisionEngine(dataset_path)
        self.parser = InputParser()

        self.state = {
            "budget": None,
            "os_preference": None,
            "weights": {
                "camera": 3,
                "battery": 3,
                "performance": 3,
                "display": 3,
                "software": 3,
                "value": 3
            },
            "clarified_features": {},
            "awaiting_field": None   # 🔥 unified state tracking
        }

    # --------------------------------------------------
    # ENTRY
    # --------------------------------------------------
    def handle_message(self, user_message):

        cleaned = normalize_user_input(user_message)

        # 1️⃣ If waiting for specific field → process it
        if self.state["awaiting_field"]:
            self.process_waiting_field(cleaned)
            return self.decide_next_step()

        # 2️⃣ Otherwise extract structured info
        self.extract_initial_information(cleaned)

        return self.decide_next_step()

    # --------------------------------------------------
    # Process Waiting Field
    # --------------------------------------------------
    def process_waiting_field(self, text):

        field = self.state["awaiting_field"]

        if field == "os_preference":
            text_lower = text.lower()

            if "android" in text_lower:
                self.state["os_preference"] = "Android"
            elif "ios" in text_lower or "iphone" in text_lower:
                self.state["os_preference"] = "iOS"
            elif "any" in text_lower or "no preference" in text_lower:
                self.state["os_preference"] = "Any"

            self.state["awaiting_field"] = None
            return

        # Otherwise it is a feature
        feature = field

        ai_rating = infer_rating_with_ai(text, feature)
        rating = ai_rating if ai_rating else self.fallback_rating(text)

        if rating is None:
            rating = 3

        self.state["weights"][feature] = rating
        self.state["clarified_features"][feature] = rating

        self.state["awaiting_field"] = None

    # --------------------------------------------------
    # Extract Initial Structured Info
    # --------------------------------------------------
    def extract_initial_information(self, text):

        ai_data = extract_structured_info_with_ai(text)

        if ai_data:
            if ai_data.get("budget"):
                self.state["budget"] = ai_data["budget"]

            if ai_data.get("os_preference"):
                self.state["os_preference"] = ai_data["os_preference"]

            if ai_data.get("feature_priority"):
                feature = ai_data["feature_priority"]
                self.state["weights"][feature] = 5
                self.state["clarified_features"][feature] = 5

        parsed = self.parser.parse(text)

        if not self.state["budget"] and parsed["budget"]:
            self.state["budget"] = parsed["budget"]

        if self.state["os_preference"] is None and parsed["os_preference"]:
            self.state["os_preference"] = parsed["os_preference"]

        if parsed["feature_detected"]:
            feature = parsed["feature_detected"]
            self.state["weights"][feature] = 5
            self.state["clarified_features"][feature] = 5

    # --------------------------------------------------
    # Fallback Rating
    # --------------------------------------------------
    def fallback_rating(self, text):
        text = text.lower()

        if "very important" in text:
            return 5
        if "important" in text:
            return 4
        if any(w in text for w in ["moderate", "sometimes", "occasionally"]):
            return 3
        if "rarely" in text:
            return 2
        if any(w in text for w in ["no", "not important"]):
            return 1

        return None

    # --------------------------------------------------
    # Decision Flow
    # --------------------------------------------------
    def decide_next_step(self):

        if not self.state["budget"]:
            self.state["awaiting_field"] = "budget"
            return {"type": "question", "message": "What is your budget range?"}

        if self.state["os_preference"] is None:
            self.state["awaiting_field"] = "os_preference"
            return {"type": "question", "message": "Do you prefer Android or iOS?"}

        feature_order = ["performance", "camera", "battery", "display", "software"]

        for feature in feature_order:
            if feature not in self.state["clarified_features"]:
                self.state["awaiting_field"] = feature
                return {
                    "type": "question",
                    "message": f"How important is {feature} for you?"
                }

        recommendations = self.engine.recommend(
            budget=self.state["budget"],
            weights=self.state["weights"],
            os_preference=self.state["os_preference"]
        )

        return {
            "type": "recommendation",
            "summary": self.generate_summary(),
            "data": recommendations,
            "ai_text": generate_recommendation_text(recommendations, self.state),
            "follow_up": "Would you like to adjust anything?"
        }

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    def generate_summary(self):

        lines = [
            f"Budget: ₹{self.state['budget']}",
            f"OS Preference: {self.state['os_preference']}"
        ]

        for f, r in self.state["clarified_features"].items():
            lines.append(f"{f.capitalize()}: {r}/5")

        return "Here is a summary of your preferences:\n\n" + "\n".join(lines)