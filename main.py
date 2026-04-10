from src.preprocessing import clean_text
from src.language_detection import detect_language
from src.translation import translate_to_english
from src.sentiment import get_sentiment
from src.aspect_analysis import analyze_aspects
from src.rating_predictor import predict_rating


def analyze_review(text):

    # ✅ Step 1: Clean
    cleaned = clean_text(text)

    # ✅ Step 2: Language Detection
    lang_info = detect_language(cleaned)
    language = lang_info["language"]
    confidence = lang_info["confidence"]

    # ✅ Step 3: Translation (if needed)
    translated = translate_to_english(cleaned, language)

    # ✅ Step 4: Sentiment
    sentiment, score = get_sentiment(translated)

    # ✅ Step 5: Aspect Analysis
    aspects = analyze_aspects(translated)

    # ✅ Step 6: Rating Prediction
    rating = predict_rating(sentiment, score)

    return {
        "original_text": text,
        "cleaned_text": cleaned,
        "language": language,
        "language_confidence": confidence,
        "translated_text": translated,
        "sentiment": sentiment,
        "score": score,
        "rating": rating,
        "aspects": aspects
    }