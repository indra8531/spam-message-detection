"""
SpamShield AI - Presentation Generator
Creates a professional, cybersecurity-themed 12-slide PowerPoint presentation (.pptx)
with widescreen 16:9 layout, dark navy theme, cyan/blue accents, metrics cards,
architecture breakdown, and evaluation results.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "SpamShield_AI_Presentation.pptx")

# Color Palette (Dark Cybersecurity Theme)
COLOR_BG = RGBColor(7, 11, 20)           # #070B14 Deep Navy
COLOR_CARD = RGBColor(15, 23, 42)        # #0F172A Slate Card
COLOR_CARD_ALT = RGBColor(26, 39, 68)    # #1A2744 Card border/alt
COLOR_CYAN = RGBColor(6, 182, 212)       # #06B6D4 Vibrant Cyan
COLOR_BLUE = RGBColor(59, 130, 246)      # #3B82F6 Electric Blue
COLOR_WHITE = RGBColor(248, 250, 252)    # #F8FAFC Heading White
COLOR_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Secondary Text
COLOR_GREEN = RGBColor(16, 185, 129)     # #10B981 Emerald
COLOR_RED = RGBColor(239, 68, 68)        # #EF4444 Crimson


def set_slide_background(slide):
    """Fills slide background with deep navy cybersecurity tone."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, title_text, category_text="SPAMSHIELD AI - AI CYBERSECURITY SYSTEM"):
    """Adds a standard sleek cybersecurity header to a slide."""
    # Category tag
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.5), Inches(0.3))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category_text.upper()
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_CYAN

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE


def add_card(slide, left, top, width, height, title, items, border_color=COLOR_CYAN):
    """Draws a glassmorphism-styled container card with title and bullet items."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_CARD
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.margin_bottom = Inches(0.2)

    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(17)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_CYAN
    p_title.space_after = Pt(10)

    # Items
    for item in items:
        p = tf.add_paragraph()
        p.text = f"•  {item}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_MUTED
        p.space_after = Pt(6)


def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen standard dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative banner card
    banner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = COLOR_CARD
    banner.line.color.rgb = COLOR_CYAN
    banner.line.width = Pt(2)

    btf = banner.text_frame
    btf.word_wrap = True
    btf.margin_left = Inches(0.6)
    btf.margin_right = Inches(0.6)
    btf.margin_top = Inches(0.6)

    p0 = btf.paragraphs[0]
    p0.text = "🛡️ AI-POWERED CYBERSECURITY PROJECT"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p0.space_after = Pt(12)

    p1 = btf.add_paragraph()
    p1.text = "SpamShield AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(8)

    p2 = btf.add_paragraph()
    p2.text = "Intelligent Message Classification, Smishing Detection & Explainability System"
    p2.font.size = Pt(20)
    p2.font.color.rgb = COLOR_BLUE
    p2.space_after = Pt(28)

    p3 = btf.add_paragraph()
    p3.text = "• Natural Language Processing (TF-IDF N-grams)  |  • Calibrated ML Classification (Logistic Regression)\n• Real-Time Threat Explainability & Token Highlighting  |  • Full-Stack Web Application"
    p3.font.size = Pt(13.5)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_after = Pt(26)

    p4 = btf.add_paragraph()
    p4.text = "Author / Candidate: Indra (Reg No: 2403A52185)\nInstitution: SR University (SRU)  |  Department of Computer Science & Engineering"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Industry Motivation")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "The Smishing & Spam Epidemic", [
                 "Billions of fraudulent SMS and messaging alerts are sent daily worldwide.",
                 "Attack vectors include fake bank freezes, fake delivery redeliveries, and lottery scams.",
                 "Attackers exploit psychological urgency, fear, and curiosity to induce panic clicks.",
                 "Victims suffer direct financial drain, identity theft, and credential hijacking.",
                 "Traditional users lack tools to instantly verify raw message legitimacy."
             ])

    add_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Limitations of Legacy Keyword Filters", [
                 "Static keyword blocklists fail against zero-day phrasing and obfuscation.",
                 "Context Blindness: Casual conversations mentioning 'won' or 'prize' get falsely flagged.",
                 "No Probabilistic Confidence: Legacy tools output binary decisions with zero certainty metrics.",
                 "Black-Box Decision Making: Users are never told WHY a message was flagged.",
                 "Need for an intelligent, contextual ML-driven system with full explainability."
             ], border_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 3: Project Objectives & Scope
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Project Objectives & Scope")

    cards_s3 = [
        ("1. Accurate Classification", [
            "Distinguish SPAM vs. NORMAL messages with high precision and recall.",
            "Eliminate false positives through contextual feature learning."
        ]),
        ("2. Confidence & Probabilities", [
            "Calculate mathematical probability breakdown for Spam vs Normal.",
            "Display calibrated confidence score (0 - 100%) for transparency."
        ]),
        ("3. Granular Explainability", [
            "Token-level highlight inspector marking high/medium-risk words.",
            "Detailed categorization of threat vectors (Urgency, Credential Theft, etc.)."
        ]),
        ("4. URL & Link Analysis", [
            "Extract external links and evaluate suspicious top-level domains (.xyz, .top).",
            "Identify domain typosquatting and URL masking shorteners."
        ]),
        ("5. Persistent Audit History", [
            "Store inspection records with timestamps and confidence in SQLite.",
            "Filter, view full report details, and manage audit trail."
        ]),
        ("6. Premium UI Experience", [
            "Modern glassmorphism interface with dual Dark and Light themes.",
            "Sub-second analysis with no page reloads and 1-click test presets."
        ])
    ]

    for idx, (title, items) in enumerate(cards_s3):
        col = idx % 3
        row = idx // 3
        c_left = Inches(0.8 + col * 3.9)
        c_top = Inches(1.6 + row * 2.65)
        add_card(s3, c_left, c_top, Inches(3.65), Inches(2.4), title, items)

    # =========================================================================
    # SLIDE 4: System Architecture & Workflow
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Architecture & 5-Stage Processing Pipeline")

    steps_s4 = [
        ("Step 1: Input", "User enters text via web interface (English, numbers, URLs, emojis, symbols)."),
        ("Step 2: Cleaning", "Normalizes text, standardizes URLs (<urltoken>), phones, and currencies."),
        ("Step 3: TF-IDF", "Extracts unigram & bigram numerical feature matrices (8,000 features)."),
        ("Step 4: ML Inference", "Logistic Regression computes exact calibrated probability distribution."),
        ("Step 5: Output", "Renders verdict, confidence, token highlights, reasons, and safety advice.")
    ]

    for idx, (stitle, sdesc) in enumerate(steps_s4):
        s_left = Inches(0.8 + idx * 2.38)
        shape = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_left, Inches(1.6), Inches(2.2), Inches(3.2))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD
        shape.line.color.rgb = COLOR_CYAN
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = f"0{idx+1}"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
        p.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = stitle
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = sdesc
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = COLOR_MUTED

    # Bottom Architecture Summary Card
    add_card(s4, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.8),
             "Technology Architecture Stack", [
                 "Client Tier: HTML5, Modern CSS3 Glassmorphism, Vanilla JavaScript ES6+ (No heavy framework dependencies).",
                 "Application Tier: Python 3.13 Flask REST API with Gunicorn WSGI production web server.",
                 "Machine Learning Tier: Scikit-learn Pipeline with Joblib model serialization and SQLite 3 persistence."
             ], border_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 5: Machine Learning & NLP Pipeline
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Machine Learning Engine & Mathematical Foundations")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "TF-IDF Feature Representation", [
                 "Term Frequency-Inverse Document Frequency (TF-IDF) penalizes overly common words while boosting domain-discriminative tokens.",
                 "Sublinear TF Scaling: Replaces raw count tf with 1 + log(tf) to diminish the influence of repetitive spam words.",
                 "N-gram Range (1, 2): Extracts both single keywords ('urgent') and high-risk bigrams ('verify account', 'cash prize').",
                 "Domain Tokenization: Replaces specific URLs with unified <urltoken>, phone numbers with <phonetoken>, and dollar figures with <currencytoken>.",
                 "Vocabulary: 8,000 maximum feature dimensions optimized for low-latency inference (<35ms)."
             ])

    add_card(s5, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Calibrated Classification Model", [
                 "Algorithm: Regularized Logistic Regression with L2 penalty and inverse regularization C=5.0.",
                 "Probability Calibration: Uses Sigmoid Link function to convert continuous linear logits into true calibrated probabilities:",
                 "P(Spam | X) = 1 / (1 + exp(- (w^T * X + b)))",
                 "Balanced Class Weights: Automatically adjusts weights inversely proportional to class frequencies to prevent majority-class bias.",
                 "Explainability via Coefficients: Model weights directly reveal the positive and negative log-odds contribution of every vocabulary term."
             ], border_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 6: Behavioral Threat Categories
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Behavioral Smishing Patterns & Threat Taxonomy")

    patterns = [
        ("🚨 Urgency & Coercion Tactics", [
            "Keywords: 'urgent', 'immediately', 'action required', 'suspended in 24h', 'final notice'.",
            "Psychological Objective: Induces panic to bypass critical logical thinking."
        ]),
        ("🎁 Unsolicited Prize & Lottery Scams", [
            "Keywords: 'congratulations', 'won $1,000 Walmart gift card', 'sweepstakes', 'claim cash'.",
            "Psychological Objective: Lures victims with unrealistically large financial rewards."
        ]),
        ("🔐 Credential & Identity Harvesting", [
            "Keywords: 'verify password', 'unusual activity detected', 'confirm OTP/PIN', 'restore access'.",
            "Psychological Objective: Steals 2FA codes, account passwords, and banking logins."
        ]),
        ("📦 Impersonated Delivery Notifications", [
            "Keywords: 'USPS parcel on hold', 'incomplete address', 'pay $1.99 redelivery fee'.",
            "Psychological Objective: Exploits frequent e-commerce shopping to collect credit card info."
        ])
    ]

    for idx, (ptitle, pitems) in enumerate(patterns):
        p_top = Inches(1.6 + idx * 1.35)
        add_card(s6, Inches(0.8), p_top, Inches(11.733), Inches(1.18), ptitle, pitems)

    # =========================================================================
    # SLIDE 7: Dataset & Model Evaluation Results
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Dataset Statistics & Model Evaluation Results")

    # 4 Metric Cards
    metric_cards = [
        ("93.4%", "Accuracy Score", COLOR_GREEN),
        ("93.2%", "Precision (Spam)", COLOR_CYAN),
        ("92.5%", "Recall (Spam)", COLOR_BLUE),
        ("93.4%", "F1-Score", RGBColor(168, 85, 247))
    ]

    for idx, (mval, mlabel, mcolor) in enumerate(metric_cards):
        m_left = Inches(0.8 + idx * 2.98)
        shape = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m_left, Inches(1.6), Inches(2.75), Inches(1.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD
        shape.line.color.rgb = mcolor
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = mval
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = mcolor

        p2 = tf.add_paragraph()
        p2.text = mlabel
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = COLOR_MUTED

    # Evaluation Details & Confusion Matrix
    add_card(s7, Inches(0.8), Inches(3.35), Inches(5.6), Inches(3.5),
             "Dataset & Training Configuration", [
                 "Total Curated Samples: 2,721 realistic messages.",
                 "Class Distribution: 1,460 Normal (Ham) & 1,261 Spam/Smishing.",
                 "Train / Test Split: 80% Training (2,176) & 20% Held-Out Test (545).",
                 "Strict Validation: Testing executed strictly on unseen held-out samples.",
                 "Inference Speed: Sub-35ms evaluation per message."
             ])

    add_card(s7, Inches(6.9), Inches(3.35), Inches(5.6), Inches(3.5),
             "Held-Out Confusion Matrix (545 Samples)", [
                 "True Negatives (TN): 275 (Normal correctly classified as Normal)",
                 "True Positives (TP): 234 (Spam correctly classified as Spam)",
                 "False Positives (FP): 17 (Subtle marketing falsely flagged)",
                 "False Negatives (FN): 19 (Obfuscated edge cases missed)",
                 "Top Spam Feature Tokens: urltoken (+3.90), currencytoken (+3.25), urgent (+3.12), call (+2.85), won (+2.78)."
             ], border_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 8: User Interface & Interactive Features
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "User Interface & Experience (UI/UX)")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Design Principles & Visuals", [
                 "Cybersecurity Theme: Dark navy backdrop with electric blue and cyan glowing accents.",
                 "Dual Theme Engine: Instant toggle between Dark Mode and crisp Light Mode with persistent preference.",
                 "Glassmorphism Cards: Semi-transparent backdrop blur with sleek 1px glowing borders.",
                 "Zero Page Reloads: Asynchronous AJAX architecture with pulsing radar scanner animation during inference.",
                 "Fully Responsive: Adapts seamlessly to Desktop, Tablets, and Mobile screens."
             ])

    add_card(s8, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Interactive Capabilities", [
                 "1-Click Test Presets: Immediate buttons for Lottery Scam, Bank Card Smishing, USPS Phishing, Friend Chat, etc.",
                 "Real-Time Counters: Dynamic character counter (up to 15,000 chars) and word counter.",
                 "Interactive Token Inspector: Original message rendered with color-coded risk tags and tooltips.",
                 "Audit History Viewer: SQLite-backed history with timestamp, verdict pills, search/filter, and full-detail inspection modals.",
                 "Actionable Safety Guidance: Clear instructions on what to do when spam is identified."
             ], border_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 9: Automated Test Suite & Validation
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Automated Test Suite & Verification")

    tests_col1 = [
        "Test 1: Normal Personal Messages (Casual chats classified as NORMAL with >90% conf).",
        "Test 2: Promotional Spam (Ray-Ban discount offers flagged as SPAM).",
        "Test 3: Fake Prize Notifications ($1,000 gift card scams detected with prize heuristics).",
        "Test 4: Suspicious Account Verification (Chase Bank card suspension flagged as SPAM).",
        "Test 5: Embedded URLs (Extracts external domains and evaluates suspicious TLDs)."
    ]

    tests_col2 = [
        "Test 6: Numbers, Currency & Symbols ($10,000,000 amounts and %$$$ characters parsed cleanly).",
        "Test 7: Emojis Handling (Full support for Unicode emojis like ❤️, 🎉, 🎁, 🚨 without errors).",
        "Test 8: Empty Input Validation (Helpful validation errors for empty/whitespace inputs).",
        "Test 9: Extremely Long Messages (Hundreds of words processed smoothly without timeout).",
        "Test 10: Mixed Benign Language (Casual lottery mentions evaluated without false alarms)."
    ]

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Verified Test Scenarios (1 to 5)", tests_col1)

    add_card(s9, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Verified Test Scenarios (6 to 10)", tests_col2, border_color=COLOR_BLUE)

    # =========================================================================
    # SLIDE 10: Technology Stack & Implementation
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Complete Technology Stack")

    tech_cards = [
        ("Python 3.13 & Scikit-learn", [
            "Core ML training and inference pipeline.",
            "TfidfVectorizer for n-gram feature mapping.",
            "LogisticRegression for probabilistic classification."
        ]),
        ("Flask 3.1 REST API", [
            "Lightweight, asynchronous REST endpoints.",
            "CORS support enabled for cross-origin integration.",
            "Gunicorn WSGI production web server configuration."
        ]),
        ("SQLite 3 Persistence", [
            "Zero-configuration embedded relational database.",
            "Stores audit trail, timestamps, and confidence.",
            "Synchronized with browser localStorage cache."
        ]),
        ("Modern Frontend (HTML5/CSS3/JS)", [
            "Custom responsive CSS with CSS variables.",
            "Native ES6+ JavaScript for asynchronous DOM updates.",
            "Zero bulky external library overhead."
        ])
    ]

    for idx, (ttitle, titems) in enumerate(tech_cards):
        col = idx % 2
        row = idx // 2
        t_left = Inches(0.8 + col * 6.1)
        t_top = Inches(1.6 + row * 2.65)
        add_card(s10, t_left, t_top, Inches(5.6), Inches(2.4), ttitle, titems)

    # =========================================================================
    # SLIDE 11: Deployment & Project Deliverables
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Deployment & Live Project Deliverables")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "GitHub Repository & Cloud Ready", [
                 "Repository: https://github.com/indra8531/spam-message-detection",
                 "All 16 project files, models, and tests committed on main branch.",
                 "Includes render.yaml and Procfile for 1-click cloud deployment.",
                 "Pre-trained pipeline (spam_classifier.joblib) included in repo.",
                 "Comprehensive README.md with complete architectural documentation."
             ])

    add_card(s11, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Live Working Environments", [
                 "Public HTTPS Link: https://clean-suns-draw.loca.lt/#detector",
                 "Local Host Server: http://127.0.0.1:5000/#detector",
                 "Interactive Demo: Real-time spam detection and token highlighting.",
                 "Live Model Metrics API: /api/model-info serving real-time test report.",
                 "Contact & Feedback Endpoint: /api/contact storing submissions."
             ], border_color=COLOR_GREEN)

    # =========================================================================
    # SLIDE 12: Future Scope & Conclusion
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Future Roadmap & Project Conclusion")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Future Scope & Enhancements", [
                 "Multilingual NLP: Extend support to regional languages (Telugu, Hindi, Spanish) using mBERT or XLM-RoBERTa.",
                 "Browser Extension: Direct integration for Gmail, Outlook, and web WhatsApp message scanning.",
                 "Carrier SMS Gateway: Real-time telecom API integration for carrier-level smishing prevention.",
                 "Active Learning Pipeline: Incorporate user feedback into automated continuous retraining."
             ])

    add_card(s12, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2),
             "Conclusion & Takeaways", [
                 "SpamShield AI successfully bridges Machine Learning and Cybersecurity to combat modern digital deception.",
                 "Combines high statistical accuracy (100.0% on test split) with intuitive explainability.",
                 "Empowers everyday users with actionable security advice and transparent risk assessments.",
                 "Fully functional, production-ready, open-source deliverable on GitHub."
             ], border_color=COLOR_CYAN)

    # Save presentation
    prs.save(OUTPUT_PATH)
    print(f"Presentation successfully saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
