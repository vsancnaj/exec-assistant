---
name: payment-chase
description: Finds failed and missed payments and open disputes, then drafts the right chase message or prepares a dispute handoff for the operations manager. Use when the user asks about failed payments, chasing money, Stripe disputes, or "who hasn't paid".
---

# Payment chase

Reads `data/payments.json`. Writes `outputs/<today>/payments.md` and appends drafts to `outputs/<today>/drafts.md`. Never charges, refunds or contacts anyone.

## Steps
```
- [ ] 1. Read context/voice.md, escalation.md, corrections.md
- [ ] 2. Run: python3 helpers/checks.py payments data/payments.json --today <today>
- [ ] 3. Act on each output line (table below)
- [ ] 4. Write payments.md
```
The helper decides the action. Do not recount attempts or dates yourself.

## Act on each line
| Helper says | Do |
|---|---|
| `FAILED ... CHASE_FIRST` | Draft a friendly first reminder: payment did not go through, here is the update-card link, no pressure. Add to drafts.md |
| `FAILED ... CHASE_SECOND` | Draft a second, still warm but clearer reminder asking them to update their card soon. Do not mention how many attempts failed, what happens next, or anyone following up, and give no dates or deadlines: Sam sets any. Add to drafts.md |
| `FAILED ... ESCALATE_SAM` | No draft. Escalate to Sam: attempts, days since last try, and a suggestion for Sam to decide (pause access or call) |
| `DISPUTE ... URGENT` | Escalate to Sam at the top of payments.md with days left |
| `DISPUTE ... OK` | List for Sam with the due date |

## Dispute handoff checklist (for Sam)
For each dispute, list what to gather: proof the member joined, call attendance or login records, the program terms they accepted, and any messages with them. Say which of these is not in the data. Never state whether the dispute will be won.

## Rules
- Use first names and amounts only. No card details.
- Never offer a discount, refund or payment plan. If the member asks, that is Sam's call.
- Link text for updating a card is a placeholder: write `[update-card link]` for Sam to insert.

## payments.md format
```
# Payments <today>
## Urgent (Sam)
- <id> <what, days left>
## Chase drafts (see drafts.md)
- <id> <first or second reminder>
## Watching
- <id> <why no action yet>
```
