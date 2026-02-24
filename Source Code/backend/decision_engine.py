import json


class DecisionEngine:
    def __init__(self, dataset_path="phones.json"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.phones = json.load(f)

    # ----------------------------------------------------
    # Normalize Weights
    # ----------------------------------------------------
    def normalize_weights(self, weights):
        total = sum(weights.values())
        if total == 0:
            return weights
        return {k: v / total for k, v in weights.items()}

    # ----------------------------------------------------
    # Effective Performance Score
    # ----------------------------------------------------
    def calculate_effective_performance(self, phone):
        return (
            0.7 * phone["performance_score"] +
            0.3 * phone["processor_score"]
        )

    # ----------------------------------------------------
    # Recommendation Engine
    # ----------------------------------------------------
    def recommend(self, budget, weights, os_preference=None):

        # Budget filter
        filtered = [
            phone for phone in self.phones
            if phone["price"] <= budget
        ]

        # OS filter
        if os_preference:
            filtered = [
                phone for phone in filtered
                if phone["os_type"].lower() == os_preference.lower()
            ]

        if not filtered:
            return []

        normalized_weights = self.normalize_weights(weights)
        scored_phones = []

        for phone in filtered:
            effective_perf = self.calculate_effective_performance(phone)

            final_score = (
                normalized_weights["camera"] * phone["camera_score"] +
                normalized_weights["battery"] * phone["battery_score"] +
                normalized_weights["performance"] * effective_perf +
                normalized_weights["display"] * phone["display_score"] +
                normalized_weights["software"] * phone["software_score"] +
                normalized_weights["value"] * phone["value_score"]
            )

            phone_copy = phone.copy()
            phone_copy["final_score"] = round(final_score, 2)
            scored_phones.append(phone_copy)

        # Sort descending
        ranked = sorted(
            scored_phones,
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranked[:3]