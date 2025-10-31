import unittest
from q1_crm_cleanup import (
    normalize_phone,
    clean_email,
    parse_text,
    deduplicate_rows,
)
class TestCRMCleanup(unittest.TestCase):

    # -------------------------------------------------------------
    # 1️⃣ Email validation tests
    # -------------------------------------------------------------
    def test_valid_emails(self):
        valid_emails = [
            "alice@example.com",
            "bob.smith@company.co",
            "user+alias@domain.org",
            "UPPERCASE@EXAMPLE.IO",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertEqual(clean_email(email), email)

    def test_invalid_emails(self):
        invalid_emails = [
            "no-at-symbol.com",
            "user@.com",
            "bad@email",
            "another@@example.com",
            "email@domain,com",
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertEqual(clean_email(email), "")

    # -------------------------------------------------------------
    # 2️⃣ Phone normalization tests
    # -------------------------------------------------------------
    def test_phone_normalization(self):
        cases = {
            "(469) 555-1234": "4695551234",
            "+1-972-555-7777": "9725557777",
            "214.555.8888": "2145558888",
            "972 777 2121": "9727772121",
            "555-999": "",  # too short
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(normalize_phone(raw), expected)

    # -------------------------------------------------------------
    # 3️⃣ Parsing logic from multi-line string
    # -------------------------------------------------------------
    def test_parsing_and_structure(self):
        text = """Alice Johnson <alice@example.com> , +1 (469) 555-1234
Sara M. , sara@mail.co , 214 555 8888
invalid_user , user@invalid , 555-000-0000
duplicate <Alice@Example.com> , 469 555 1234
"Mehdi A." <mehdi.ay@example.org> , (469)555-9999
"""
        rows = parse_text(text)
        expected = [
            {"name": "Alice Johnson", "email": "alice@example.com", "phone": "4695551234"},
            {"name": "Sara M.", "email": "sara@mail.co", "phone": "2145558888"},
            {"name": "Mehdi A.", "email": "mehdi.ay@example.org", "phone": "4695559999"},
        ]
        self.assertEqual(rows, expected)

    # -------------------------------------------------------------
    # 4️⃣ De-duplication by case-insensitive email
    # -------------------------------------------------------------
    def test_deduplication_case_insensitive(self):
        data = [
            {"name": "Alice", "email": "Alice@Example.com", "phone": "123"},
            {"name": "Duplicate", "email": "alice@example.COM", "phone": "999"},
            {"name": "Bob", "email": "bob@example.com", "phone": "111"},
        ]
        deduped = deduplicate_rows(data)
        expected = [
            {"name": "Alice", "email": "Alice@Example.com", "phone": "123"},
            {"name": "Bob", "email": "bob@example.com", "phone": "111"},
        ]
        self.assertEqual(deduped, expected)


# Run tests inside Jupyter or normal Python
if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
