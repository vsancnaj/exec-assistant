import unittest
from datetime import date

from checks import conflicts, payments, stale

TODAY = date(2026, 3, 16)


class StaleTests(unittest.TestCase):
    def test_flags_old_unreplied_only(self):
        items = [
            {"id": "a", "received": "2026-03-10", "replied": False},
            {"id": "b", "received": "2026-03-16", "replied": False},
            {"id": "c", "received": "2026-03-03", "replied": True},
        ]
        self.assertEqual(stale(items, TODAY), [("a", 6)])


class ConflictTests(unittest.TestCase):
    def test_overlap_and_touching(self):
        events = [
            {"id": "1", "date": "d", "start": "10:00", "end": "11:00"},
            {"id": "2", "date": "d", "start": "10:30", "end": "11:30"},
            {"id": "3", "date": "d", "start": "11:30", "end": "12:00"},
        ]
        self.assertEqual(conflicts(events), [("1", "2", "d")])


class PaymentTests(unittest.TestCase):
    def test_actions(self):
        rows = [
            {"id": "p1", "type": "payment", "status": "failed", "failed_attempts": 1, "last_attempt": "2026-03-15"},
            {"id": "p2", "type": "payment", "status": "failed", "failed_attempts": 2, "last_attempt": "2026-03-14"},
            {"id": "p3", "type": "payment", "status": "failed", "failed_attempts": 3, "last_attempt": "2026-03-03"},
            {"id": "p4", "type": "dispute", "status": "needs_response", "amount": 1, "currency": "USD", "evidence_due": "2026-03-19"},
            {"id": "p5", "type": "payment", "status": "paid", "failed_attempts": 0, "last_attempt": "2026-03-13"},
        ]
        out = payments(rows, TODAY)
        self.assertIn("action=CHASE_FIRST", out[0])
        self.assertIn("action=CHASE_SECOND", out[1])
        self.assertIn("action=ESCALATE_SAM", out[2])
        self.assertIn("URGENT", out[3])
        self.assertEqual(len(out), 4)


if __name__ == "__main__":
    unittest.main()
