---
name: e-assistant
description: Orchestrates the executive assistant agent. Runs the daily chain (inbox triage, payment chase, daily priorities brief, draft review) or routes a single request to the right skill. Use when the user says /e-assistant, asks "what's on today", "run the morning brief", "handle my inbox and payments", or gives an admin request for the founder that no other skill clearly owns.
---

# E-Assistant (orchestrator)

Drafts and flags only. Nothing is sent, booked, refunded or filed.

## Before anything else
Read `AGENTS.md`, then every file in `context/` (voice, escalation, principal, corrections). Create `outputs/<today>/` where today is the date in `AGENTS.md`.

## Route the request
| Request | Do |
|---|---|
| No request, "morning brief", "what's on today" | Full chain below |
| Emails, DMs, comments to handle | `/inbox-triage` only, then `/review-drafts` |
| Failed payments, disputes, chasing money | `/payment-chase` only, then `/review-drafts` |
| "Just the brief" | `/daily-priorities` only, using files already in the run folder |
| Anything else | Say what is outside scope and who it should go to (Jordan or Sam). Do not improvise |

## Full chain
Copy this checklist and tick it off:
```
- [ ] 1. /inbox-triage      -> triage.md, drafts.md
- [ ] 2. /payment-chase     -> payments.md (drafts appended to drafts.md)
- [ ] 3. /daily-priorities  -> brief.md
- [ ] 4. /review-drafts     -> review.md
- [ ] 5. Act on review.md (rules below)
- [ ] 6. Report
```
Step 4 must run in a separate subagent (the Agent tool) started with clean context. Give it only `outputs/<today>/drafts.md`, `context/voice.md`, `context/escalation.md`, `context/corrections.md`, `context/principal.md`, `outputs/<today>/payments.md` (so it can check payment drafts against the helper's decisions) and the path to `.claude/skills/review-drafts/SKILL.md`; also tell it today's project date (from `AGENTS.md`) for the review.md heading. Do not pass your drafting reasoning. If you cannot start a subagent, still run the review but say "review was not independent" in the report.

Run the steps in this order: the brief needs triage and payments, and the review needs every draft. If a step cannot run (missing data file), say so in the report and continue with the rest.

## Acting on the review
- `pass`: keep the draft.
- `fix`: rewrite that draft once, then re-run the review once for it. If it is still `fix`, treat it as `escalate`.
- `escalate`: remove the draft from `drafts.md`, add the item to "Needs Jordan" or "Needs Sam" in the brief with the reviewer's reason, and say so in the report. Never keep a draft the reviewer escalated.
Never overrule the reviewer. If you disagree, say so in the report and let the human decide.

## Report
Finish with at most 8 lines: the top priority, how many items need Jordan and how many need Sam (count every item for them in the brief's "Needs you" and overflow sections, including the calendar clash), how many drafts passed review, and the path `outputs/<today>/brief.md`. Never paste message bodies.

## Corrections
If the user corrects a draft or a decision, append one dated line to `context/corrections.md` (`YYYY-MM-DD | wrong | do instead`), then apply it.
