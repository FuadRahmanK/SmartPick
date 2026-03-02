from decision_engine import DecisionEngine
from input_parser import InputParser
from ai_layer import (
    normalize_user_input,
    extract_structured_info_with_ai,
    infer_rating_with_ai
)


class ConversationManager:

    def __init__(self, dataset_path="phones.json"):

        self.engine = DecisionEngine(dataset_path)
        self.parser = InputParser()

        self.default_weight = 1

        self.state = {
            "budget": None,
            "os_preference": None,
            "weights": {
                "camera": 1,
                "battery": 1,
                "performance": 1,
                "display": 1,
                "software": 1,
                "value": 1
            },
            "clarified_features": {},
            "awaiting_field": None
        }

        self.last_update = None

    # ==============================
    # ENTRY
    # ==============================
    def handle_message(self, user_message):

        text = normalize_user_input(user_message)
        self.last_update = None

        if self.state["awaiting_field"]:
            self.process_waiting_field(text)
            return self.decide_next_step()

        parsed = self.parser.parse(text)

        # Deterministic first
        if parsed["budget"]:
            self.state["budget"] = parsed["budget"]
            self.last_update = "budget"

        if parsed["os_preference"]:
            self.state["os_preference"] = parsed["os_preference"]
            self.last_update = "os_preference"

        if parsed["feature_detected"]:
            feature = parsed["feature_detected"]
            self.state["weights"][feature] = 5
            self.state["clarified_features"][feature] = 5
            self.last_update = feature

        # AI only if rule parser failed
        if not parsed["budget"] and not parsed["os_preference"] and not parsed["feature_detected"]:
            ai_data = extract_structured_info_with_ai(text)
        else:
            ai_data = None

        if ai_data:
            if ai_data.get("os_preference"):
                self.state["os_preference"] = ai_data["os_preference"]
                self.last_update = "os_preference"

            if ai_data.get("feature_priority"):
                feature = ai_data["feature_priority"]
                self.state["weights"][feature] = 5
                self.state["clarified_features"][feature] = 5
                self.last_update = feature

        return self.decide_next_step()

    # ==============================
    # PROCESS WAITING FIELD
    # ==============================
    def process_waiting_field(self, text):

        field = self.state["awaiting_field"]

        if field == "budget":
            parsed = self.parser.parse(text)
            if parsed["budget"]:
                self.state["budget"] = parsed["budget"]
                self.last_update = "budget"
            self.state["awaiting_field"] = None
            return

        if field == "os_preference":
            parsed = self.parser.parse(text)
            if parsed["os_preference"]:
                self.state["os_preference"] = parsed["os_preference"]
                self.last_update = "os_preference"
            self.state["awaiting_field"] = None
            return

        # Feature rating
        rating = self.fallback_rating(text)

        if rating is None:
            rating = infer_rating_with_ai(text, field)

        if rating is None:
            rating = self.default_weight

        self.state["weights"][field] = rating
        self.state["clarified_features"][field] = rating
        self.last_update = field
        self.state["awaiting_field"] = None

    def fallback_rating(self, text):
        text = text.lower()

        if "very important" in text:
            return 5
        if "important" in text:
            return 4
        if "moderate" in text:
            return 3
        if "rarely" in text:
            return 2
        if "not important" in text:
            return 1

        return None

    def acknowledge_last(self):
        if not self.last_update:
            return ""

        if self.last_update == "budget":
            return "Budget noted. "

        if self.last_update == "os_preference":
            if self.state["os_preference"] == "Any":
                return "No OS restriction applied. "
            return f"{self.state['os_preference']} preference recorded. "

        return f"{self.last_update.capitalize()} priority updated. "

    # ==============================
    # SMART FLOW
    # ==============================
    def decide_next_step(self):

        ack = self.acknowledge_last()

        if not self.state["budget"]:
            self.state["awaiting_field"] = "budget"
            return {"type": "question", "message": f"{ack}What is your budget range?"}

        if self.state["os_preference"] is None:
            self.state["awaiting_field"] = "os_preference"
            return {"type": "question", "message": f"{ack}Do you prefer Android or iOS?"}

        # Dynamic feature ordering
        filtered = self.engine.get_filtered_phones(
            self.state["budget"],
            self.state["os_preference"]
        )

        variance_map = self.engine.feature_variance(filtered)

        feature_questions = {
            "performance": "How important is performance or gaming power?",
            "camera": "How important is camera quality?",
            "battery": "How important is battery life?",
            "display": "How important is display quality?",
            "software": "How important is clean software and updates?"
        }

        sorted_features = sorted(
            variance_map.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for feature, _ in sorted_features:
            if feature not in self.state["clarified_features"]:
                self.state["awaiting_field"] = feature
                return {
                    "type": "question",
                    "message": f"{ack}{feature_questions[feature]}"
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
            "follow_up": "Would you like to refine any criteria?"
        }

    def generate_summary(self):
        lines = [
            f"Budget: ₹{self.state['budget']}",
            f"OS Preference: {self.state['os_preference']}"
        ]
        for f, r in self.state["weights"].items():
            lines.append(f"{f.capitalize()}: {r}/5")

        return "Summary:\n\n" + "\n".join(lines)