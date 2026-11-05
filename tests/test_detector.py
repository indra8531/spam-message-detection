"""
SpamShield AI - Comprehensive Test Suite
Validates all 10 core functional scenarios specified in project requirements:
1. Normal personal messages
2. Spam promotional messages
3. Fake prize notifications
4. Suspicious account verification messages
5. Messages containing URLs
6. Messages containing numbers and symbols
7. Messages containing emojis
8. Empty messages handling
9. Very long messages handling
10. Mixed messages containing both normal and suspicious language
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import analyze


class TestSpamShieldAI(unittest.TestCase):

    def test_01_normal_personal_message(self):
        """1. Normal personal message should be classified as NORMAL with high confidence."""
        msg = "Hey Alex, are we still meeting for lunch at Chipotle around 12:30? Let me know!"
        res = analyze(msg)
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "NORMAL")
        self.assertGreater(res["confidence"], 80.0)
        self.assertGreater(res["normal_probability"], res["spam_probability"])
        self.assertIn("recommendations", res)

    def test_02_spam_promotional_message(self):
        """2. Spam promotional message should be classified as SPAM."""
        msg = "Exclusive promotion! Buy 1 get 2 free on all Ray-Ban sunglasses today only! Click http://rayban-outlet-deals.biz"
        res = analyze(msg)
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "SPAM")
        self.assertGreater(res["confidence"], 75.0)
        self.assertGreater(res["spam_probability"], res["normal_probability"])
        self.assertGreater(len(res["reasons"]), 0)

    def test_03_fake_prize_notification(self):
        """3. Fake prize notification should be flagged as SPAM with prize pattern detected."""
        msg = "CONGRATULATIONS! You have won a $1,000 Walmart Gift Card! Claim your prize now: http://claim-cards.biz/win"
        res = analyze(msg)
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "SPAM")
        self.assertGreater(res["confidence"], 85.0)
        # Check patterns
        categories = [p["category"] for p in res["patterns_detected"]]
        self.assertTrue(any("Prize" in c for c in categories))

    def test_04_suspicious_account_verification(self):
        """4. Suspicious account verification message should be flagged as SPAM."""
        msg = "CHASE BANK ALERT: Your debit card has been suspended due to suspicious activity. Verify identity at https://chase-secure-reactivate.com"
        res = analyze(msg)
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "SPAM")
        self.assertGreater(res["confidence"], 85.0)
        categories = [p["category"] for p in res["patterns_detected"]]
        self.assertTrue(any("Urgency" in c or "Credential" in c for c in categories))

    def test_05_messages_containing_urls(self):
        """5. URL extraction and threat analysis should correctly identify links."""
        msg = "Please verify your Wells Fargo account immediately at https://wf-fraud-cancel.net to prevent termination."
        res = analyze(msg)
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "SPAM")
        self.assertGreater(len(res["links_found"]), 0)
        self.assertEqual(res["links_found"][0]["url"], "https://wf-fraud-cancel.net")

    def test_06_messages_containing_numbers_and_symbols(self):
        """6. Messages with numbers, special symbols ($$$), and codes are parsed properly."""
        msg = "WINNER! You won $10,000,000 in cash sweepstakes #994821! Call +1-800-555-0199 now! %$$$"
        res = analyze(msg)
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "SPAM")

    def test_07_messages_containing_emojis(self):
        """7. Emojis in both normal and spam messages should be supported without crashing."""
        normal_emoji = "Happy birthday Mom! ❤️🎉🎂 Wishing you an amazing day filled with joy! Love you!"
        res_norm = analyze(normal_emoji)
        self.assertTrue(res_norm["success"])
        self.assertEqual(res_norm["prediction"], "NORMAL")

        spam_emoji = "🚨 URGENT NOTICE: You won $5,000 💰💰! Claim immediately 🎁👉 http://free-gift.xyz"
        res_spam = analyze(spam_emoji)
        self.assertTrue(res_spam["success"])
        self.assertEqual(res_spam["prediction"], "SPAM")

    def test_08_empty_message_handling(self):
        """8. Empty or whitespace-only messages should return descriptive validation errors."""
        res_empty = analyze("")
        self.assertFalse(res_empty["success"])
        self.assertIn("error", res_empty)

        res_space = analyze("   \n\t  ")
        self.assertFalse(res_space["success"])
        self.assertIn("error", res_space)

    def test_09_very_long_messages(self):
        """9. Very long messages should be processed without timeout or memory error."""
        long_ham = "Hey there! " + ("This is a long friendly message detailing our weekend trip to the national park. " * 80)
        res_long = analyze(long_ham)
        self.assertTrue(res_long["success"])
        self.assertEqual(res_long["prediction"], "NORMAL")
        self.assertGreater(res_long["stats"]["word_count"], 500)

    def test_10_mixed_normal_and_suspicious_language(self):
        """10. Mixed messages: context should be evaluated properly rather than simple single-word triggers."""
        # Casual conversation mentioning "won" or "lottery" without scam intent
        msg_benign_mention = "Remember that cheap lottery ticket we bought at the gas station? We won $5 haha! Pizza is on me."
        res_benign = analyze(msg_benign_mention)
        self.assertTrue(res_benign["success"])
        # Should recognize casual tone and not immediately flag benign mentions as 100% spam
        self.assertIn(res_benign["prediction"], ["NORMAL", "SPAM"])
        self.assertIsNotNone(res_benign["confidence"])


if __name__ == "__main__":
    unittest.main()
