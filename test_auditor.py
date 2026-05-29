import unittest
from auditor import score_password, get_strength_label

class TestScorePassword(unittest.TestCase):

    # --- Length scoring ---

    def test_very_short_password_scores_low(self):
        score, feedback = score_password("abc")
        self.assertLess(score, 40)
        self.assertTrue(any("short" in f.lower() for f in feedback))

    def test_8_char_password_gets_partial_length_score(self):
        score, _ = score_password("abcdefgh")
        self.assertGreaterEqual(score, 10)

    def test_12_char_password_gets_medium_length_score(self):
        score, _ = score_password("abcdefghijkl")
        self.assertGreaterEqual(score, 20)

    def test_16_char_password_gets_full_length_score(self):
        score, _ = score_password("abcdefghijklmnop")
        self.assertGreaterEqual(score, 30)

    # --- Complexity scoring ---

    def test_uppercase_adds_score(self):
        score_with, _ = score_password("Password")
        score_without, _ = score_password("password")
        self.assertGreater(score_with, score_without)

    def test_missing_uppercase_gives_feedback(self):
        _, feedback = score_password("password1!")
        self.assertTrue(any("uppercase" in f.lower() for f in feedback))

    def test_lowercase_adds_score(self):
        score_with, _ = score_password("Password")
        score_without, _ = score_password("PASSWORD")
        self.assertGreater(score_with, score_without)

    def test_missing_lowercase_gives_feedback(self):
        _, feedback = score_password("PASSWORD1!")
        self.assertTrue(any("lowercase" in f.lower() for f in feedback))

    def test_digits_add_score(self):
        score_with, _ = score_password("Password1")
        score_without, _ = score_password("Passworda")
        self.assertGreater(score_with, score_without)

    def test_missing_digits_gives_feedback(self):
        _, feedback = score_password("Password!")
        self.assertTrue(any("number" in f.lower() for f in feedback))

    def test_special_chars_add_score(self):
        score_with, _ = score_password("Password1!")
        score_without, _ = score_password("Password1a")
        self.assertGreater(score_with, score_without)

    def test_missing_special_chars_gives_feedback(self):
        _, feedback = score_password("Password1")
        self.assertTrue(any("special" in f.lower() for f in feedback))

    # --- Full-featured passwords ---

    def test_strong_password_scores_high(self):
        score, feedback = score_password("Tr0ub4dor&3!XyZ#")
        self.assertGreaterEqual(score, 80)
        self.assertEqual(feedback, [])

    def test_all_criteria_met_no_feedback(self):
        _, feedback = score_password("C0mpl3x!Pass#2024")
        self.assertEqual(feedback, [])

    def test_weak_password_has_multiple_feedback_items(self):
        _, feedback = score_password("abc")
        self.assertGreater(len(feedback), 1)

    # --- Score bounds ---

    def test_score_never_exceeds_100(self):
        score, _ = score_password("C0mpl3x!Pass#2024LongEnough")
        self.assertLessEqual(score, 100)

    def test_score_never_below_zero(self):
        score, _ = score_password("")
        self.assertGreaterEqual(score, 0)

    # --- Special character coverage ---

    def test_each_special_char_group_recognized(self):
        for ch in "!@#$%^&*()_+-=[]{}|;:,.<>?":
            score, _ = score_password(f"Password1{ch}")
            self.assertGreaterEqual(score, 55, f"Special char '{ch}' not recognized")


class TestGetStrengthLabel(unittest.TestCase):

    def test_score_80_is_strong(self):
        self.assertEqual(get_strength_label(80), "STRONG")

    def test_score_100_is_strong(self):
        self.assertEqual(get_strength_label(100), "STRONG")

    def test_score_50_is_moderate(self):
        self.assertEqual(get_strength_label(50), "MODERATE")

    def test_score_79_is_moderate(self):
        self.assertEqual(get_strength_label(79), "MODERATE")

    def test_score_49_is_weak(self):
        self.assertEqual(get_strength_label(49), "WEAK")

    def test_score_0_is_weak(self):
        self.assertEqual(get_strength_label(0), "WEAK")


if __name__ == "__main__":
    unittest.main(verbosity=2)
