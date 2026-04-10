from src.preprocessing import clean_text
from src.language_detection import detect_language
from src.translation import translate_to_english
from src.sentiment import get_sentiment
from src.aspect_analysis import analyze_aspects
from src.rating_predictor import predict_rating


def analyze_review(text):

    cleaned = clean_text(text)

    # FIX: language return may be string
    lang = detect_language(cleaned)

    if isinstance(lang, dict):
        language = lang.get("language", "Unknown")
        confidence = lang.get("confidence", 0)
    else:
        language = lang
        confidence = 1.0

    translated = translate_to_english(cleaned, language)

    sentiment, score = get_sentiment(translated)

    aspects = analyze_aspects(translated)

    rating = predict_rating(sentiment, score)

    return {
        "language": language,
        "confidence": confidence,
        "translated_text": translated,
        "sentiment": sentiment,
        "score": score,
        "rating": rating,
        "aspects": aspects
    }