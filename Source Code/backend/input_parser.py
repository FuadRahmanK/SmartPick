import re


class InputParser:

    # ----------- BULLETPROOF BUDGET -----------
    def extract_budget(self, text):
        text = text.lower().replace(",", "")

        match_k = re.search(r"(\d{1,3})\s?k", text)
        if match_k:
            return int(match_k.group(1)) * 1000

        match = re.search(r"₹?\s?(\d{4,6})", text)
        if match:
            return int(match.group(1))

        match_thousand = re.search(r"(\d{1,3})\s?thousand", text)
        if match_thousand:
            return int(match_thousand.group(1)) * 1000

        return None

    def extract_os_preference(self, text):
        text = text.lower()

        if "any" in text or "no preference" in text:
            return "Any"

        if "android" in text:
            return "Android"

        if "iphone" in text or "ios" in text:
            return "iOS"

        return None

    def detect_feature_from_text(self, text):
        text = text.lower()

        if "camera" in text:
            return "camera"
        if "battery" in text:
            return "battery"
        if "gaming" in text or "performance" in text or "editing" in text:
            return "performance"
        if "display" in text or "screen" in text:
            return "display"
        if "software" in text or "updates" in text:
            return "software"

        return None

    def parse(self, text):
        return {
            "budget": self.extract_budget(text),
            "os_preference": self.extract_os_preference(text),
            "feature_detected": self.detect_feature_from_text(text)
        }