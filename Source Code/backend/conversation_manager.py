from decision_engine import DecisionEngine
from input_parser import InputParser


class ConversationManager:
    def __init__(self, dataset_path="phones.json"):
        self.engine = DecisionEngine(dataset_path)
        self.parser = InputParser()

        # Default session state
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
            "confidence": 0,
            "priority_detected": False
        }

    # ----------------------------------------------------
    # 1️⃣ Update State From User Input
    # ----------------------------------------------------
    def update_state(self, user_message):
        parsed = self.parser.parse(user_message, self.state["weights"])

        # Update budget if detected
        if parsed["budget"]:
            self.state["budget"] = parsed["budget"]

        # Update OS preference if detected
        if parsed["os_preference"]:
            self.state["os_preference"] = parsed["os_preference"]

        # Update weights
        self.state["weights"] = parsed["weights"]

        # Track whether priorities were detected
        if parsed["priority_detected"]:
            self.state["priority_detected"] = True

        # Recalculate confidence
        self.calculate_confidence()

    # ----------------------------------------------------
    # 2️⃣ Confidence Calculation
    # ----------------------------------------------------
    def calculate_confidence(self):
        confidence = 0

        # Budget known
        if self.state["budget"]:
            confidence += 50

        # At least one priority keyword detected
        if self.state["priority_detected"]:
            confidence += 30

        # OS preference specified
        if self.state["os_preference"]:
            confidence += 20

        self.state["confidence"] = confidence

    # ----------------------------------------------------
    # 3️⃣ Decide Next Action
    # ----------------------------------------------------
    def decide_next_step(self):
        # If budget missing → ask for it
        if not self.state["budget"]:
            return {
                "type": "question",
                "message": "What is your maximum budget?"
            }

        # If priorities not clear yet
        if not self.state["priority_detected"]:
            return {
                "type": "question",
                "message": "What matters most to you — gaming performance, camera, battery life, display quality, or software experience?"
            }

        # If confidence high enough → recommend
        if self.state["confidence"] >= 80:
            recommendations = self.engine.recommend(
                budget=self.state["budget"],
                weights=self.state["weights"],
                os_preference=self.state["os_preference"]
            )

            if not recommendations:
                return {
                    "type": "question",
                    "message": "I couldn't find phones matching your criteria. Would you like to adjust your budget?"
                }

            return {
                "type": "recommendation",
                "data": recommendations
            }

        # Fallback clarification
        return {
            "type": "question",
            "message": "Could you tell me more about what features matter to you?"
        }

    # ----------------------------------------------------
    # 4️⃣ Main Entry Point
    # ----------------------------------------------------
    def handle_message(self, user_message):
        self.update_state(user_message)
        return self.decide_next_step()