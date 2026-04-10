import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
import base64

from transformers import pipeline

from src.language_detection import detect_language

st.set_page_config(layout="wide", page_title="Multilingual Sentiment Analysis")

# ---------------- LLM MODEL ----------------
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )

bert_model = load_model()

def get_sentiment_llm(text):
    try:
        result = bert_model(text[:512])[0]
        stars = int(result['label'][0])

        if stars >= 4:
            sentiment = "Positive"
        elif stars == 3:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"

        return sentiment, stars
    except:
        return "Neutral", 3

# ---------------- STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "platform" not in st.session_state:
    st.session_state.platform = None

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp { background: #f5f7fb; }
.title { font-size: 48px; font-weight: 800; }
.highlight { color: #4da3ff; }
.card {
    background: white;
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    cursor: pointer;
    transition: 0.3s;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}
.card img {
    height: 60px;
    object-fit: contain;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(__file__)

platforms = [
    ("Amazon", os.path.join(BASE_DIR, "assets", "amazon.png"), 4.2),
    ("Flipkart", os.path.join(BASE_DIR, "assets", "flipkart.png"), 4.0),
    ("Meesho", os.path.join(BASE_DIR, "assets", "meesho.png"), 4.3),
    ("Myntra", os.path.join(BASE_DIR, "assets", "myntra.png"), 4.1),
]

# ---------------- HELPERS ----------------
def safe_language_display(lang_data):
    if isinstance(lang_data, dict):
        language = lang_data.get("language", "Unknown")
        conf = lang_data.get("confidence", 0)
        try:
            confidence = float(conf) * 100
        except:
            confidence = 0
    elif isinstance(lang_data, list):
        language = lang_data[0]
        confidence = 100
    else:
        language = str(lang_data)
        confidence = 100
    return language, confidence

def normalize_language(language):
    if isinstance(language, list):
        return ", ".join(map(str, language))
    return str(language)

def safe_read_csv(file_path):
    try:
        return pd.read_csv(file_path, quotechar='"', on_bad_lines='skip', encoding='utf-8')
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame(columns=['review_text'])

# ---------------- HOME ----------------
if st.session_state.page == "home":

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown(
            '<div class="title">Multilingual <span class="highlight">Sentiment</span><br>Product Analysis</div>',
            unsafe_allow_html=True
        )
        st.write("Understand customer feedback across Indian e-commerce platforms")

        if st.button("🔍 Check Single Review"):
            st.session_state.page = "single"
            st.rerun()

        if st.button("📂 Upload Bulk Reviews"):
            st.session_state.page = "bulk"
            st.rerun()

        # ✅ NEW BUTTON
        if st.button("📊 Overall Platforms Review"):
            st.session_state.page = "overall"
            st.rerun()

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=220)

    st.markdown("## 🔒 Explore Platforms")
    cols = st.columns(4)

    for i, col in enumerate(cols):
        name, logo, rating = platforms[i]
        with col:
            with open(logo, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()

            st.image(f"data:image/png;base64,{b64}", width=60)
            st.markdown(f"**{name}**")
            st.markdown(f"{rating} ⭐")

            if st.button(f"View {name} Reviews", key=f"btn_{name}"):
                st.session_state.page = "platform"
                st.session_state.platform = name
                st.rerun()

# ---------------- SINGLE ----------------
elif st.session_state.page == "single":

    st.title("🔍 Single Review Analysis")
    review = st.text_area("Enter Review")

    if st.button("Analyze"):
        if review.strip():
            lang_data = detect_language(review)
            language, _ = safe_language_display(lang_data)
            language = normalize_language(language)

            sentiment, star = get_sentiment_llm(review)

            st.success("✅ Analysis Done")
            st.write(f"Language: {language}")
            st.write(f"Sentiment: {sentiment}")
            st.write(f"Stars: {'⭐'*star}")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- BULK ----------------
elif st.session_state.page == "bulk":

    st.title("📂 Bulk Upload")
    file = st.file_uploader("Upload CSV")

    if file:
        df = safe_read_csv(file)

        if not df.empty:
            df = df.rename(columns={df.columns[0]: "review_text"})

            def analyze(row):
                review = str(row['review_text'])

                lang_data = detect_language(review)
                language, _ = safe_language_display(lang_data)
                language = normalize_language(language)

                sentiment, star = get_sentiment_llm(review)

                return pd.Series([language, sentiment, star])

            df[['language','sentiment','star']] = df.apply(analyze, axis=1)

            st.dataframe(df)
            st.bar_chart(df['sentiment'].value_counts())
            st.bar_chart(df['star'].value_counts())

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- PLATFORM ----------------
elif st.session_state.page == "platform":

    platform_name = st.session_state.platform
    st.title(f"📊 {platform_name} Reviews Dashboard")

    file_path = os.path.join(BASE_DIR, "data", f"{platform_name.lower()}_reviews.csv")

    if os.path.exists(file_path):
        df = safe_read_csv(file_path)

        def analyze(row):
            review = str(row['review_text'])

            lang_data = detect_language(review)
            language, _ = safe_language_display(lang_data)
            language = normalize_language(language)

            sentiment, star = get_sentiment_llm(review)

            return pd.Series([language, sentiment, star])

        df[['language','sentiment','star']] = df.apply(analyze, axis=1)

        st.dataframe(df)
        st.bar_chart(df['sentiment'].value_counts())
        st.bar_chart(df['star'].value_counts())

    else:
        st.error("CSV not found")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- OVERALL ----------------
elif st.session_state.page == "overall":

    st.title("📊 Overall Platforms Analysis")

    platform_files = {
        "Amazon": os.path.join(BASE_DIR, "data", "amazon_reviews.csv"),
        "Flipkart": os.path.join(BASE_DIR, "data", "flipkart_reviews.csv"),
        "Meesho": os.path.join(BASE_DIR, "data", "meesho_reviews.csv"),
        "Myntra": os.path.join(BASE_DIR, "data", "myntra_reviews.csv"),
    }

    results = {}

    for name, path in platform_files.items():
        if os.path.exists(path):
            df = safe_read_csv(path)

            stars = []
            for review in df['review_text']:
                _, star = get_sentiment_llm(str(review))
                stars.append(star)

            avg_rating = round(sum(stars) / len(stars), 2)
            results[name] = avg_rating

    if results:
        st.subheader("📊 Average Ratings Comparison")
        st.bar_chart(pd.Series(results))

        st.subheader("🥧 Platform Share")
        pie = go.Figure(data=[go.Pie(
            labels=list(results.keys()),
            values=list(results.values())
        )])
        st.plotly_chart(pie)

        best_platform = max(results, key=results.get)
        best_score = results[best_platform]

        st.success(f"🏆 Best Platform: {best_platform} ({best_score} ⭐)")

    else:
        st.error("No data found")

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()