---
name: review-drafts
description: Independently reviews drafted replies against the founder's voice guide and escalation rules before anything reaches the founder, returning pass, fix or escalate for each draft. Use after drafting replies, or when the user asks to check, review or sanity-check drafts.
---

# Review drafts

A fresh-eyes check. It reviews; it never edits `drafts.md`. Run it in a subagent with clean context when one is available, giving it only `drafts.md`, `context/voice.md`, `context/escalation.md`, `context/corrections.md`, `context/principal.md` and, if payment drafts are present, `payments.md`. Do not pass the drafting reasoning.

Writes `outputs/<today>/review.md`.

## Checks, in this order
Mechanics first, then judgment.

1. **Escalation:** does this draft touch money, a brand or press, personal distress, legal or data matters, or access? If yes, it should not exist: verdict `escalate`.
2. **Promises:** any discount, refund, date, rate or exclusivity promised? Verdict `fix` (or `escalate` if it commits money).
3. **Facts:** is every fact traceable to `principal.md` or the original message? An invented fact is `fix`.
4. **Voice:** US spelling, first name, answer first, banned phrases absent, correct sign-off for the audience, at most one emoji.
5. **Length and clarity:** can the recipient act on it in one read?
6. **Corrections:** does it repeat anything listed in `corrections.md`? That is `fix`.

## review.md format
```
# Review <today>
| Draft | Verdict | Finding |
|---|---|---|
| <id> | pass / fix / escalate | <one line, specific: quote the offending phrase> |

## Summary
<n> pass, <n> fix, <n> escalate.
```

## Rules
- A finding names the exact phrase and the rule it breaks, so the author can fix it without guessing.
- If the draft is acceptable, say `pass` and stop. Do not invent nitpicks.
- A repeat review starts fresh, then checks each earlier finding was fixed.
