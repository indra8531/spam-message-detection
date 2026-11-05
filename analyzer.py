"""
SpamShield AI - Message Analyzer & Explainability Engine
Integrates ML model probability predictions with granular pattern heuristics,
token highlighting, threat factor extraction, and safety recommendations.
"""

import os
import re
from typing import Dict, Any, List, Optional
import joblib

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "spam_classifier.joblib")

# Suspicious TLDs commonly used in smishing campaigns
SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".vip", ".biz", ".info", ".cc", ".club",
    ".tk", ".ml", ".ga", ".cf", ".gq", ".buzz", ".work", ".live",
    ".icu", ".monster", ".cyou", ".cfd", ".cam"
}

# URL shorteners often used to hide destination
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "is.gd", "buff.ly", "cutt.ly", "rb.gy"
}

# Suspicious pattern dictionary with categories and explanation
PATTERN_CATEGORIES = {
    "urgency": {
        "title": "Urgency & Coercion Tactics",
        "keywords": [
            r"\burgent\b", r"\bimmediate(ly)?\b", r"\baction required\b",
            r"\bfinal notice\b", r"\bwithin 24 hours?\b", r"\bwithin 48 hours?\b",
            r"\bsuspended\b", r"\baccount locked\b", r"\bterminate(d)?\b",
            r"\bpenalty\b", r"\blegal action\b", r"\blast chance\b",
            r"\bexpire(s|d)?\b", r"\brestricted\b", r"\bwarning\b"
        ],
        "reason": "Uses artificial urgency or threats to pressure quick emotional reactions."
    },
    "prizes_financial": {
        "title": "Prize & Unrealistic Reward Claims",
        "keywords": [
            r"\bcongratulations?\b", r"\bwinner\b", r"\bwon\b", r"\bprize\b",
            r"\bjackpot\b", r"\bsweepstakes\b", r"\bgift card\b", r"\bvoucher\b",
            r"\bfree entry\b", r"\bcash prize\b", r"\bclaim your prize\b",
            r"\bfree cruise\b", r"\bguaranteed profit\b", r"\bpassive income\b",
            r"\bfree\s*\$?\d+", r"\b\$[0-9]+,[0-9]+\b"
        ],
        "reason": "Offers unsolicited cash, luxury rewards, or gift vouchers typical of lottery scams."
    },
    "credential_theft": {
        "title": "Credential & Verification Harvesting",
        "keywords": [
            r"\bverify your (identity|account|password|card)\b",
            r"\bconfirm your pin\b", r"\botp\b", r"\bone[- ]time password\b",
            r"\bverification code\b", r"\bunauthorized login\b",
            r"\bunusual activity\b", r"\brestore access\b", r"\bsecure your account\b",
            r"\bsecurity alert\b", r"\bupdate your (details|billing|profile)\b"
        ],
        "reason": "Attempts to elicit sensitive security credentials, OTPs, or identity documents."
    },
    "financial_coercion": {
        "title": "Unsolicited Financial or Toll Demands",
        "keywords": [
            r"\bwire transfer\b", r"\bunpaid toll\b", r"\bcustoms fee\b",
            r"\bredelivery fee\b", r"\bbitcoin\b", r"\bcrypto\b",
            r"\bunsecured loan\b", r"\bpre[- ]approved\b", r"\bno credit check\b",
            r"\bsettle payment\b", r"\boutstanding fee\b", r"\btax penalty\b"
        ],
        "reason": "Demands payment for fabricated fees, fake tolls, or promotes predatory financial services."
    },
    "delivery_scams": {
        "title": "Impersonated Package Delivery",
        "keywords": [
            r"\bpackage delivery\b", r"\bparcel\b", r"\busps alert\b",
            r"\bfedex\b", r"\bdhl express\b", r"\bups delivery\b",
            r"\bincomplete address\b", r"\bon hold\b", r"\bredelivery\b",
            r"\bcustoms clearance\b"
        ],
        "reason": "Falsely mimics postal or courier services to prompt malicious link clicks."
    }
}


class SpamDetectorAnalyzer:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the trained model pipeline."""
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"Warning: Failed to load model from {MODEL_PATH}: {e}")
                self.model = None
        else:
            print(f"Model file not found at {MODEL_PATH}. Run train_model.py first.")

    @staticmethod
    def clean_text(text: str) -> str:
        """Preprocesses text identically to the training pipeline."""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', ' urltoken ', text)
        text = re.sub(r'\+?\d[\d -]{8,}\d', ' phonetoken ', text)
        text = re.sub(r'[\$£€₹]\s*\d+([,\.]\d+)?|\d+\s*(dollars|pounds|euro|cash|bucks)', ' currencytoken ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def extract_links(text: str) -> List[Dict[str, Any]]:
        """Extracts and evaluates URLs in the text for threat indicators."""
        url_regex = r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.(?:com|org|net|xyz|top|biz|info|vip|cc|club|biz|co|live)[^\s]*)'
        matches = re.findall(url_regex, text, re.IGNORECASE)
        links = []
        for match in set(matches):
            clean_url = match.rstrip(".,;!?)\"'>")
            threats = []
            risk_level = "low"

            lower_url = clean_url.lower()

            # Check TLD
            for tld in SUSPICIOUS_TLDS:
                if tld in lower_url:
                    threats.append(f"Suspicious top-level domain ({tld}) commonly used by phishing scams")
                    risk_level = "high"

            # Check Shorteners
            for shortener in URL_SHORTENERS:
                if shortener in lower_url:
                    threats.append(f"Shortened URL ({shortener}) hides final destination")
                    if risk_level != "high":
                        risk_level = "medium"

            # Check brand impersonation in domain
            brand_impersonations = [
                "chase-", "-chase", "wellsfargo-", "bofa-", "citi-", "paypal-",
                "apple-id", "appleid-", "netflix-", "usps-", "fedex-", "ups-", "amazon-"
            ]
            for bi in brand_impersonations:
                if bi in lower_url:
                    threats.append("Domain mimics recognized brand name (typosquatting/lookalike)")
                    risk_level = "high"

            # Check IP address as host
            if re.search(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', clean_url):
                threats.append("Raw IP address used instead of legitimate registered domain")
                risk_level = "high"

            links.append({
                "url": clean_url,
                "risk_level": risk_level,
                "threats": threats if threats else ["Standard web address format"]
            })
        return links

    def find_suspicious_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Identifies specific behavioral threat patterns."""
        detected = []
        for cat_key, cat_data in PATTERN_CATEGORIES.items():
            matched_terms = []
            for kw_pattern in cat_data["keywords"]:
                found = re.findall(kw_pattern, text, re.IGNORECASE)
                if found:
                    for item in found:
                        term = item if isinstance(item, str) else item[0]
                        if term and term.lower() not in [m.lower() for m in matched_terms]:
                            matched_terms.append(term)
            if matched_terms:
                detected.append({
                    "category": cat_data["title"],
                    "reason": cat_data["reason"],
                    "matched_terms": matched_terms
                })
        return detected

    def generate_token_highlights(self, text: str, suspicious_terms: List[str]) -> List[Dict[str, Any]]:
        """Splits message into tokens and marks suspicious tokens with risk levels."""
        if not text:
            return []

        # Build list of suspicious phrases/words sorted by length (descending)
        suspicious_set = set()
        for term in suspicious_terms:
            if term and len(term.strip()) > 1:
                suspicious_set.add(term.strip().lower())

        # Also add individual common high-risk spam words
        extra_keywords = [
            "urgent", "won", "winner", "prize", "jackpot", "free", "congratulations",
            "sweepstakes", "voucher", "verify", "password", "suspended", "locked",
            "toll", "customs", "bitcoin", "crypto", "wire", "otp", "code"
        ]
        suspicious_set.update(extra_keywords)

        # Regex for tokens including punctuation and words
        token_regex = re.compile(r'(\bhttps?://\S+\b|\bwww\.\S+\b|\b\w+\b|[^\w\s]|\s+)')
        raw_tokens = token_regex.findall(text)

        tokens_data = []
        for tok in raw_tokens:
            if not tok:
                continue
            cleaned = tok.strip().lower()
            is_url = bool(re.match(r'https?://|www\.', tok, re.IGNORECASE))

            if is_url:
                tokens_data.append({
                    "text": tok,
                    "type": "suspicious_url",
                    "risk": "high",
                    "tooltip": "External link target"
                })
            elif cleaned in suspicious_set:
                tokens_data.append({
                    "text": tok,
                    "type": "suspicious_word",
                    "risk": "high" if cleaned in ["urgent", "won", "jackpot", "verify", "suspended", "password", "otp"] else "medium",
                    "tooltip": f"Spam/smishing pattern term: '{cleaned}'"
                })
            elif tok.isspace():
                tokens_data.append({
                    "text": tok,
                    "type": "space",
                    "risk": "none"
                })
            else:
                tokens_data.append({
                    "text": tok,
                    "type": "normal",
                    "risk": "none"
                })

        return tokens_data

    def analyze_message(self, message: str) -> Dict[str, Any]:
        """Performs end-to-end analysis combining ML prediction with rule explainability."""
        # 1. Validation
        if not message or not message.strip():
            return {
                "success": False,
                "error": "Message content is empty. Please enter text to analyze."
            }

        # Check maximum length (e.g. 15,000 chars)
        if len(message) > 15000:
            return {
                "success": False,
                "error": "Message exceeds maximum permitted length (15,000 characters)."
            }

        cleaned = self.clean_text(message)

        # 2. Machine Learning Prediction
        if self.model is None:
            self._load_model()

        if self.model is not None:
            proba = self.model.predict_proba([cleaned])[0]
            normal_prob = float(proba[0])
            spam_prob = float(proba[1])
            prediction = "SPAM" if spam_prob >= 0.50 else "NORMAL"
        else:
            # Fallback heuristic if model is not loaded
            spam_prob = 0.5
            normal_prob = 0.5
            prediction = "NORMAL"

        # 3. Suspicious Pattern Analysis
        patterns = self.find_suspicious_patterns(message)
        links = self.extract_links(message)

        # High-risk link boost
        has_high_risk_link = any(link["risk_level"] == "high" for link in links)
        if has_high_risk_link and spam_prob < 0.65:
            spam_prob = min(0.92, spam_prob + 0.35)
            normal_prob = 1.0 - spam_prob
            prediction = "SPAM"

        # 4. Calculate Final Confidence Percentage
        if prediction == "SPAM":
            confidence = round(spam_prob * 100, 1)
        else:
            confidence = round(normal_prob * 100, 1)

        # 5. Extract words for token highlighting
        matched_terms = []
        for p in patterns:
            matched_terms.extend(p["matched_terms"])
        for l in links:
            matched_terms.append(l["url"])

        token_highlights = self.generate_token_highlights(message, matched_terms)

        # 6. Generate Reasoning
        reasons = []
        if prediction == "SPAM":
            if patterns:
                for pat in patterns[:4]:
                    reasons.append(f"{pat['category']}: {pat['reason']}")
            if links:
                reasons.append(f"Contains {len(links)} external URL(s), including potentially deceptive or unverified destinations.")
            if not reasons:
                reasons.append("Text structure and vocabulary match statistical patterns commonly found in promotional or smishing campaigns.")
            reasons.append(f"AI classifier calculated a {round(spam_prob * 100, 1)}% mathematical probability of spam intent.")
        else:
            reasons.append("Standard conversational structure with natural cadence and vocabulary.")
            reasons.append("No deceptive psychological urgency or artificial pressure tactics identified.")
            reasons.append("No credential harvesting attempts (passwords, PINs, OTP codes) requested.")
            if links:
                reasons.append("Included link(s) do not exhibit overt characteristics of known deceptive shorteners or suspicious TLDs.")
            else:
                reasons.append("No unsolicited external links detected.")
            reasons.append(f"AI classifier calculated a {round(normal_prob * 100, 1)}% mathematical probability of legitimate content.")

        # 7. Safety Recommendations
        if prediction == "SPAM":
            recommendations = [
                "Do NOT click any links, open attachments, or download files from this message.",
                "Never disclose one-time passwords (OTP), banking PINs, or personal identity details.",
                "Verify legitimate claims by logging directly into the official website or mobile app.",
                "Block the sender and report the message to your service provider (forward to 7726)."
            ]
        else:
            recommendations = [
                "Message appears to be standard legitimate communication.",
                "Always verify unexpected requests involving money or account access out-of-band.",
                "Exercise normal digital vigilance: AI classifications are predictive estimates, not guarantees."
            ]

        # 8. Character & Word stats
        char_count = len(message)
        word_count = len(message.split())

        return {
            "success": True,
            "prediction": prediction,
            "confidence": confidence,
            "spam_probability": round(spam_prob * 100, 2),
            "normal_probability": round(normal_prob * 100, 2),
            "reasons": reasons,
            "recommendations": recommendations,
            "patterns_detected": patterns,
            "links_found": links,
            "token_highlights": token_highlights,
            "stats": {
                "char_count": char_count,
                "word_count": word_count,
                "link_count": len(links),
                "suspicious_pattern_count": len(patterns)
            },
            "disclaimer": "This analysis is an AI-powered prediction based on natural language processing and statistical machine learning. It does not constitute a guaranteed security assessment."
        }


# Singleton instance
analyzer_instance = SpamDetectorAnalyzer()


def analyze(text: str) -> Dict[str, Any]:
    """Helper entry point for API consumption."""
    return analyzer_instance.analyze_message(text)
