import streamlit as st
import pickle
import numpy as np
# import cv2
from PIL import Image
# import pytesseract
import pdfplumber
import tempfile
# from tensorflow.keras.models import load_model

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AITrust Dashboard",
    page_icon="🛡",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ===== RESET & BASE ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080b14;
    color: #e2e8f8;
}

/* ===== HIDE STREAMLIT DEFAULTS ===== */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem !important;
    max-width: 1100px !important;
}

/* ===== BACKGROUND ===== */
.stApp {
    background: #080b14;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(30, 60, 120, 0.25) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(0, 180, 120, 0.08) 0%, transparent 50%);
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: rgba(10, 14, 28, 0.95) !important;
    border-right: 1px solid rgba(100, 140, 255, 0.12) !important;
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.2rem !important;
}

/* Sidebar Brand */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(100, 140, 255, 0.15);
}
.sidebar-brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1e40af, #0ea5e9);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.sidebar-brand-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #e2e8f8;
    letter-spacing: 0.03em;
}
.sidebar-brand-sub {
    font-size: 0.65rem;
    color: #4a6a9e;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Sidebar Radio */
[data-testid="stSidebar"] .stRadio > label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4a6a9e;
    margin-bottom: 0.75rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 4px;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebar"] .stRadio label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 10px 14px;
    transition: all 0.2s;
    cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #8baad4;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(59, 130, 246, 0.08);
    border-color: rgba(59, 130, 246, 0.2);
    color: #c8daf8;
}
[data-testid="stSidebar"] .stRadio label[data-testid="stMarkdownContainer"] {
    color: #fff;
}

/* ===== PAGE HEADER ===== */
.page-header {
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(100, 140, 255, 0.1);
}
.page-header-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.6rem;
}
.page-header-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #e2e8f8;
    line-height: 1.15;
    margin-bottom: 0.4rem;
}
.page-header-title span {
    color: #3b82f6;
}
.page-header-sub {
    font-size: 0.92rem;
    color: #4a6a9e;
    font-weight: 300;
}

/* ===== CARDS ===== */
.ait-card {
    background: rgba(15, 22, 45, 0.7);
    border: 1px solid rgba(100, 140, 255, 0.1);
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
    backdrop-filter: blur(10px);
}
.ait-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4a6a9e;
    margin-bottom: 1rem;
}

/* ===== METRIC CARDS ===== */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: rgba(15, 22, 45, 0.8);
    border: 1px solid rgba(100, 140, 255, 0.12);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.metric-card.blue::before { background: linear-gradient(90deg, #1d4ed8, #3b82f6); }
.metric-card.green::before { background: linear-gradient(90deg, #065f46, #10b981); }
.metric-card.red::before { background: linear-gradient(90deg, #991b1b, #ef4444); }
.metric-card.amber::before { background: linear-gradient(90deg, #92400e, #f59e0b); }
.metric-label {
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a6a9e;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #e2e8f8;
    line-height: 1;
}
.metric-badge {
    display: inline-block;
    margin-top: 0.6rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.06em;
}
.badge-low { background: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.25); }
.badge-medium { background: rgba(245, 158, 11, 0.12); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.25); }
.badge-high { background: rgba(239, 68, 68, 0.12); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.25); }

/* ===== KEYWORD TABLE ===== */
.kw-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid rgba(100, 140, 255, 0.07);
}
.kw-row:last-child { border-bottom: none; }
.kw-word {
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    color: #93c5fd;
}
.kw-bar-wrap {
    flex: 1;
    margin: 0 1rem;
    background: rgba(100, 140, 255, 0.07);
    border-radius: 4px;
    height: 4px;
    overflow: hidden;
}
.kw-bar {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #1d4ed8, #3b82f6);
}
.kw-score {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #4a6a9e;
    min-width: 45px;
    text-align: right;
}

/* ===== RESULT BADGE ===== */
.result-hero {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1.5rem;
    background: rgba(15, 22, 45, 0.8);
    border: 1px solid rgba(100, 140, 255, 0.12);
    border-radius: 14px;
    margin-bottom: 1rem;
}
.result-icon {
    width: 56px; height: 56px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}
.result-icon.fake { background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.25); }
.result-icon.real { background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); }
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #4a6a9e;
}
.result-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #e2e8f8;
}
.result-conf {
    font-size: 0.85rem;
    color: #4a6a9e;
}

/* ===== STREAMLIT ELEMENTS ===== */
.stTextArea textarea {
    background: rgba(15, 22, 45, 0.8) !important;
    border: 1px solid rgba(100, 140, 255, 0.15) !important;
    border-radius: 10px !important;
    color: #e2e8f8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 12px 14px !important;
}
.stTextArea textarea:focus {
    border-color: rgba(59, 130, 246, 0.4) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.08) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #1e3a8a, #1d4ed8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 10px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.25) !important;
}

[data-testid="stFileUploader"] {
    background: rgba(15, 22, 45, 0.5) !important;
    border: 1px dashed rgba(100, 140, 255, 0.2) !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(59, 130, 246, 0.35) !important;
}

.stSuccess {
    background: rgba(16, 185, 129, 0.08) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: 8px !important;
    color: #6ee7b7 !important;
}
.stWarning {
    background: rgba(245, 158, 11, 0.08) !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    border-radius: 8px !important;
}
.stMetric {
    background: rgba(15, 22, 45, 0.7) !important;
    border: 1px solid rgba(100, 140, 255, 0.1) !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="metric-container"] {
    background: rgba(15, 22, 45, 0.7);
    border: 1px solid rgba(100, 140, 255, 0.1);
    border-radius: 12px;
    padding: 1rem 1.25rem;
}

/* Divider */
hr { border-color: rgba(100, 140, 255, 0.1) !important; }

/* Image */
.stImage img {
    border-radius: 12px !important;
    border: 1px solid rgba(100, 140, 255, 0.12) !important;
}

/* Video */
.stVideo {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(100, 140, 255, 0.12) !important;
}

/* Section heading */
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #e2e8f8 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080b14; }
::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.3); border-radius: 10px; }

/* Status dot */
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #10b981;
    margin-right: 6px;
    box-shadow: 0 0 6px #10b981;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD MODELS ----------------
text_model = pickle.load(open("aitrust_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

try:
    image_model = load_model("deepfake_image_model.h5")
except:
    image_model = None


# ---------------- FUNCTIONS ----------------

def clean_text(text):
    return text.lower()

def predict_with_trust_score(text):
    text = clean_text(text)
    text_tfidf = vectorizer.transform([text])
    prob = text_model.predict_proba(text_tfidf)[0]
    ai_prob = prob[1]
    human_prob = prob[0]
    trust_score = round(human_prob * 100, 2)
    if trust_score > 70:
        risk = "Low Risk"
    elif trust_score > 40:
        risk = "Medium Risk"
    else:
        risk = "High Risk"
    return trust_score, round(ai_prob * 100, 2), risk

def explain_prediction(text, top_n=5):
    text = clean_text(text)
    tfidf = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf.toarray()[0]
    top_indices = scores.argsort()[-top_n:][::-1]
    return [(feature_names[i], scores[i]) for i in top_indices]

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()
        return text
    elif "image" in uploaded_file.type:
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)
    return ""

def predict_image(img):
    if image_model is None:
        return "Model not loaded", 0
    img = img.convert("RGB")
    img = img.resize((128, 128))
    img = np.array(img) / 255.0
    img = np.reshape(img, (1, 128, 128, 3))
    pred = image_model.predict(img)[0][0]
    if pred > 0.6:
        return "Fake", pred * 100
    else:
        return "Real", (1 - pred) * 100

def predict_video(video_path):
    if image_model is None:
        return "Model not loaded", 0
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error opening video", 0
    fake_count = 0
    total = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (128, 128))
        frame = frame / 255.0
        frame = np.reshape(frame, (1, 128, 128, 3))
        pred = image_model.predict(frame)[0][0]
        if pred > 0.6:
            fake_count += 1
        total += 1
    cap.release()
    if total == 0:
        return "No frames detected", 0
    fake_ratio = fake_count / total
    if fake_ratio > 0.5:
        return "Fake Video", fake_ratio * 100
    else:
        return "Real Video", (1 - fake_ratio) * 100


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🛡</div>
        <div>
            <div class="sidebar-brand-text">AITrust</div>
            <div class="sidebar-brand-sub">Detection Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["✍  Text Detection", "🖼  Image Deepfake", "🎥  Video Deepfake"],
        label_visibility="visible"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 12px 14px; background: rgba(16,185,129,0.06); border: 1px solid rgba(16,185,129,0.15); border-radius: 10px;">
        <div style="font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: #4a6a9e; margin-bottom: 8px;">System Status</div>
        <div style="font-size: 0.8rem; color: #6ee7b7;">
            <span class="status-dot"></span> Text Model Active
        </div>
        <div style="font-size: 0.8rem; color: #6ee7b7; margin-top: 4px;">
            <span class="status-dot"></span> Image Model Active
        </div>
        <div style="font-size: 0.8rem; color: #6ee7b7; margin-top: 4px;">
            <span class="status-dot"></span> Video Pipeline Ready
        </div>
    </div>
    """, unsafe_allow_html=True)


# ================= TEXT DETECTION =================

if "Text Detection" in page:

    st.markdown("""
    <div class="page-header">
        <div class="page-header-eyebrow">Module 01</div>
        <div class="page-header-title">Text <span>AI</span> Detection</div>
        <div class="page-header-sub">Analyze written content for AI-generated signals using TF-IDF + ML classification</div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_gap = st.columns([1, 0.01])

    with col_input:
        st.markdown('<div class="ait-card"><div class="ait-card-title">Input</div>', unsafe_allow_html=True)
        text_input = st.text_area(
            "Paste your text below",
            height=160,
            placeholder="Enter the content you want to analyze for AI generation signals...",
            label_visibility="collapsed"
        )
        uploaded_file = st.file_uploader(
            "Or upload a PDF / Image file",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Supported: PDF, PNG, JPG, JPEG (max 200MB)"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    final_text = ""

    if uploaded_file:
        extracted = extract_text_from_file(uploaded_file)
        if extracted:
            st.success(f"✓  Text extracted from file — {len(extracted)} characters found")
            with st.expander("Preview extracted text"):
                st.write(extracted[:800] + ("..." if len(extracted) > 800 else ""))
            final_text = extracted

    if text_input:
        final_text = text_input

    analyze_btn = st.button("🔍  Analyze Text", use_container_width=False)

    if analyze_btn:
        if final_text.strip() == "":
            st.warning("⚠ Please enter text or upload a file before analyzing.")
        else:
            with st.spinner("Analyzing content..."):
                trust, ai_prob, risk = predict_with_trust_score(final_text)
                explanation = explain_prediction(final_text)

            # Risk color
            if risk == "Low Risk":
                risk_class = "badge-low"
                metric_color = "green"
            elif risk == "Medium Risk":
                risk_class = "badge-medium"
                metric_color = "amber"
            else:
                risk_class = "badge-high"
                metric_color = "red"

            st.markdown("<br>", unsafe_allow_html=True)

            # Metric cards
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card blue">
                    <div class="metric-label">Human Trust Score</div>
                    <div class="metric-value">{trust}%</div>
                    <span class="metric-badge badge-low">Human Written</span>
                </div>
                <div class="metric-card {metric_color}">
                    <div class="metric-label">AI Probability</div>
                    <div class="metric-value">{ai_prob}%</div>
                    <span class="metric-badge badge-high">AI Generated</span>
                </div>
                <div class="metric-card {metric_color}">
                    <div class="metric-label">Risk Level</div>
                    <div class="metric-value" style="font-size:1.4rem;">{risk}</div>
                    <span class="metric-badge {risk_class}">{risk}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Keyword explainability
            st.markdown("""
            <div class="ait-card">
                <div class="ait-card-title">🧠 Explainable AI — Key Signals</div>
            """, unsafe_allow_html=True)

            max_score = max([s for _, s in explanation]) if explanation else 1
            for word, score in explanation:
                bar_pct = int((score / max_score) * 100) if max_score > 0 else 0
                st.markdown(f"""
                <div class="kw-row">
                    <span class="kw-word">{word}</span>
                    <div class="kw-bar-wrap"><div class="kw-bar" style="width:{bar_pct}%"></div></div>
                    <span class="kw-score">{score:.4f}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


# ================= IMAGE DEEPFAKE =================

elif "Image Deepfake" in page:

    st.markdown("""
    <div class="page-header">
        <div class="page-header-eyebrow">Module 02</div>
        <div class="page-header-title">Image <span>Deepfake</span> Detection</div>
        <div class="page-header-sub">Upload a photo to analyze authenticity using our trained GAN detection model</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ait-card"><div class="ait-card-title">Upload Image</div>', unsafe_allow_html=True)
    img_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if img_file:
        img = Image.open(img_file)

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown('<div class="ait-card"><div class="ait-card-title">Uploaded Image</div>', unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="ait-card"><div class="ait-card-title">Analysis</div>', unsafe_allow_html=True)
            analyze_img_btn = st.button("🔍  Analyze Image", use_container_width=True)

            if analyze_img_btn:
                with st.spinner("Running deepfake detection..."):
                    label, confidence = predict_image(img)

                icon = "⚠" if label == "Fake" else "✓"
                icon_class = "fake" if label == "Fake" else "real"
                conf_color = "#ef4444" if label == "Fake" else "#10b981"

                st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <div class="result-hero">
                        <div class="result-icon {icon_class}">{icon}</div>
                        <div>
                            <div class="result-label">Prediction</div>
                            <div class="result-value" style="color: {conf_color}">{label}</div>
                            <div class="result-conf">Confidence: {confidence:.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Confidence bar
                st.markdown(f"""
                <div style="margin-top:1rem;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#4a6a9e; text-transform:uppercase; letter-spacing:0.1em;">Confidence Score</span>
                        <span style="font-family:'DM Mono',monospace; font-size:0.78rem; color:{conf_color};">{confidence:.1f}%</span>
                    </div>
                    <div style="background:rgba(100,140,255,0.08); border-radius:6px; height:8px; overflow:hidden;">
                        <div style="width:{min(confidence,100):.0f}%; height:100%; background:linear-gradient(90deg, {'#991b1b, #ef4444' if label=='Fake' else '#065f46, #10b981'}); border-radius:6px; transition:width 0.8s;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)


# ================= VIDEO DEEPFAKE =================

elif "Video Deepfake" in page:

    st.markdown("""
    <div class="page-header">
        <div class="page-header-eyebrow">Module 03</div>
        <div class="page-header-title">Video <span>Deepfake</span> Detection</div>
        <div class="page-header-sub">Frame-by-frame analysis of uploaded video for synthetic manipulation detection</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ait-card"><div class="ait-card-title">Upload Video</div>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if video_file:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<div class="ait-card"><div class="ait-card-title">Video Preview</div>', unsafe_allow_html=True)
            st.video(video_file)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="ait-card"><div class="ait-card-title">Analysis</div>', unsafe_allow_html=True)
            analyze_vid_btn = st.button("🔍  Analyze Video", use_container_width=True)

            if analyze_vid_btn:
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(video_file.read())

                with st.spinner("Processing frames — this may take a moment..."):
                    result, confidence = predict_video(tfile.name)

                is_fake = "Fake" in result
                icon = "⚠" if is_fake else "✓"
                icon_class = "fake" if is_fake else "real"
                conf_color = "#ef4444" if is_fake else "#10b981"

                st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <div class="result-hero">
                        <div class="result-icon {icon_class}">{icon}</div>
                        <div>
                            <div class="result-label">Prediction</div>
                            <div class="result-value" style="color: {conf_color}">{result}</div>
                            <div class="result-conf">Confidence: {confidence:.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="margin-top:1rem;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:#4a6a9e; text-transform:uppercase; letter-spacing:0.1em;">Detection Score</span>
                        <span style="font-family:'DM Mono',monospace; font-size:0.78rem; color:{conf_color};">{confidence:.1f}%</span>
                    </div>
                    <div style="background:rgba(100,140,255,0.08); border-radius:6px; height:8px; overflow:hidden;">
                        <div style="width:{min(confidence,100):.0f}%; height:100%; background:linear-gradient(90deg, {'#991b1b, #ef4444' if is_fake else '#065f46, #10b981'}); border-radius:6px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
