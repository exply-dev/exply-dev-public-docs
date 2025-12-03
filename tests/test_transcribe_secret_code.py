import unittest

from scripts.transcribe_secret_code import extract_numeric_code


class ExtractNumericCodeTests(unittest.TestCase):
    def test_concatenates_digit_groups(self) -> None:
        text = "секретный код: 12 34 56-78"
        self.assertEqual(extract_numeric_code(text), "12345678")

    def test_detects_russian_words(self) -> None:
        text = "цифры: один два три четыре пять шесть семь"
        self.assertEqual(extract_numeric_code(text), "1234567")

    def test_raises_when_missing_digits(self) -> None:
        with self.assertRaises(ValueError):
            extract_numeric_code("не удалось распознать код")


if __name__ == "__main__":
    unittest.main()
