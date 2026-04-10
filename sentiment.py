from transformers import pipeline
import re

# -------------------------------
# 1. Load Sentiment Classifiers
# -------------------------------
classifier = pipeline("sentiment-analysis")
multilingual_classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# -------------------------------
# 2. Skip Spelling Correction for Telugu
# -------------------------------
def correct_text(text):
    if re.search(r'[\u0C00-\u0C7F]', text):
        return text
    try:
        from textblob import TextBlob
        return str(TextBlob(text).correct())
    except:
        return text

# -------------------------------
# 3. Split Text for Mixed Sentiment
# -------------------------------
def split_text(text):
    parts = re.split(
        r'\bbut\b|\bhowever\b|\bthough\b|\byet\b|\balthough\b|\bkaani\b|\bkooda\b',
        text,
        flags=re.IGNORECASE
    )
    return [p.strip() for p in parts if p.strip()]

# -------------------------------
# 4a. English Sentiment
# -------------------------------
def get_sentiment(text):
    text = correct_text(text)
    parts = split_text(text)
    results = []

    for part in parts:
        res = classifier(part)[0]
        label = res["label"]

        if label == "POSITIVE":
            sentiment = "Positive"
        elif label == "NEGATIVE":
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        results.append({"text": part, "sentiment": sentiment})

    return results

# -------------------------------
# 4b. Multilingual Sentiment
# -------------------------------
def get_sentiment_multilingual(text):
    """
    Handles Hindi, Telugu, Tamil, etc.
    Treats whole review as one clause for now.
    """
    res = multilingual_classifier(text)[0]
    label = res['label']  # e.g., '4 stars'
    stars = int(label[0])

    if stars >= 4:
        sentiment = "Positive"
    elif stars == 3:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"

    return [{"text": text, "sentiment": sentiment}]

# -------------------------------
# 5. Calculate Star Rating
# -------------------------------
def calculate_star(results):
    score = 0
    for r in results:
        if r["sentiment"] == "Positive":
            score += 1
        elif r["sentiment"] == "Negative":
            score -= 1

    if score >= 2:
        return 5
    elif score == 1:
        return 4
    elif score == 0:
        return 3
    elif score == -1:
        return 2
    else:
        return 1