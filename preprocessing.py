import re

def clean_text(text):

    # ✅ lowercase
    text = text.lower()

    # ✅ remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # ✅ remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # ✅ normalize repeated characters (goooood → good)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    # ✅ keep emojis but remove unwanted symbols
    text = re.sub(r"[^\w\s₹$€£😊😡😍😢😂👍👎]", "", text)

    # ✅ remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text