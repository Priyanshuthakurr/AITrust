import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import cv2
from tensorflow.keras.models import load_model

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AITrust Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# LOAD MODELS
# -----------------------------
text_model = pickle.load(open("aitrust_model.pkl","rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl","rb"))

image_model = load_model("deepfake_image_model.h5")

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    return text.lower()

# -----------------------------
# TEXT PREDICTION
# -----------------------------
def predict_with_trust_score(text):

    text = clean_text(text)

    text_tfidf = vectorizer.transform([text])

    prob = text_model.predict_proba(text_tfidf)[0]

    ai_prob = prob[1]
    human_prob = prob[0]

    trust_score = round(human_prob * 100,2)

    if trust_score > 70:
        risk = "Low Risk"
    elif trust_score > 40:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return trust_score, round(ai_prob*100,2), risk

# -----------------------------
# EXPLAINABLE AI
# -----------------------------
def explain_prediction(text,top_n=5):

    text = clean_text(text)

    text_tfidf = vectorizer.transform([text])

    feature_names = vectorizer.get_feature_names_out()
    coefs = text_model.coef_[0]
    tfidf_array = text_tfidf.toarray()[0]

    word_importance = []

    for i in range(len(tfidf_array)):
        if tfidf_array[i] > 0:
            word_importance.append(
                (feature_names[i], coefs[i]*tfidf_array[i])
            )

    word_importance = sorted(
        word_importance,
        key=lambda x:abs(x[1]),
        reverse=True
    )

    return word_importance[:top_n]

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🛡️ AITrust")

page = st.sidebar.radio(
    "Navigation",
    ["Text Detection","Image Deepfake","Video Deepfake"]
)

st.sidebar.info(
"""
AI Misuse Detection Platform

Detect AI generated text  
Explain predictions  
Image & Video Deepfake Detection
"""
)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛡️ AITrust")
st.caption("AI Content Detection & Trust Evaluation Platform")

st.divider()

# ====================================
# TEXT DETECTION
# ====================================
if page=="Text Detection":

    st.subheader("✍ AI Text Detection")

    text_input = st.text_area("Enter text",height=200)

    if st.button("Analyze Text"):

        trust_score, ai_probability, risk = predict_with_trust_score(text_input)

        st.divider()

        col1,col2,col3 = st.columns(3)

        col1.metric("Human Trust Score",f"{trust_score}%")
        col2.metric("AI Probability",f"{ai_probability}%")
        col3.metric("Risk Level",risk)

        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ai_probability,
            title={'text':"AI Probability"},
            gauge={
                'axis':{'range':[0,100]},
                'bar':{'color':"red"},
                'steps':[
                    {'range':[0,40],'color':"green"},
                    {'range':[40,70],'color':"yellow"},
                    {'range':[70,100],'color':"red"}
                ]
            }
        ))

        st.plotly_chart(fig,use_container_width=True)

        st.divider()

        st.subheader("🧠 Explainable AI")

        explanation = explain_prediction(text_input)

        words = [w[0] for w in explanation]
        scores = [w[1] for w in explanation]

        df = pd.DataFrame({
            "Word":words,
            "Impact":scores
        })

        st.bar_chart(df.set_index("Word"))

# ====================================
# IMAGE DEEPFAKE DETECTION
# ====================================
elif page=="Image Deepfake":

    st.subheader("🖼 Image Deepfake Detection")

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg","jpeg","png"]
    )

    if uploaded_file is not None:

        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

        image = cv2.imdecode(file_bytes, 1)

        st.image(image, caption="Uploaded Image")

        img = cv2.resize(image,(128,128))
        img = img/255.0
        img = np.reshape(img,(1,128,128,3))

        prediction = image_model.predict(img)[0][0]

        if prediction > 0.5:
            st.error("⚠ Fake Image Detected")
        else:
            st.success("✅ Real Image")

# ====================================
# VIDEO DEEPFAKE DETECTION
# ====================================
elif page=="Video Deepfake":

    st.subheader("🎥 Video Deepfake Detection")

    video_file = st.file_uploader(
        "Upload Video",
        type=["mp4","mov","avi"]
    )

    if video_file is not None:

        with open("temp_video.mp4","wb") as f:
            f.write(video_file.read())

        st.video("temp_video.mp4")

        cap = cv2.VideoCapture("temp_video.mp4")

        fake_count = 0
        real_count = 0
        frame_count = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            if frame_count % 20 == 0:

                img = cv2.resize(frame,(128,128))
                img = img/255.0
                img = np.reshape(img,(1,128,128,3))

                prediction = image_model.predict(img)[0][0]

                if prediction > 0.5:
                    fake_count += 1
                else:
                    real_count += 1

        cap.release()

        st.write("Frames analyzed:",fake_count + real_count)

        if fake_count > real_count:
            st.error("⚠ Deepfake Video Detected")
        else:
            st.success("✅ Real Video")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.markdown(
"""
<center>
AITrust © 2026 | AI Misuse Detection System  
Built using Machine Learning + Explainable AI
</center>
""",
unsafe_allow_html=True
)