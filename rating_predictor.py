def predict_rating(sentiment, score=0.5):

    sentiment = sentiment.lower()

    if sentiment == "positive":
        if score > 0.85:
            return 5
        else:
            return 4

    elif sentiment == "neutral":
        return 3

    elif sentiment == "negative":
        if score > 0.85:
            return 1
        else:
            return 2

    return 3