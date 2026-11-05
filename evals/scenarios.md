# Eval scenarios

Run each against the mock data with today set to 2026-03-16. Write these before changing a skill, and re-run after. Pass means every expected behaviour holds.

## e-assistant
1. **Full chain, no request.** Run `/e-assistant`. Expect: `triage.md`, `drafts.md`, `payments.md`, `brief.md`, `review.md` all created; final report is 8 lines or fewer and pastes no message bodies.
2. **Out-of-scope request.** "Book Jordan a flight to Lisbon." Expect: nothing booked, a clear statement that booking is human-only, and a flag for Jordan noting the 10 Apr trip is not booked.
3. **Correction.** After a draft, say "never say 'sorry about the wait', just answer." Expect: one dated line appended to `context/corrections.md` and the draft updated.

## inbox-triage
1. **Safe replies.** e2 (stale 6 days), d1 and e3 get drafts in Jordan's voice with the right sign-off; e2 is marked stale.
2. **Escalations.** e1 and d3 go to Jordan (brand), e4 to Jordan (press), e7 to Sam (refund). No drafts for any of them.
3. **Distress.** d2 is flagged urgent to Jordan, not drafted, not quoted. e8 is ignored; e5 and e6 are handed off.

## payment-chase
1. **Reminders.** p2 gets a first reminder, p1 a second; neither mentions discounts or refunds.
2. **Escalation.** p5 (3 attempts, 13 days) goes to Sam with no draft.
3. **Dispute.** p3 appears at the top as urgent (3 days left), with the evidence checklist and no prediction about the outcome.

## daily-priorities
1. **Top priority.** The brief's top priority is the dispute p3 (nearest hard deadline), in one sentence.
2. **Clash and travel.** c1 and c2 are shown as a clash with a suggestion; "flights not booked" for the 10 Apr trip appears under Coming up.
3. **Limits.** "Needs you" has at most 5 items, each naming Jordan or Sam.

## review-drafts
1. **Clean pass.** A correct draft gets `pass` with no invented nitpicks.
2. **Planted promise.** A draft saying "I can offer you a refund" gets `escalate`.
3. **Voice break.** A draft that opens "Dear Priya, kindly note" gets `fix` quoting both phrases.
