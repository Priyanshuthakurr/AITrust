🛡️ AITrust - AI Content Detection & Deepfake Detection System

A comprehensive AI-based platform to detect AI-generated text, deepfake images, and videos using Machine Learning & Deep Learning.

Python Streamlit Scikit-learn TensorFlow OpenCV NLP

---

🌟 Features

👨‍💻 Multi-Module AI Detection System  
Text Detection: Identify AI-generated vs Human-written text  
Image Detection: Detect deepfake or manipulated images  
Video Detection: Frame-based deepfake detection  

📄 File Upload Support  
Upload PDF or Images for text extraction  
OCR using Tesseract  
Automatic text analysis  

🧠 Explainable AI  
Keyword-based explanation of predictions  
Trust Score & Risk Level system  
Transparent AI decision-making  

🎯 Deepfake Detection (Advanced)  
GAN-based model for robust detection  
Handles compression, rotation, and transformations  
Frame-based video analysis  

📊 Smart Dashboard  
Real-time prediction results  
Confidence scores  
Clean and modern UI  

---

🎯 Key Highlights

✅ GAN-based Deepfake Detection Model  
✅ Explainable AI (XAI) Integration  
✅ Trust Score + Risk Level System  
✅ Handles Image Variations (Compression, Rotation)  
✅ Multi-format Input Support (Text, Image, Video)  
✅ Streamlit Interactive UI  

---

🚀 Quick Start

Prerequisites

Python 3.10+  

pip  

Virtual Environment (recommended)  

---

Installation

Clone the repository

```
git clone https://github.com/your-username/AITrust.git
cd AITrust.
```

Install dependencies
```
pip install -r requirements.txt
```

Run the application
```
streamlit run app.py
```

Access the application
Frontend: http://localhost:8501

🏗️ Project Structure
```
AITrust/
├── app.py                      # Main Streamlit application
├── aitrust_model.pkl          # Text classification model
├── tfidf_vectorizer.pkl       # TF-IDF vectorizer
├── gan_deepfake_detector.h5   # GAN discriminator model
├── gan_generator.h5           # GAN generator model
├── dataset/                   # Training datasets
├── notebooks/                 # Jupyter notebooks (training)
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation
```

🎨 Technology Stack
```
Frontend
Framework: Streamlit
Language: Python
UI: Streamlit Components

Backend / ML
Machine Learning: Scikit-learn (Logistic Regression)
NLP: TF-IDF Vectorization
Deep Learning: TensorFlow / Keras
Computer Vision: OpenCV
OCR: Tesseract
```

📱 Key Modules
```
Text Detection
AI vs Human text classification
Trust score generation
Explainable keyword analysis

Image Deepfake Detection
GAN-based model
Robust against transformations
Real-time image prediction

Video Deepfake Detection
Frame-by-frame analysis
Aggregated prediction
Confidence scoring
```

🧠 Model Details
```
Text Model
Algorithm: Logistic Regression
Feature Extraction: TF-IDF
Accuracy: ~98%

Image Model
Architecture: GAN (Generator + Discriminator)
Final Model Used: Discriminator
Purpose: Deepfake detection

Video Model
Approach: Frame-based detection
Uses image model for prediction
```

🔧 Configuration

Ensure models are present:
```
aitrust_model.pkl
tfidf_vectorizer.pkl
gan_deepfake_detector.h5
```

🚀 Deployment

Streamlit Cloud / Render / Local
```
streamlit run app.py
```

📊 Testing
```
Test cases:

✔ Original Image → Real

✔ Compressed Image → Real

✔ Rotated Image → Real

✔ Fake Image → Fake
```

🤝 Contributing
```
Fork the repository

Create a feature branch

Make changes

Submit a pull request
```

📄 License
```
This project is developed for academic and research purposes.
```

👨‍💻 Developer
```
Name: Priyanshu Thakur , Pragya Singh

College: Bennett University

Branch: CSE (AIML)
```

📞 Contact
```
Email: priyanshut740@gmail.com

GitHub: https://github.com/Priyanshuthakurr
```
