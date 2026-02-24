import json


class DecisionEngine:
    def __init__(self, dataset_path="phones.json"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.phones = json.load(f)

    def normalize_weights(self, weights):
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()} if total else weights

    def calculate_effective_performance(self, phone):
        return 0.7 * phone["performance_score"] + 0.3 * phone["processor_score"]

    def recommend(self, budget, weights, os_preference=None):

        filtered = [p for p in self.phones if p["price"] <= budget]

        if os_preference and os_preference != "Any":
            filtered = [
                p for p in filtered
                if p["os_type"].lower() == os_preference.lower()
            ]

        amplified = {k: v ** 2 for k, v in weights.items()}
        normalized = self.normalize_weights(amplified)

        scored = []

        for phone in filtered:
            effective_perf = self.calculate_effective_performance(phone)

            score = (
                normalized["camera"] * phone["camera_score"] +
                normalized["battery"] * phone["battery_score"] +
                normalized["performance"] * effective_perf +
                normalized["display"] * phone["display_score"] +
                normalized["software"] * phone["software_score"] +
                normalized["value"] * phone["value_score"]
            )

            phone_copy = phone.copy()
            phone_copy["final_score"] = round(score, 2)
            scored.append(phone_copy)

        return sorted(scored, key=lambda x: x["final_score"], reverse=True)[:3]