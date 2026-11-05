---
name: daily-priorities
description: Writes the founder's short daily priorities brief from the day's triage, payments and calendar, so the founder knows exactly what needs them. Use when the user asks for the daily brief, morning priorities, "what needs me today", or a day plan.
---

# Daily priorities

Composes `outputs/<today>/brief.md`. It summarizes; it does not re-triage. Needs `triage.md` and `payments.md` in the run folder. If either is missing, run `/inbox-triage` or `/payment-chase` first.

## Steps
```
- [ ] 1. Read context/principal.md (preferences) and the run folder's triage.md and payments.md
- [ ] 2. Run: python3 helpers/checks.py conflicts data/calendar.json
- [ ] 3. Read data/calendar.json for today and the next 30 days
- [ ] 4. Pick one top priority
- [ ] 5. Write brief.md
```

## Choosing the top priority
Pick the single item with the nearest hard deadline and the largest cost of delay. Typical order: urgent dispute, urgent distress message, a brand or press deadline within the week, a calendar clash today, then stale VIP messages. State it in one sentence.

## brief.md format (strict)
```
# Brief <today>
**Top priority:** <one sentence>

## Needs you (max 5)
- <item>: <what is needed>. (<Jordan|Sam>)

## Today
- HH:MM-HH:MM <event>   (flag CLASH with the other event id)

## Also needs you (overflow)
- <id> <first name>: <one line> (<Jordan|Sam>)

## Waiting too long (unanswered messages only, stale per the helper)
- <id> <first name>, <days> days

## Money
- <one line per urgent payment or dispute>

## Coming up (next 30 days)
- <event or deadline>: <what is not done, e.g. "flights not booked">

## Handled
- <n> replies drafted, <n> ignored, <n> handed off
```

## Rules
- "Needs you" never exceeds the limit in `principal.md`. If more qualify, keep the most urgent and put the rest under "Also needs you (overflow)". Never use "Waiting too long" for items that are not stale.
- Travel alerts handed off by triage go under "Coming up", not "Needs you".
- Every item names who it is for. The calendar clash counts as one of the items.
- A calendar clash is always listed, with both events, and a suggestion to move the lower-stakes one. Do not move anything.
- Anything within 30 days of travel that is not booked goes under "Coming up". Flag it; never book.
- Quote brand and press asks, as `principal.md` requires. Do not quote distressed members.
