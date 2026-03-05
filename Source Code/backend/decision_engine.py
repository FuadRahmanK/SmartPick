import json
import statistics


class DecisionEngine:

    def __init__(self, dataset_path="phones.json"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.phones = json.load(f)

    def normalize_weights(self, weights):
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()} if total else weights

    def effective_performance(self, phone):
        return 0.7 * phone["performance_score"] + 0.3 * phone["processor_score"]

    def get_filtered_phones(self, budget, os_preference=None):
        filtered = [p for p in self.phones if p["price"] <= budget]

        if os_preference and os_preference != "Any":
            filtered = [
                p for p in filtered
                if p["os_type"].lower() == os_preference.lower()
            ]

        return filtered

    def feature_variance(self, phones):
        if not phones:
            return {}

        features = ["camera", "battery", "performance", "display", "software"]
        variance_map = {}

        for f in features:
            values = [p[f"{f}_score"] for p in phones]
            variance_map[f] = statistics.variance(values) if len(values) > 1 else 0

        return variance_map

    def recommend(self, budget, weights, os_preference=None):

        filtered = self.get_filtered_phones(budget, os_preference)

        if not filtered:
            return []

        amplified = {
            k: (1 if v == 1 else v ** 2)
            for k, v in weights.items()
        }

        normalized = self.normalize_weights(amplified)

        scored = []

        for phone in filtered:
            score = (
                normalized["camera"] * phone["camera_score"] +
                normalized["battery"] * phone["battery_score"] +
                normalized["performance"] * self.effective_performance(phone) +
                normalized["display"] * phone["display_score"] +
                normalized["software"] * phone["software_score"] +
                normalized["value"] * phone["value_score"]
            )

            p = phone.copy()
            p["final_score"] = round(score, 3)
            scored.append(p)

        return sorted(
            scored,
            key=lambda x: (
                x["final_score"],
                x["value_score"],
                -x["price"],
                x["processor_score"]
            ),
            reverse=True
        )[:3]