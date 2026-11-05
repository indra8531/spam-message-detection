"""
SpamShield AI - Model Training Pipeline
Trains a Machine Learning Classifier for Spam vs Normal Message Detection.
Uses TF-IDF Vectorization and Logistic Regression / Multinomial Naive Bayes.
Evaluates on a held-out test dataset and exports the model and evaluation report.
"""

import os
import json
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import joblib

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DATASET_PATH = os.path.join(DATA_DIR, "spam_dataset.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "spam_classifier.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")


def clean_text(text: str) -> str:
    """Preprocess text for feature extraction while retaining semantic indicators."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Normalize URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' urltoken ', text)
    # Normalize phone numbers
    text = re.sub(r'\+?\d[\d -]{8,}\d', ' phonetoken ', text)
    # Normalize currency amounts
    text = re.sub(r'[\$£€₹]\s*\d+([,\.]\d+)?|\d+\s*(dollars|pounds|euro|cash|bucks)', ' currencytoken ', text)
    # Normalize excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def generate_curated_dataset() -> pd.DataFrame:
    """Generates a rich, diverse dataset of SMS and messaging spam & ham."""
    # Base spam message templates and variations
    spam_templates = [
        # Lottery & Prizes
        "CONGRATULATIONS! You've won a $1,000 Walmart Gift Card! Claim your prize now: http://claim-cards.biz/win",
        "You have been selected as the winner of our £1,000,000 cash sweepstakes. Call 08712400603 to claim prize.",
        "URGENT! You won a brand new iPhone 15 Pro Max! Click https://apple-reward-win.xyz/redeem within 24 hours.",
        "Final Notice: You have an unclaimed lottery jackpot of $50,000. Text WIN to 88202 to transfer funds.",
        "You have won a free 4-day Caribbean cruise vacation! Call 1-800-555-CRUISE today to confirm reservation.",
        "Free entry in 2 a weekly comp to win £1000 cash! Text MUSIC to 85222 to receive contest entry.",
        "Selected winner! You have 1 unclaimed gift waiting. Visit http://reward-hub.info now before it expires.",
        "Congratulations! Your mobile number was chosen for a $500 Amazon voucher. Click here: http://bit.ly/3x892a",
        "Prize Draw Alert: You are guaranteed £500 cash or an iPad. Call 09061701461 to claim your reward.",
        "WINNER! As a valued customer you are entitled to a $250 dining voucher. Reply CLAIM to receive.",

        # Banking, Financial & Smishing
        "CHASE BANK ALERT: Your debit card has been suspended due to suspicious activity. Verify identity at https://chase-secure-reactivate.com",
        "Wells Fargo Alert: A wire transfer of $1,450.00 is pending. If this was not you, visit https://wf-fraud-cancel.net",
        "Bank of America: Security alert. Unauthorized login attempt from Russia. Secure your account immediately: https://bofa-verify-user.info",
        "CITIBANK: Your account has been temporarily locked for security reasons. Click https://citi-id-verify.org to restore access.",
        "Security Alert: Your PayPal account has been limited due to unusual transactions. Update details here: https://paypal-account-resolve.top",
        "URGENT: Suspicious charge of $899.99 at Best Buy on your Visa card. Call fraud department immediately at 1-800-555-0199.",
        "Capital One Alert: Unusual activity detected on card ending 4019. Reply 1 if recognized, 2 to freeze account.",
        "Your Bank: Account #9102 has been flagged for fraud. Confirm your PIN and identity at http://bank-secure-login.xyz",
        "USPS ALERT: Your parcel #US948123 could not be delivered due to incomplete address. Pay $1.99 redelivery fee at https://usps-track-parcel.vip",
        "FedEx Notification: Your package delivery is on hold. Update delivery address here: http://fedex-update-package.co",
        "DHL Express: Package awaiting customs clearance. Outstanding fee of $3.50 required. Settle at http://dhl-express-duty.com",
        "UPS Delivery Notice: Driver unable to deliver package. Reschedule now at http://ups-parcel-reschedule.top to avoid return to sender.",

        # Impersonation & Security Codes
        "Your Google verification code is 739102. If you did not request this, someone has your password! Secure now at https://google-protect-id.net",
        "Apple Support: Your Apple ID was used to sign in to iCloud from an unrecognized device. Verify ownership: https://apple-id-locked-resolve.com",
        "Microsoft Account Team: Unusual sign-in detected. If this wasn't you, verify your credentials at https://ms-login-security.info",
        "WhatsApp Security: Your WhatsApp code is 492-192. Do not share this code. Enter code at http://wa-security-check.biz",
        "Instagram Alert: We detected copyright infringement on your profile. Submit dispute within 24h at https://ig-help-support.xyz or account deleted.",
        "Netflix Alert: Your membership payment failed. Update credit card information at http://netflix-billing-renew.com to keep streaming.",
        "IRS Notice: You have an unpaid tax penalty of $1,850. Legal action will begin unless paid immediately. Call 1-888-555-0144.",
        "Social Security Administration: Your SSN has been suspended due to fraudulent activity. Press 1 to speak with an officer.",
        "Toll Services: Unpaid toll invoice of $14.25 due today. Late enforcement fees apply. Pay immediately at https://ezpass-toll-settlement.com",

        # Crypto, Loans, Offers & Work from Home
        "Work from home! Earn $300 to $800 daily testing apps on your smartphone. Flexible hours, no experience. WhatsApp: +1-555-0182",
        "Guaranteed loan approved! Receive up to $15,000 cash in your account today with no credit check. Apply: http://fast-cash-loans.net",
        "Exclusive Bitcoin Alert: AI trading bot generated +420% profit this week! Join VIP Telegram free: https://t.me/crypto-signals-vip",
        "Hot singles in your area want to meet you tonight! View local profiles now: http://flirt-date-now.xyz/chat",
        "Lose 20lbs in 14 days with this secret keto miracle pill! Doctors hate this trick. Order risk-free: http://keto-fast-burn.biz",
        "Pre-approved credit card with $10,000 limit and 0% APR for 18 months! No annual fee. Claim card: http://credit-offer-direct.com",
        "Refinance your mortgage at historic low rates! Save $450/month. Check eligibility in 60 seconds: http://mortgage-save-now.org",
        "URGENT business proposal: I am legal counsel handling $12.5M estate with no heirs. Reply for 40% share: lawyer@offshore-trust.com",
        "You have 1 new voice message waiting from Unknown Caller. Listen to audio message: http://voice-mailbox-access.net/msg",
        "Earn passive income from Amazon automation! Guaranteed $5,000/month payout. Limited spots left. Sign up at http://ecom-wealth-club.co"
    ]

    # Base legitimate message templates and variations
    ham_templates = [
        # Casual personal chat
        "Hey! Are we still on for lunch at Chipotle around 12:30?",
        "Don't forget to pick up eggs, milk, and bread on your way back home from work.",
        "Just landed safely at JFK airport! Baggage claim is crazy, see you in 20 minutes.",
        "Happy birthday Mom! Wishing you an incredible day filled with love and happiness ❤️",
        "Can you send me the lecture slides from today's computer science class?",
        "That movie was absolutely incredible! The plot twist at the end blew my mind.",
        "Running about 10 minutes late due to traffic on the highway. Sorry about that!",
        "Thanks for helping me move the sofa yesterday, really appreciate your help bro!",
        "What time does the soccer practice start tomorrow morning?",
        "Are you free this weekend to go hiking at the national park?",
        "Let me know when you reach home so I know you're safe.",
        "The recipe you sent turned out amazing! Everyone in the family loved it.",
        "Could you check if I left my sunglasses on your dining table?",
        "Sounds like a great plan, I'll book the tickets for the 7 PM show tonight.",
        "Hey buddy, congratulations on passing your driving exam! Proud of you!",
        "Do you want me to bring anything for the barbecue party on Saturday?",
        "Just finished my workout at the gym. Heading home now for a quick shower.",
        "I'll be working from home on Wednesday, so let me know if you need to coordinate.",
        "Did you get a chance to review the draft I sent over email earlier today?",
        "Haha that dog video you sent was hilarious, literally made my day!",

        # Professional & Work
        "Hi team, please review the attached sprint retrospective notes before tomorrow's meeting.",
        "The client has approved the design mockups. We can commence the frontend integration.",
        "Please find the updated project schedule in our shared Google Drive folder.",
        "Could you please send over the invoice for the consultancy services provided last month?",
        "I will be out of the office on medical leave on Friday. Please contact Sarah for urgent matters.",
        "Great job on the presentation today, the board members were very impressed with the metrics.",
        "Let's schedule a 15-minute quick sync at 3 PM to align on the upcoming release checklist.",
        "Attached is the weekly status report for executive review. Feedback is welcome.",
        "The code review comments have been addressed in pull request #142. Ready for re-review.",
        "Reminder: All hands meeting is scheduled for Thursday at 11:00 AM in Conference Room B.",

        # Legitimate notifications & edge cases
        "Your Uber driver Alex is arriving in 3 minutes in a white Toyota Camry (License: 7ABC123).",
        "Appointment reminder: Your dental cleaning with Dr. Williams is scheduled for Oct 18 at 2:30 PM.",
        "Your Starbucks mobile order is ready for pickup at the counter. Thank you for your order!",
        "Library notification: The book 'Clean Code' you requested is now available for pickup.",
        "Your table for 4 at Bella Italia has been confirmed for tonight at 8:00 PM.",
        "School alert: School bus route 14 is running 15 minutes delayed due to weather conditions.",
        "Your flight DL 1842 to Chicago is boarding now at Gate B22.",
        "Your pharmacy prescription is ready for pickup at CVS on Main Street.",
        "Gym membership renewal confirmed. Your next billing date is November 1st.",
        "Your haircut appointment with Marcus is confirmed for Saturday at 11:30 AM."
    ]

    # Additional contextual variation generators
    variations_spam = [
        "ACTION REQUIRED: Your Netflix account is suspended. Verify billing details immediately: http://my-netflix-account-help.net",
        "Dear customer, you have 1 pending package at terminal 4. Settle clearance duty of $2.50 at http://delivery-customs-track.vip",
        "You are eligible for a COVID-19 relief subsidy of $1,200. Claim your disbursement at http://gov-aid-disbursement.org",
        "Bank Security: Debit card blocked. To unblock immediately visit http://bank-unblock-card.com or call customer support.",
        "Exclusive promotion! Buy 1 get 2 free on all Ray-Ban sunglasses today only! Click http://rayban-outlet-deals.biz",
        "Cash Prize winner! Text WIN to 77120 to receive your £250 voucher. T&Cs apply. 150p/msg.",
        "URGENT: Your PayPal has been accessed from an unknown IP in Nigeria. Login to lock account: http://paypal-dispute-center.org",
        "Wells Fargo: Transaction of $2,300 flagged. If unauthorized, cancel transaction at http://wellsfargo-cancel-payment.com",
        "Congratulations! You won free tickets to Taylor Swift concert! Click http://swiftie-ticket-draw.xyz to claim tickets.",
        "Your mobile bill is overdue by $87.50. Avoid line termination by paying at http://carrier-mobile-bill-pay.net now.",
        "Earn up to $500 daily evaluating products online. No experience needed. Start now: http://product-tester-jobs.biz",
        "Amazon: Unusual order placed for Sony PlayStation 5 ($499.99). If not you, report fraud to 1-800-555-0128 or http://amz-fraud-cancel.top",
        "Crypto giveaway! Elon Musk is giving away 500 BTC to celebrating Starship launch! Claim yours at http://tesla-btc-event.vip",
        "Your Apple ID is temporarily disabled. Visit http://appleid-support-unlock.com to verify your credentials.",
        "Important notification from Medicare: You are entitled to a new free back brace. Call 1-800-555-0149 to qualify.",
        "You have been pre-approved for an unsecured credit line of $25,000. Low interest. Apply at http://instant-credit-line.biz",
        "Urgent: Your Google cloud storage is full. Photos will be deleted in 48 hours unless upgraded: http://google-storage-upgrade.biz",
        "Final reminder: Your car warranty has expired. Speak to our specialist at 1-800-555-0199 to renew coverage.",
        "You have 3 unread messages from secret admirers in your neighborhood. See photos: http://local-dates-nearby.net",
        "Free $100 Target Gift Card opportunity! Complete this 2-minute survey to claim: http://target-surveys-win.org"
    ]

    variations_ham = [
        "Hey! Are you still at the library? Could you grab my notebook from the second floor table?",
        "I just sent over the draft for the quarterly marketing deck, let me know your thoughts when you have time.",
        "Dinner was so good tonight, thanks for cooking! We should try that pasta recipe again next week.",
        "Can you pick up Leo from soccer practice at 5:30? I'm stuck in an unexpected meeting at work.",
        "Happy anniversary guys! Hope you both have a fantastic evening celebrating ❤️",
        "Could you email me the contact details for the plumber you used last month?",
        "Don't worry about paying me back for the coffee, it's on me today!",
        "Flight got delayed by an hour due to runway congestion. Expected arrival is now 9:45 PM.",
        "Hey, do you know what chapters are going to be on the midterm exam next Tuesday?",
        "Just finished cleaning the apartment, looking forward to relaxing this evening.",
        "Thanks for referring me for the position! The HR recruiter reached out to schedule a phone screen.",
        "Are we meeting in room 302 or the main conference hall for the presentation?",
        "I found your keys by the front door shoe rack. I'll leave them on the kitchen island for you.",
        "Remember that funny video of the cat jumping into the box? I can't stop laughing at it 😂",
        "Heading out for a quick 5k run in the park, will call you once I'm back.",
        "Can you send the WiFi password for the guest network whenever you get a second?",
        "Doctor said everything looks completely normal, just need to drink more water and rest.",
        "Let's catch up over coffee this Thursday around 10 AM if your schedule permits.",
        "I'll bring the potato salad and some soda for tomorrow's picnic in the park.",
        "The package from mom just arrived safely! She sent homemade cookies and warm socks."
    ]

    # Combine into rich pools and generate parameterized variations
    all_spam = spam_templates + variations_spam
    all_ham = ham_templates + variations_ham

    # Generate additional realistic variations to reach ~2,400+ diverse samples
    extended_spam = []
    extended_ham = []

    # Multiply with contextual mutations (names, amounts, links, phrases)
    companies = ["Chase", "Bank of America", "Wells Fargo", "Citibank", "PayPal", "Amazon", "Apple", "Netflix", "USPS", "FedEx", "DHL"]
    amounts = ["$250", "$500", "$1,000", "$2,500", "$5,000", "$10,000", "£750", "£1,500"]
    domains = [".xyz", ".top", ".biz", ".info", ".vip", ".cc", ".club", ".link"]
    urgencies = ["URGENT", "IMMEDIATE ACTION REQUIRED", "FINAL NOTICE", "ALERT", "CRITICAL WARNING", "LAST CHANCE"]

    for i in range(1200):
        base = all_spam[i % len(all_spam)]
        comp = companies[i % len(companies)]
        amt = amounts[i % len(amounts)]
        dom = domains[i % len(domains)]
        urg = urgencies[i % len(urgencies)]

        if i % 4 == 0:
            var = f"{urg}: {comp} security notice. Unusual transaction of {amt} detected. Verify at http://{comp.lower().replace(' ', '')}-security{dom}/login"
        elif i % 4 == 1:
            var = f"Congratulations! You won {amt} cash prize in our mobile sweepstakes. Text WIN to {50000 + i} to claim prize immediately."
        elif i % 4 == 2:
            var = f"{comp} Package delivery notification: Unclaimed parcel pending customs payment of $2.{i % 99:02d}. Click http://track-package{dom}/update"
        else:
            var = f"{base} Ref ID: #{1000 + i}. Call 1-800-555-{i % 9000 + 1000:04d} or reply STOP to opt out."
        extended_spam.append(var)

    # Legitimate variations
    friend_names = ["Sarah", "Mike", "Jessica", "David", "Emma", "Daniel", "Rachel", "Alex", "Chris", "Emily"]
    times = ["12:00 PM", "1:30 PM", "3:45 PM", "5:00 PM", "6:30 PM", "7:15 PM", "8:00 PM"]
    places = ["the coffee shop", "Central Park", "the downtown library", "campus cafeteria", "the bookstore", "the gym"]
    tasks = ["review the slides", "prepare the report", "study for exams", "grab some dinner", "plan our trip", "finish the assignment"]

    for i in range(1400):
        base = all_ham[i % len(all_ham)]
        friend = friend_names[i % len(friend_names)]
        t = times[i % len(times)]
        p = places[i % len(places)]
        task = tasks[i % len(tasks)]

        if i % 4 == 0:
            var = f"Hey {friend}, are we still meeting at {p} at {t} to {task}?"
        elif i % 4 == 1:
            var = f"Hi {friend}, just wanted to check if you got my email regarding {task}. Let me know when free."
        elif i % 4 == 2:
            var = f"Thanks for the update {friend}! I'll be there around {t}. See you soon."
        else:
            var = f"{base} (Talk to you later {friend}!)"
        extended_ham.append(var)

    spam_data = [(msg, "spam") for msg in (all_spam + extended_spam)]
    ham_data = [(msg, "ham") for msg in (all_ham + extended_ham)]

    all_data = spam_data + ham_data
    df = pd.DataFrame(all_data, columns=["message", "label"])
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def train_and_evaluate_model():
    """Trains the ML model, generates metrics, and saves model artifacts."""
    print("=" * 60)
    print("SpamShield AI - Training Machine Learning Pipeline")
    print("=" * 60)

    # 1. Dataset Generation / Loading
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)

    print("Generating comprehensive labeled dataset...")
    df = generate_curated_dataset()
    df.to_csv(DATASET_PATH, index=False)
    print(f"Dataset saved to: {DATASET_PATH}")
    print(f"Total samples: {len(df)}")
    print(f"Class distribution:\n{df['label'].value_counts()}")

    # 2. Text Preprocessing
    print("\nPreprocessing messages...")
    df['cleaned_message'] = df['message'].apply(clean_text)

    # 3. Train/Test Split (80% Train, 20% Held-out Test)
    X = df['cleaned_message']
    y = df['label'].map({'ham': 0, 'spam': 1})

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\nTraining set size: {len(X_train)} samples")
    print(f"Test set size: {len(X_test)} samples (strictly held-out)")

    # 4. Feature Extraction & Classifier Pipeline
    # Using TF-IDF with unigrams & bigrams, sublinear tf scaling
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=8000,
            sublinear_tf=True,
            token_pattern=r'(?u)\b\w+\b'
        )),
        ('classifier', LogisticRegression(
            C=5.0,
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        ))
    ])

    print("\nTraining Logistic Regression with TF-IDF Vectorizer...")
    pipeline.fit(X_train, y_train)

    # 5. Model Evaluation on Test Split
    print("\nEvaluating model on strictly held-out test dataset...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    cm = confusion_matrix(y_test, y_pred).tolist()

    report_dict = classification_report(
        y_test, y_pred, target_names=["Normal (Ham)", "Spam"], output_dict=True
    )

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE REPORT (TEST DATASET)")
    print("=" * 60)
    print(f"Accuracy:  {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall:    {recall * 100:.2f}%")
    print(f"F1-Score:  {f1 * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(f"True Negatives: {cm[0][0]} | False Positives: {cm[0][1]}")
    print(f"False Negatives: {cm[1][0]} | True Positives: {cm[1][1]}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Normal (Ham)", "Spam"]))

    # Extract top spam-indicative features from model coefficients
    vectorizer = pipeline.named_steps['tfidf']
    classifier = pipeline.named_steps['classifier']
    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = classifier.coef_[0]

    top_spam_indices = np.argsort(coefs)[-25:][::-1]
    top_ham_indices = np.argsort(coefs)[:25]

    top_spam_words = [
        {"word": feature_names[i], "weight": round(float(coefs[i]), 3)}
        for i in top_spam_indices
    ]
    top_ham_words = [
        {"word": feature_names[i], "weight": round(float(-coefs[i]), 3)}
        for i in top_ham_indices
    ]

    # Save Model Artifacts
    print(f"\nSaving model pipeline to: {MODEL_PATH}")
    joblib.dump(pipeline, MODEL_PATH)

    metrics_data = {
        "model_name": "TF-IDF + Regularized Logistic Regression",
        "algorithm": "LogisticRegression (C=5.0, balanced class weights)",
        "vectorizer": "TF-IDF (1-2 ngrams, sublinear tf, 8000 max features)",
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "total_samples": int(len(df)),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {
            "tn": cm[0][0],
            "fp": cm[0][1],
            "fn": cm[1][0],
            "tp": cm[1][1]
        },
        "classification_report": report_dict,
        "top_spam_indicators": top_spam_words[:15],
        "top_normal_indicators": top_ham_words[:15],
        "vocabulary_size": len(feature_names)
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"Saved evaluation metrics to: {METRICS_PATH}")
    print("\nTraining complete successfully!")


if __name__ == "__main__":
    train_and_evaluate_model()
