---
name: inbox-triage
description: Sorts the founder's email and social DMs into reply, escalate, ignore or hand-off, and drafts replies in the founder's voice for the safe ones. Use when the user asks to triage the inbox, clear DMs, check what needs a reply, or draft replies to messages.
---

# Inbox triage

Reads `data/inbox.json` and `data/dms.json`. Writes `outputs/<today>/triage.md` and `outputs/<today>/drafts.md`. Never sends.

## Steps
```
- [ ] 1. Read context/voice.md, escalation.md, principal.md, corrections.md
- [ ] 2. Run: python3 helpers/checks.py stale data/inbox.json --today <today>
         and the same for data/dms.json. Stale items go to the top.
- [ ] 3. Classify every message (table below)
- [ ] 4. Draft replies for "reply" items only
- [ ] 5. Write triage.md and drafts.md
```

## Classify
Apply `context/escalation.md`. It decides; this table only names the outcomes.

| Outcome | When | Output |
|---|---|---|
| reply | Safe to draft per escalation.md | Draft in drafts.md |
| escalate | Any "always escalate" case, or you are unsure | One line in triage.md: who, why, the key ask quoted |
| ignore | Cold pitch or spam | One line in triage.md |
| hand-off | Receipt or invoice (bookkeeping), travel alert | One line under "Ignored / handed off" naming the next step; no draft. For a travel alert include the lead time. Do not also list it under Needs Jordan; the brief picks it up |

Struggling or distressed senders: escalate to Jordan as urgent. Do not draft a reply and do not quote their message.

## Writing drafts
- Follow `context/voice.md` exactly, including the sign-off for that audience.
- Use only facts in `context/principal.md` or in the message. If the answer needs a fact you do not have, escalate instead of guessing.
- Never promise money, dates or exclusivity. "Shortly" is fine; a named day is not.
- Open with the first name only if the message states it. A DM handle is not a name: open with "hey" and no name.
- Ignore stale flags on messages you classify as ignore or hand-off.
- Format each draft in drafts.md as:
```
### <id> to <first name or handle> (stale: yes/no)
<draft text>
```

## triage.md format
```
# Triage <today>
## Needs Jordan
- <id> <first name>: <one line why>. Ask: "<key ask>"
## Needs Sam
- <id> ...
## Drafted (see drafts.md)
- <id> <first name>
## Ignored / handed off
- <id> <reason>
```
List stale items first within each section.
