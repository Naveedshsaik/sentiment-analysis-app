from deep_translator import GoogleTranslator

# ✅ simple cache (improves speed)
translation_cache = {}

def translate_to_english(text, detected_lang="English"):

    try:
        # ✅ Skip if already English
        if detected_lang == "English":
            return text

        # ✅ Check cache
        if text in translation_cache:
            return translation_cache[text]

        translated = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(text)

        # ✅ Store in cache
        translation_cache[text] = translated

        return translated

    except Exception as e:
        print("Translation Error:", e)
        return text