from transformers import pipeline
import re

# ✅ BETTER MODEL (multilingual support)
classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# ✅ SMART ASPECT KEYWORDS
aspect_keywords = {
    "battery": ["battery", "charging", "backup"],
    "delivery": ["delivery", "shipping", "late", "delay"],
    "price": ["price", "cost", "expensive", "cheap", "worth"],
    "quality": ["quality", "build", "material"],
    "performance": ["performance", "speed", "lag", "fast", "slow"],
    "packaging": ["packaging", "box", "packed"],
    "camera": ["camera", "photo", "picture"],
    "display": ["display", "screen"],
    "speaker": ["speaker", "sound", "audio"],
    "product": ["product", "item"]
}

# ✅ BETTER SENTENCE SPLIT
def split_sentences(text):
    return re.split(r"[,.!?]|but|however|although", text.lower())


def analyze_aspects(text):

    results = {}

    sentences = split_sentences(text)

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        for aspect, keywords in aspect_keywords.items():

            if any(word in sentence for word in keywords):

                sentiment = classifier(sentence)[0]

                label = sentiment["label"]

                # Convert star rating → sentiment
                if "1" in label or "2" in label:
                    final_sentiment = "Negative"
                elif "3" in label:
                    final_sentiment = "Neutral"
                else:
                    final_sentiment = "Positive"

                # ✅ STORE MULTIPLE RESULTS
                if aspect not in results:
                    results[aspect] = []

                results[aspect].append({
                    "sentence": sentence,
                    "sentiment": final_sentiment
                })

    return results