import re
from langdetect import detect, DetectorFactory

# Fix randomness in langdetect
DetectorFactory.seed = 0

# ---------------- Telugu + Hindi word lists (Roman) ----------------
TELUGU_WORDS = [
    "bagundi", "baagundi", "ayindi", "kaani", "kani",
    "chala", "chaala", "ledu", "undi", "vastundi", "late ayindi"
]

HINDI_WORDS = [
    "bahut", "acha", "accha", "nahi", "hai", "kharab", "bahut acha"
]

# ---------------- Detect language ----------------
def detect_language(text):
    text = text.strip()
    if not text:
        return {"language": "Unknown", "confidence": 0.0}

    # 1️⃣ Telugu script check
    if re.search(r'[\u0C00-\u0C7F]', text):
        return {"language": "Telugu", "confidence": 1.0}

    # 2️⃣ Roman Telugu / Hindi detection
    text_lower = text.lower()
    languages = []
    confidence = {}

    # Telugu
    if any(word in text_lower for word in TELUGU_WORDS):
        languages.append("Telugu")
        confidence["Telugu"] = 0.95

    # Hindi
    if any(word in text_lower for word in HINDI_WORDS):
        languages.append("Hindi")
        confidence["Hindi"] = 0.95

    # English fallback
    if re.search(r'[a-zA-Z]', text):
        languages.append("English")
        confidence["English"] = 0.99

    # 3️⃣ If no known words, fallback to langdetect
    if not languages:
        try:
            lang = detect(text)
            lang_map = {
                "en": ("English", 0.99),
                "hi": ("Hindi", 0.95),
                "te": ("Telugu", 0.95),
                "ta": ("Tamil", 0.95),
                "kn": ("Kannada", 0.95),
                "ml": ("Malayalam", 0.95)
            }
            if lang in lang_map:
                languages.append(lang_map[lang][0])
                confidence[lang_map[lang][0]] = lang_map[lang][1]
            else:
                languages.append(lang.capitalize())
                confidence[lang.capitalize()] = 0.85
        except:
            languages.append("Unknown")
            confidence["Unknown"] = 0.0

    return {"language": languages, "confidence": confidence}


# ---------------- Mixed language helper ----------------
def detect_mixed_language(text):
    data = detect_language(text)
    # Flatten into list
    return data["language"]

# ---------------- Example ----------------
if __name__ == "__main__":
    samples = [
        "product baagundi kaani delivery late ayyindi",
        "yeh product bahut acha hai",
        "This product is excellent",
        "chala bagundi but late delivery"
    ]
    for s in samples:
        print(s)
        print(detect_language(s))
        print("-"*40)