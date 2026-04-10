import pandas as pd
import random
import os

BASE_DIR = os.path.dirname(__file__)

reviews = [
    # English
    "Great product, works perfectly!",
    "Not worth the price, quality is poor.",
    "Average item, nothing special.",
    "Loved it! Fast delivery.",
    "Battery life is okay, could be better.",

    # Hindi
    "यह प्रोडक्ट बहुत अच्छा है",
    "बिल्कुल बेकार है",
    "ठीक ठाक है",
    "मुझे बहुत पसंद आया",
    "क्वालिटी अच्छी नहीं है",

    # Telugu
    "ఈ ప్రొడక్ట్ చాలా బాగుంది",
    "చాలా చెత్తగా ఉంది",
    "సరాసరి ఉంది",
    "నాకు చాలా నచ్చింది",
    "క్వాలిటీ బాగోలేదు",

    # Bangla
    "এই প্রোডাক্টটা খুব ভালো",
    "একদম বাজে",
    "মোটামুটি",
    "আমার খুব পছন্দ হয়েছে",
    "কোয়ালিটি ভালো না",

    # Mixed
    "Product bagundi but delivery late",
    "Bahut acha product but costly",
    "Quality thik hai but price high",
    "Nice product lekin packaging poor",
    "Super undi but battery weak"
]

platforms = ["amazon", "flipkart", "meesho", "myntra"]

for platform in platforms:
    data = []

    for i in range(500):
        review = random.choice(reviews)
        data.append([review])

    df = pd.DataFrame(data, columns=["review_text"])

    file_path = os.path.join(BASE_DIR, f"{platform}_reviews.csv")
    df.to_csv(file_path, index=False)

print("✅ 500 reviews generated for each platform!")