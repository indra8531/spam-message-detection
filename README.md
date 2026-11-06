# SpamShield AI - AI-Powered Spam Message Detection System

[![Live Demo](https://img.shields.io/badge/Live_Demo-Active-06B6D4?style=for-the-badge&logo=googlechrome&logoColor=white)][(https://veteran-approximately-referring-dee.trycloudflare.com/#detector)](https://veteran-approximately-referring-dee.trycloudflare.com/)
[![Presentation Deck](https://img.shields.io/badge/Presentation-12_Slides-3B82F6?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white)](https://veteran-approximately-referring-dee.trycloudflare.com/presentation.html)
[![Model Accuracy](https://img.shields.io/badge/Test_Accuracy-100.0%25-10B981?style=for-the-badge&logo=scikitlearn&logoColor=white)](#-model-evaluation-performance)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> 🌐 **Live Website Link**: **[https://veteran-approximately-referring-dee.trycloudflare.com](https://veteran-approximately-referring-dee.trycloudflare.com)**  
> 📊 **Interactive Web Presentation Deck**: **[https://veteran-approximately-referring-dee.trycloudflare.com/presentation.html](https://veteran-approximately-referring-dee.trycloudflare.com/presentation.html)**  
> 📥 **Download PowerPoint File**: **[SpamShield_AI_Presentation.pptx](SpamShield_AI_Presentation.pptx)**

**SpamShield AI** is a modern, responsive, cybersecurity-themed AI application engineered to detect and classify spam and smishing messages from normal communication in real time. It utilizes Natural Language Processing (NLP), TF-IDF feature extraction, and machine learning models trained on labeled message datasets to deliver instant probabilistic verdicts, token-level explainability, and actionable security recommendations.

---

## 🚀 Key Features

1. **Genuine Machine Learning Classification**:
   - Uses Scikit-learn with **TF-IDF Vectorization** (unigram and bigram n-grams, sublinear term-frequency scaling) and **calibrated Logistic Regression** with balanced class weights.
   - Evaluated on a strictly held-out test split, generating authentic probability distributions (`predict_proba`) and calibrated confidence scores.

2. **Granular Behavioral Explainability**:
   - Identifies specific smishing threat vectors:
     - **Urgency & Psychological Coercion** ("immediate action required", "account locked in 24h")
     - **Unsolicited Rewards & Fake Lotteries** ("winner", "claim $1,000 gift card")
     - **Credential & Identity Theft** ("verify password", "provide OTP/PIN")
     - **Impersonated Logistics / Delivery Services** ("USPS package pending customs fee")
     - **Predatory Financial / Crypto Schemes** ("guaranteed loan", "crypto trading VIP")
   - Structured categorized reasons explaining why a message was flagged or deemed normal.

3. **Interactive Suspicious Token Highlighting**:
   - The user's original message is visually inspected inline:
     - 🔴 **Red Badges** for high-risk tokens (e.g. *urgent*, *verify*, *suspended*, *jackpot*).
     - 🟡 **Amber Badges** for medium-risk pattern terms.
     - 🔵 **Cyan Badges** for embedded URLs with threat inspection.
     - Hover tooltips explain the reason for each highlighted token.

4. **External Link & Domain Threat Assessment**:
   - Identifies URLs, shortened links (`bit.ly`, `tinyurl`), raw IP addresses, and high-risk top-level domains (`.xyz`, `.top`, `.vip`, `.biz`).

5. **Detection History with SQLite Persistence**:
   - Logs message snippet, classification verdict, confidence %, and timestamp.
   - Includes "View Full Analysis" modal, individual deletion, and "Clear All" functionality.
   - Backed by an SQLite database (`data/spamshield.db`) and synchronized with browser `localStorage`.

6. **Cybersecurity & AI Themed UI**:
   - Professional **Dark and Light Theme** toggle with persistent preference.
   - Dark navy palette (`#070b14`), electric blue, and glowing cyan accents.
   - Glassmorphism cards, pulsing radar scanner animation during analysis, and responsive layouts across desktop, tablet, and mobile.
   - Preset test chips for 1-click evaluation of real-world scenarios.

7. **Transparent Machine Learning Metrics**:
   - Built-in "View Full ML Evaluation Report" modal displaying live test accuracy, precision, recall, F1-score, confusion matrix, and top vocabulary weights directly from the backend.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Flask 3.1, Flask-CORS
- **Machine Learning**: Scikit-learn 1.9, NumPy 2.5, Pandas 3.1, Joblib
- **Database**: SQLite 3 (built-in Python `sqlite3`)
- **Frontend**: HTML5, Modern CSS3 (CSS Variables, Flexbox/Grid, Glassmorphism), Vanilla JavaScript (ES6+)

---

## 📂 Project Directory Structure

```
spamshield-ai/
├── app.py                      # Flask REST API server and static file provider
├── analyzer.py                 # Core text processor, ML inference, and explainability engine
├── train_model.py              # Dataset builder, model training pipeline, and evaluation
├── db.py                       # SQLite database manager for history and contact messages
├── requirements.txt            # Python dependencies
├── data/
│   ├── spam_dataset.csv        # Comprehensive labeled dataset
│   └── spamshield.db           # SQLite database for history & feedback
├── models/
│   ├── spam_classifier.joblib  # Trained TF-IDF + Logistic Regression pipeline
│   └── model_metrics.json      # Saved test evaluation report & top feature weights
├── static/
│   ├── index.html              # Main single-page web application
│   ├── css/
│   │   └── style.css           # Glassmorphism dark/light CSS
│   └── js/
│       └── app.js              # Interactive client application logic
└── tests/
    └── test_detector.py        # Automated test suite covering all 10 core scenarios
```

---

## 📊 Model Evaluation Performance

Evaluated on a strictly held-out test split of 545 samples:

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **100.0%** |
| **Precision (Spam)** | **100.0%** |
| **Recall (Spam)** | **100.0%** |
| **F1-Score** | **100.0%** |
| **Inference Latency** | **< 35ms** |

### Confusion Matrix

```
                 Predicted Normal    Predicted Spam
Actual Normal          292 (TN)            0 (FP)
Actual Spam              0 (FN)          253 (TP)
```

---

## 🚀 Installation & Running the Application

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)
- `pip` package manager

### 2. Set Up Virtual Environment

```bash
cd C:\Users\lambu\.gemini\antigravity\scratch\spamshield-ai
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train Model (Optional — Pre-trained Model Included)

```bash
python train_model.py
```

### 5. Run the Automated Test Suite

```bash
python -m unittest discover tests
```

All 10 tests validate:
- Normal personal communication
- Promotional spam
- Prize and sweepstake scams
- Bank smishing alerts
- URL detection and threat analysis
- Numbers, symbols, and currency handling
- Emoji support
- Empty message validation
- Long message processing
- Mixed benign and suspicious language

### 6. Start the Web Server

```bash
python app.py
```

- **Public Live Application**: [https://veteran-approximately-referring-dee.trycloudflare.com/#detector](https://veteran-approximately-referring-dee.trycloudflare.com/#detector)
- **Interactive Presentation Deck**: [https://veteran-approximately-referring-dee.trycloudflare.com/presentation.html](https://veteran-approximately-referring-dee.trycloudflare.com/presentation.html)
- **Local Application**: [http://127.0.0.1:5000/#detector](http://127.0.0.1:5000/#detector)

---

## 🌐 API Reference

### 1. `POST /api/predict`
Analyzes message text and returns classification verdict, probabilities, reasons, and token highlights.

**Request Body:**
```json
{
  "message": "URGENT: Your debit card is suspended. Verify at https://chase-secure-update.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "prediction": "SPAM",
  "confidence": 94.2,
  "spam_probability": 94.2,
  "normal_probability": 5.8,
  "reasons": [
    "Urgency & Coercion Tactics: Uses artificial urgency or threats to pressure quick emotional reactions.",
    "Credential & Verification Harvesting: Attempts to elicit sensitive security credentials, OTPs, or identity documents.",
    "Contains 1 external URL(s), including potentially deceptive or unverified destinations.",
    "AI classifier calculated a 94.2% mathematical probability of spam intent."
  ],
  "recommendations": [
    "Do NOT click any links, open attachments, or download files from this message.",
    "Never disclose one-time passwords (OTP), banking PINs, or personal identity details.",
    "Verify legitimate claims by logging directly into the official website or mobile app.",
    "Block the sender and report the message to your service provider (forward to 7726)."
  ],
  "token_highlights": [
    { "text": "URGENT", "type": "suspicious_word", "risk": "high" },
    { "text": "https://chase-secure-update.com", "type": "suspicious_url", "risk": "high" }
  ],
  "history_id": 1
}
```

### 2. `GET /api/history`
Retrieves past analyzed records. Query param `limit` (default: 50).

### 3. `DELETE /api/history/<id>`
Deletes a specific history record.

### 4. `DELETE /api/history`
Clears all detection history records.

### 5. `GET /api/model-info`
Returns model metadata, performance metrics, confusion matrix, and top feature weights.

### 6. `GET /api/stats`
Returns aggregate statistics (total messages analyzed, spam count, normal count, average confidence).

### 7. `POST /api/contact`
Receives contact and feedback form submissions.

---

## 🔒 Security & Privacy Notice

- **No Remote Telemetry**: Messages are processed locally on the server instance.
- **Probabilistic Predictions**: As highlighted throughout the user interface, ML classifications are probabilistic evaluations and do not guarantee 100% security assessment. Users are advised to always exercise standard digital vigilance.
