from .parse import parse_issue, parse_issues
from unittest import TestCase

class TestIssueParsing(TestCase):

    def test_completed_issue_with_number(self):
        status, title, number = parse_issue("+ this is a test issue (512)")
        self.assertEqual('complete', status)
        self.assertEqual('this is a test issue', title)
        self.assertEqual(512, number)


    def test_in_progress_issue_with_number(self):
        status, title, number = parse_issue("- this is a test issue also (513)")
        self.assertEqual('in progress', status)
        self.assertEqual('this is a test issue also', title)
        self.assertEqual(513, number)

    def test_issue_no_number(self):
        status, title, number = parse_issue("  and this")
        self.assertEqual('pending', status)
        self.assertEqual('and this', title)
        self.assertIsNone(number)

    def test_abandoned(self):
        status, title, number = parse_issue("! I decided not to do this (41)")
        self.assertEqual('abandoned', status)
        self.assertEqual('I decided not to do this', title)
        self.assertEqual(41, number)

    def test_comments_and_empty_lines(self):
        issues = """+ I did this one (451)
; this is a comment

; this is also a comment
- Working on this one""".split('\n')
        issues = [issue for issue in parse_issues(issues)]
        self.assertEqual(5, len(issues))


    def test_hanging_parenthesis(self):
        _, title, number = parse_issue("  some title with a random extra (bracket")
        self.assertEqual(title, "some title with a random extra (bracket")
        self.assertIsNone(number)

