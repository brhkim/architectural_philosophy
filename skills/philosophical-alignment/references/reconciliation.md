# Reconciling several maintainers' philosophies

How to turn several maintainers' individual philosophies into one shared philosophy without averaging anyone
away. The process borrows from structured group judgment (Delphi and the policy Delphi), open-source
governance (IETF rough consensus, Apache lazy consensus, the Rust final comment period, Python's steering
council), consent-based decision making (sociocracy), and principled negotiation. It also covers onboarding a
new maintainer later.

## Contents

- Principles
- Files and folders
- Round 0: the governance agreement
- The alignment report (the diff)
- Round 1: definitions and framing first
- Round 2: exploring divergence
- Round 3: proposed dispositions
- Round 4 and later: objections, then a final comment period
- Stopping rule
- Closing a cycle
- Decision rules a team can choose
- Endorsement levels
- Recording disagreement
- Presenting differences neutrally
- Onboarding a new maintainer
- What the agent must not do

---

## Principles

1. **Interview alone first.** Each maintainer's individual file is produced before they see anyone else's, so
   no one's framing anchors another's.
2. **Agree on what the words and tensions are before comparing where people stand.** Two maintainers can
   disagree sharply on a stance while sharing an understanding of what the issue is; that shared framing
   (called meta-consensus in deliberation research) is what makes the later comparison meaningful. Without it,
   people argue past each other. Definitions come first of all: two people who mean different things by
   "Correctness" are not yet disagreeing about correctness.
3. **Never average stances.** When views cluster at two points, a midpoint describes nobody, hides a real
   conflict, and misleads agents. On a three-way trade-off the average of two corners can land somewhere the
   trade-off itself says is infeasible. Divergence is shown as named positions, never as a mean.
4. **Ask for objections, not agreement.** "Can anyone not live with this?" separates choices that are merely
   unappealing from those that are truly harmful (IETF RFC 7282).
5. **Disagreement is a recorded state, not a failure.** A tension can end a cycle as contested, scoped or
   decided over a recorded objection, with dissent and a reopen trigger.
6. **The team chooses its decision rule in advance,** and every shared stance records which rule decided it
   and who applied it.
7. **Humans decide.** The agent drafts, compares, quotes and records. It never declares consensus.

## Files and folders

Inside the philosophy folder (layout in `SKILL.md`):

```
individuals/<handle>/philosophy.json     each maintainer's own file (never edited by reconciliation)
individuals/<handle>/session-notes.md    their interview state
GOVERNANCE.md                            the team's agreement (Round 0)
reconciliation/<YYYY-MM-DD>_<slug>/      one folder per cycle:
    snapshot.md                          which individual files and git commits this cycle used
    round-1_alignment.md                 the alignment report: definitions, framing, classified rows
    responses/<handle>.md                each person's private responses, per round
    round-2_divergence.md                positions, interests and strongest counter-arguments
    round-3_proposals.md                 candidate dispositions per row, with endorsements
    outcome.md                           final dispositions, rule applied, who decided, links to amendments
philosophy.json                          the shared result (what agents read, with PHILOSOPHY.md)
AMENDMENTS.md                            one entry per changed tension or value
```

A solo project skips all of this. When a second maintainer joins a solo project, copy the existing
`philosophy.json` to `individuals/<first-handle>/philosophy.json` as that person's record, interview the
newcomer, and run a light cycle (see "Onboarding a new maintainer").

## Round 0: the governance agreement

Before any substance is on the table, the team writes `GOVERNANCE.md`. Agreeing on procedure before content is
easier, and it is what negotiators recommend when substantive criteria are disputed. A template:

```markdown
# Philosophy governance

**Participants and scopes:** alex (core, CLI), sam (resolver), lee (docs). Emeritus: none.
**Default decision rule:** consent. **Fallback:** arbiter (alex), used only after two rounds without
change. **Low-stakes items** (wording, new precedents, adopting a singleton tension as provisional): lazy
consensus, 72 hours.
**Consensus caller:** alex for this cycle (rotates each cycle).
**Comment windows:** 72 hours per round; a 10-day final comment period before adoption.
**Round cap and stopping rule:** at most four rounds; a row unchanged across two rounds is recorded as stable
disagreement.
**Agent strictness:** advisory; flag-and-ask for core stances.
**Joining and leaving:** newcomers interview before reading PHILOSOPHY.md; leavers move to emeritus, and their
positions stay visible as history.
**Ratification:** merging the reconciliation pull request after the final comment period ratifies it.
```

Revisit the agreement rarely, and only through the same process.

## The alignment report (the diff)

Input: the individual files, snapshotted at specific commits (record them in `snapshot.md`). The agent matches
values and tensions across files, proposes matches ("Alex's T03 and Sam's T05 look like the same tension"), and
the maintainers confirm or reject each match. Every row then gets one class.

| Class | Detection | Treatment |
|-------|-----------|-----------|
| **0. Definitional divergence** | The same value word with different definitions, boundaries or `in_own_words` across files; or different words for what reads as the same meaning. | Resolve first, before any framing or stance discussion (Round 1). |
| **1. Aligned** | Same tension, compatible definitions, stances and flip conditions. | Candidate for `agreed`; confirm by lazy consensus. |
| **2. Framing mismatch** | Same values, different decomposition: a pair against a triad, values merged or split, different value sets. | Resolve in Round 1, after definitions. |
| **3. Stance divergence** | Same framing, different stances. | Rounds 2 to 4. Show as a distribution, never a mean. |
| **4. Flip-condition divergence** | Same stance, different conditions for flipping. | Often the cheapest to reconcile: a union or intersection of conditions, or a conditional stance. Often reveals differing interests. |
| **5. Scope divergence** | Stances differ because each person has a different part of the project in mind. | Offer a scoped split with owners. |
| **6. Singleton** | A value or tension appears in only one file. | Ask everyone else for their view (a mini round). Default: adopt as `provisional` by lazy consensus. Never silently drop it and never silently adopt it. |
| **7. Precedent conflict** | The same precedent cited for different stances, or a precedent that contradicts a stance. | Treat the precedent as shared evidence and discuss what it actually shows. |
| **8. Cross-tension inconsistency** | The combination of candidate stances implies a cycle or contradiction that no individual holds (for example speed over cost, cost over quality, quality over speed). | Flag in Round 3; resolve before adoption. |

### What the report shows for each row

- The definitions of the values involved, from each file, quoted, with `in_own_words` and `examples`.
- Each person's stance, quoted from their file, side by side in a fixed order that does not imply rank
  (alphabetical by handle, or anonymous labels in the first pass).
- Their flip conditions, precedents, firmness and evidence level.
- For multi-way tensions, each person's point on the same diagram or table, plus a plain statement of whether
  positions cluster in one place or several. If numeric weights exist, a geometric-mean summary may be shown,
  labelled "summary only, not a stance". Never adopt it as the shared stance.

The map page can help here: render each individual file, or show positions on a shared tension (the shared file
carries `positions`).

## Round 1: definitions and framing first

**Definitions (class 0).** For each value whose meaning differs, show the definitions and elaborations side by
side and ask:

- "Are you describing the same thing in different words, or two different things under one word?"
- "Can you find a definition you would both accept, or should this become two values?"
- "What does each of you call this value that the other would not?" (the boundary)

Outcomes: one shared definition (built from both people's words, read back, confirmed by each; `by:
"shared"`), a split into two values with separate IDs, or a recorded definitional disagreement that keeps the
tension `contested` until resolved. Each maintainer's own elaboration stays in their individual file.

**Framing (class 2).** Then ask only about framing: "Is this the same tension? Are these the right values? Is
it a pair, a triad, or more?" The outcome is a shared catalog of values and tensions, every row classified.
This step is the equivalent of consenting to a purpose before debating a proposal.

No stance is compared in Round 1.

## Round 2: exploring divergence

For each row in classes 3 to 5, the agent shows the positions, each holder's stated interests and flip
conditions, and asks each person privately (answers go to `responses/<handle>.md`):

- "What is the strongest case for the other position?"
- "What would make you move?"
- "Can you live with the other position? If not, what specific harm would it cause?"
- When a file gives only a position: "Why do you hold it, and why not the other one?" (interests, not positions)

The goal is that every option and the strongest argument for each is on the table, as in a policy Delphi,
which seeks the strongest opposing views rather than early convergence. Asking "which part of the project are
you thinking of?" dissolves many apparent disagreements into scope differences.

## Round 3: proposed dispositions

For each row the agent drafts one disposition from a fixed menu. The menu deliberately has no numeric midpoint.

| Disposition | When it fits |
|-------------|-------------|
| **Adopt stance X** | One stance has broad support and no reasoned objection. |
| **Adopt a conditional stance** | The positions are both right in different situations; build the stance from their flip conditions. |
| **Split by scope with named owners** | The disagreement tracks different subsystems. |
| **Adopt provisionally with a review date** | Good enough for now and safe enough to try until the date. |
| **Mark contested** | No disposition is acceptable yet; list the options and their holders, and optionally agree a settling test and an arbiter. |

Each maintainer responds per row with an endorsement level (below). Every objection states its reason.

Watch for linked concessions ("I'll drop my objection on T03 if you drop yours on T05"). Trading stances across
tensions produces a philosophy nobody holds; the agent flags it when concessions look linked.

## Round 4 and later: objections, then a final comment period

Test each objection: would the proposed disposition fail the project's purpose, cause a harmful side effect, or
waste effort or miss a clear improvement? An objection that meets one of those tests is resolved by changing
the proposal, or, under rough consensus, recorded by the named caller as addressed but not accommodated. A
concern that does not meet them is recorded and does not block.

Then run a final comment period on the whole set of dispositions: every decision-holder signs off, a timer runs
(the governance agreement sets it), and a substantively new argument reopens that row only.

## Stopping rule

- Stop when every row has a status.
- If a row's positions are unchanged across two consecutive rounds, record it as stable disagreement: status
  `contested`, or decided by the fallback rule if the governance agreement says so, with dissent recorded.
- Respect the round cap (three or four rounds).

## Closing a cycle

1. Write `outcome.md`: each row's disposition, the rule applied, who decided, dissent, review dates.
2. Update the shared `philosophy.json`: stances, `status`, `positions`, `dissent`, `decision`, `review_by`,
   `origin`, and the glossary (shared definitions with `by: "shared"`). Assign shared `T` numbers to new
   tensions now, not earlier. Draft the shared `synthesis` (3 to 5 plain sentences) and have it confirmed under
   the team's decision rule.
3. Append one `AMENDMENTS.md` entry per changed tension or value, and bump the document version
   (`amendments.md`).
4. Run a cross-tension consistency check on the result (class 8), and a definition check: every value word in
   every stance summary and flip condition is used in its glossary sense.
5. Regenerate `PHILOSOPHY.md` and the map. Suggest a commit message; commit only when asked.

## Decision rules a team can choose

The team picks a default and a fallback in `GOVERNANCE.md`, optionally different for different kinds of item.

| Rule | How it decides | Good for |
|------|---------------|----------|
| Full consensus | Everyone actively endorses; apathy does not count. | Two or three founders; foundational tensions. |
| **Consent** (a sensible default) | Adopted when no reasoned objection remains; concerns recorded; a review date set. | Most teams and most tensions. |
| Rough consensus | A named human caller declares it once every objection is addressed, even if not accommodated; holdouts named. | Larger teams; a persistent single holdout. |
| Lazy consensus | Silence over a stated window (for example 72 hours) counts as assent; objections need reasons. | Low-stakes changes, singleton adoption, newcomer confirmations. |
| Scoped owner | The owner of a subsystem decides that subsystem's stance after consultation. | Projects with clear module ownership. |
| Council vote | A strict majority of non-abstaining decision-holders; everyone votes or explicitly abstains. | A fallback when consent fails on a project-wide item. |
| Arbiter | A named person decides after hearing all positions; dissent recorded. | Founder-led projects; the last fallback. |

Whatever the rule, the posture afterwards is "disagree and commit": the dissenter's view is recorded with a
reopen trigger, and the team proceeds. Avoid sequences of pairwise votes among three or more options, where the
order of votes can decide the outcome.

## Endorsement levels

Recorded per holder in `positions[].endorsement`.

| Level | Meaning |
|-------|---------|
| `endorse` | "This is my view." |
| `consent` | "Not exactly my view, but I have no objection." |
| `consent with concern` | "I can live with it; here is a concern to record." Does not block. |
| `stand aside` | "I won't take part in this one" (for example a conflict of interest). |
| `in the rough` | "I still object, and my objection was heard and addressed but not accommodated." |
| `object` | "I cannot live with this, for this reason." Blocks under consent until resolved. |

An optional `intensity` from -1 to +1 records strength of feeling, in the style of Apache votes ("-0.5: I don't
like it but won't block").

## Recording disagreement

- The tension stays in the shared file with status `contested`, `rough` or `scoped`. It is never removed or
  averaged.
- Every position is listed with its holder, quoted stance, stated interests and endorsement level.
- Each `dissent` entry says what would change the dissenter's mind (`reopen_trigger`) and, where the team
  agrees on one, a `settling_test` (an experiment, metric or precedent to watch) with an arbiter.
- Each recorded concern or dissent has a `review_by` date.
- Agents never pick a side on a contested tension; they present the positions and ask, at any strictness.

## Presenting differences neutrally

1. Quote each holder's stance and definitions from their own file. Do not paraphrase toward a middle.
2. Show reasons and interests, not only positions.
3. Name the shape of the difference before asking anyone to move: "You define Correctness differently", "You agree on
   the values but weight them differently", "You agree on the stance but would flip it under different
   conditions", "You are thinking of different subsystems."
4. Offer only options the structure allows: shared or split definitions, scope splits, conditional stances
   built from the flip conditions, provisional adoption with a review date.
5. Ask objection-shaped questions, and classify each response as objection, concern or preference.
6. Never summarise in a way that nudges toward an option. Group feedback is known to pull people toward
   whatever the summary emphasises.

## Onboarding a new maintainer

1. **Interview first, read later.** The newcomer completes their own interview, including their own
   definitions of the key values, before reading `PHILOSOPHY.md`. If they have already read it, record that in
   their session notes; their answers are then partly anchored.
2. **Align against the shared file,** not against every individual file, using the same classes (definitions
   first).
3. **Light cycle by default.**
   - Confirmations add the newcomer to the holder list.
   - New values and tensions become `provisional` by lazy consensus.
   - A definitional difference on a shared value is discussed with the value's current holders; the shared
     definition changes only through an amendment.
   - A divergence on an `agreed` or `consented` tension is tested as an objection: a reasoned objection reopens
     that tension for a mini cycle; a preference or concern is recorded without reopening it. Settled items do
     not churn every time someone joins.
4. **Record membership** in `GOVERNANCE.md` and `maintainers`. A maintainer who leaves becomes `emeritus`:
   their positions stay visible as history but no longer count as current holders.
5. **Orient the newcomer** afterwards with the map page and the decision-card worked example, so they see how
   the philosophy is used.

## What the agent must not do

- Compute a shared stance by arithmetic.
- Declare consensus. Only the named human caller or the chosen rule can.
- Paraphrase a holder's stance or definition toward a midpoint. Quote instead.
- Merge two maintainers' definitions of a word without both confirming the result.
- Drop a value or tension because only one person raised it.
- Reopen every settled tension whenever someone new joins.
- Treat silence as assent, except under an explicitly chosen lazy-consensus window.
- Edit an individual maintainer's file during reconciliation.
