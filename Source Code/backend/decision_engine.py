import json


class DecisionEngine:
    def __init__(self, dataset_path="phones.json"):
        self.phones = self.load_dataset(dataset_path)

    def load_dataset(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ----------------------------------------------------
    # 1️⃣ Filter Phones
    # ----------------------------------------------------
    def filter_phones(self, budget=None, os_preference=None):
        filtered = self.phones

        if budget is not None:
            filtered = [p for p in filtered if p["price"] <= budget]

        if os_preference:
            filtered = [p for p in filtered if p["os_type"].lower() == os_preference.lower()]

        return filtered

    # ----------------------------------------------------
    # 2️⃣ Normalize Weights
    # ----------------------------------------------------
    def normalize_weights(self, weights):
        total = sum(weights.values())
        if total == 0:
            return weights

        return {k: v / total for k, v in weights.items()}

    # ----------------------------------------------------
    # 3️⃣ Calculate Effective Performance
    # ----------------------------------------------------
    def calculate_effective_performance(self, phone):
        return (
            0.7 * phone["performance_score"] +
            0.3 * phone["processor_score"]
        )

    # ----------------------------------------------------
    # 4️⃣ Score Phones
    # ----------------------------------------------------
    def score_phones(self, phones, weights):
        scored = []

        normalized_weights = self.normalize_weights(weights)

        for phone in phones:
            effective_performance = self.calculate_effective_performance(phone)

            final_score = (
                normalized_weights["camera"] * phone["camera_score"] +
                normalized_weights["battery"] * phone["battery_score"] +
                normalized_weights["performance"] * effective_performance +
                normalized_weights["display"] * phone["display_score"] +
                normalized_weights["software"] * phone["software_score"] +
                normalized_weights["value"] * phone["value_score"]
            )

            phone_copy = phone.copy()
            phone_copy["final_score"] = round(final_score, 2)

            scored.append(phone_copy)

        return sorted(scored, key=lambda x: x["final_score"], reverse=True)

    # ----------------------------------------------------
    # 5️⃣ Generate Explanation
    # ----------------------------------------------------
    def generate_explanation(self, phone, weights):
        strongest_factor = max(weights, key=weights.get)

        explanation_map = {
            "camera": "It offers strong camera performance.",
            "battery": "It provides excellent battery life.",
            "performance": f"It is powered by {phone['processor_name']} ensuring smooth performance.",
            "display": "It has a high-quality display experience.",
            "software": "It delivers a smooth and reliable software experience.",
            "value": "It offers strong value for money in this segment."
        }

        base_explanation = explanation_map.get(
            strongest_factor,
            "It matches your preferences well."
        )

        return (
            f"This phone was recommended because {base_explanation} "
            f"It fits within your budget of ₹{phone['price']}."
        )

    # ----------------------------------------------------
    # 6️⃣ Main Recommendation Method
    # ----------------------------------------------------
    def recommend(self, budget, weights, os_preference=None, top_n=3):
        filtered = self.filter_phones(budget, os_preference)

        if not filtered:
            return []

        ranked = self.score_phones(filtered, weights)

        top_results = ranked[:top_n]

        for phone in top_results:
            phone["explanation"] = self.generate_explanation(phone, weights)

        return top_results