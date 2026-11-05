#!/usr/bin/env python3
"""Deterministic checks for the e-assistant.

The model decides what to say; this script decides what is late, clashing or
overdue. It prints ids and aggregates only, never message bodies.

Usage (from the repo root):
    python3 helpers/checks.py stale data/inbox.json --today 2026-03-16
    python3 helpers/checks.py conflicts data/calendar.json
    python3 helpers/checks.py payments data/payments.json --today 2026-03-16
"""
import argparse
import json
import sys
from datetime import date

# A message left unanswered this long counts as stale. Two days keeps most
# members inside a "reply within a working day or two" promise.
STALE_DAYS = 2

# Payment failed this many times is no longer a polite reminder; it goes to Sam.
ESCALATE_ATTEMPTS = 3

# A failed payment untouched for this long needs a human look even at 2 attempts.
ESCALATE_AFTER_DAYS = 7

# Flag a dispute with this many days or fewer left, so there is time to gather evidence.
DISPUTE_URGENT_DAYS = 5


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"ERROR: {path} not found. Run from the repo root.")
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: {path} is not valid JSON ({e}).")


def parse_date(value, label):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        sys.exit(f"ERROR: {label} must be YYYY-MM-DD, got {value!r}.")


def stale(items, today, threshold=STALE_DAYS):
    out = []
    for item in items:
        if item.get("replied"):
            continue
        age = (today - parse_date(item["received"], f"{item['id']}.received")).days
        if age >= threshold:
            out.append((item["id"], age))
    return out


def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def conflicts(events):
    out = []
    for i, a in enumerate(events):
        for b in events[i + 1:]:
            if a["date"] != b["date"]:
                continue
            if to_minutes(a["start"]) < to_minutes(b["end"]) and to_minutes(b["start"]) < to_minutes(a["end"]):
                out.append((a["id"], b["id"], a["date"]))
    return out


def payments(rows, today):
    out = []
    for r in rows:
        if r["type"] == "dispute" and r["status"] == "needs_response":
            left = (parse_date(r["evidence_due"], f"{r['id']}.evidence_due") - today).days
            tag = "URGENT" if left <= DISPUTE_URGENT_DAYS else "OK"
            out.append(f"DISPUTE {r['id']} amount={r['amount']} {r['currency']} days_left={left} {tag} owner=Sam")
        elif r["type"] == "payment" and r["status"] == "failed":
            since = (today - parse_date(r["last_attempt"], f"{r['id']}.last_attempt")).days
            attempts = r["failed_attempts"]
            if attempts >= ESCALATE_ATTEMPTS or since >= ESCALATE_AFTER_DAYS:
                action = "ESCALATE_SAM"
            elif attempts >= 2:
                action = "CHASE_SECOND"
            else:
                action = "CHASE_FIRST"
            out.append(f"FAILED {r['id']} attempts={attempts} days_since={since} action={action}")
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("stale", "conflicts", "payments"):
        s = sub.add_parser(name)
        s.add_argument("file")
        s.add_argument("--today", default=None, help="YYYY-MM-DD; required for stale and payments")
    args = p.parse_args()

    if args.cmd in ("stale", "payments") and not args.today:
        sys.exit("ERROR: --today YYYY-MM-DD is required.")
    today = parse_date(args.today, "--today") if args.today else None
    data = load(args.file)

    if args.cmd == "stale":
        lines = [f"STALE {i} days={d}" for i, d in stale(data, today)]
    elif args.cmd == "conflicts":
        lines = [f"CONFLICT {a} {b} {d}" for a, b, d in conflicts(data)]
    else:
        lines = payments(data, today)
    print("\n".join(lines) if lines else "NONE")


if __name__ == "__main__":
    main()
