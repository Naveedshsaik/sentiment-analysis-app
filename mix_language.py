def detect_mixed_language(text):

    text = text.lower()

    telugu_words = [
        "bagundi","baagundi","ayindi","ayindi","kaani","kani",
        "chala","chaala","ledu","undi","vastundi","late ayindi"
    ]

    hindi_words = [
        "bahut","acha","accha","nahi","hai","kharab","bahut acha"
    ]

    languages = []

    # Telugu detection (roman)
    for word in telugu_words:
        if word in text:
            languages.append("Telugu")
            break

    # Hindi detection
    for word in hindi_words:
        if word in text:
            languages.append("Hindi")
            break

    # English detection (default)
    if any(c.isalpha() for c in text):
        languages.append("English")

    return list(set(languages))