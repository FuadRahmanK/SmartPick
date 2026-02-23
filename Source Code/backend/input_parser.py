import re


class InputParser:
    def __init__(self):
        # Keyword mappings
        self.keyword_map = {
            "gaming": ["gaming", "game", "pubg", "bgmi", "cod", "call of duty"],
            "camera": ["camera", "photo", "photography", "selfie", "video"],
            "battery": ["battery", "long lasting", "full day", "heavy usage"],
            "software": ["clean software", "stock android", "no bloatware", "smooth ui", "updates"],
            "value": ["value", "value for money", "affordable", "worth it"],
        }

    # ----------------------------------------------------
    # 1️⃣ Extract Budget
    # ----------------------------------------------------
    def extract_budget(self, text):
        text = text.lower()

        # Match numbers like 50000 or ₹50000
        match = re.search(r"(₹?\s?)(\d{4,6})", text)

        if match:
            return int(match.group(2))

        # Match patterns like 50k
        match_k = re.search(r"(\d{2,3})\s?k", text)
        if match_k:
            return int(match_k.group(1)) * 1000

        return None

    # ----------------------------------------------------
    # 2️⃣ Extract OS Preference
    # ----------------------------------------------------
    def extract_os_preference(self, text):
        text = text.lower()

        if "iphone" in text or "ios" in text:
            return "iOS"

        if "android" in text:
            return "Android"

        return None

    # ----------------------------------------------------
    # 3️⃣ Boost Weights Based on Keywords
    # ----------------------------------------------------
    def boost_weights(self, text, weights):
        text = text.lower()
        boosted = False

        # Gaming boosts
        if any(word in text for word in self.keyword_map["gaming"]):
            weights["performance"] += 2
            weights["battery"] += 1
            boosted = True

        # Camera boosts
        if any(word in text for word in self.keyword_map["camera"]):
            weights["camera"] += 2
            boosted = True

        # Battery boosts
        if any(word in text for word in self.keyword_map["battery"]):
            weights["battery"] += 2
            boosted = True

        # Software boosts
        if any(word in text for word in self.keyword_map["software"]):
            weights["software"] += 2
            boosted = True

        # Value boosts
        if any(word in text for word in self.keyword_map["value"]):
            weights["value"] += 2
            boosted = True

        return weights, boosted

    # ----------------------------------------------------
    # 4️⃣ Parse Entire Input
    # ----------------------------------------------------
    def parse(self, text, current_weights):
        result = {
            "budget": None,
            "os_preference": None,
            "weights": current_weights,
            "priority_detected": False
        }

        budget = self.extract_budget(text)
        if budget:
            result["budget"] = budget

        os_pref = self.extract_os_preference(text)
        if os_pref:
            result["os_preference"] = os_pref

        updated_weights, boosted = self.boost_weights(text, current_weights)
        result["weights"] = updated_weights
        result["priority_detected"] = boosted

        return result