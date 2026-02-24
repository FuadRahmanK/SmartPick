import re


class InputParser:
    def __init__(self):

        self.brands = [
            "samsung", "apple", "iphone", "oneplus",
            "xiaomi", "realme", "iqoo", "vivo",
            "oppo", "nothing", "motorola"
        ]

        self.feature_keywords = {
            "performance": ["gaming", "game", "performance", "pubg", "bgmi", "cod", "editing"],
            "camera": ["camera", "photo", "photography", "selfie", "video"],
            "battery": ["battery", "backup", "long lasting"],
            "display": ["display", "screen", "amoled", "refresh rate"],
            "software": ["software", "updates", "stock android", "ui"]
        }

    # -----------------------------
    # Budget Extraction (Robust)
    # -----------------------------
    def extract_budget(self, text):
        text = text.lower()

        # 30k or 30 k
        match_k = re.search(r"(\d{1,3})\s?k", text)
        if match_k:
            return int(match_k.group(1)) * 1000

        # ₹30000 or 30000
        match = re.search(r"(₹?\s?)(\d{4,6})", text)
        if match:
            return int(match.group(2))

        # 30 thousand
        match_thousand = re.search(r"(\d{1,3})\s?thousand", text)
        if match_thousand:
            return int(match_thousand.group(1)) * 1000

        return None

    # -----------------------------
    # OS Detection (Neutral Supported)
    # -----------------------------
    def extract_os_preference(self, text):
        text = text.lower()

        if "no preference" in text or "doesn't matter" in text:
            return "Any"

        if "iphone" in text or "ios" in text:
            return "iOS"

        if "android" in text:
            return "Android"

        return None

    # -----------------------------
    # Brand Detection
    # -----------------------------
    def extract_brand_preference(self, text):
        text = text.lower()
        for brand in self.brands:
            if brand in text:
                return brand.capitalize()
        return None

    # -----------------------------
    # Feature Intent Detection
    # -----------------------------
    def detect_feature_from_text(self, text):
        text = text.lower()
        for feature, keywords in self.feature_keywords.items():
            for word in keywords:
                if word in text:
                    return feature
        return None

    # -----------------------------
    # Main Parse
    # -----------------------------
    def parse(self, text):
        return {
            "budget": self.extract_budget(text),
            "os_preference": self.extract_os_preference(text),
            "brand_preference": self.extract_brand_preference(text),
            "feature_detected": self.detect_feature_from_text(text)
        }