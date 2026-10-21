import unittest

from app import answer_college_question


class CollegeLookupTests(unittest.TestCase):
    def test_returns_college_name_from_json(self):
        answer = answer_college_question("What is the name of the college?")
        self.assertIn("rathinam technical campus", answer.lower())

    def test_returns_missing_info_message(self):
        answer = answer_college_question("What is the hostel menu for today?")
        self.assertEqual(
            answer,
            "Sorry, I don't have that information in my college database."
        )


if __name__ == "__main__":
    unittest.main()
