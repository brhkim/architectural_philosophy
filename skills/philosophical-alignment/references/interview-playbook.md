# Interview playbook

How to interview one maintainer and turn the conversation into a philosophy file. It covers the facilitator
posture, the session flow, the "define before you weigh" step, the four interview styles (abstract values,
retrospective walkthrough, forced choice, contradiction checks), how each answer is recorded, pacing and
resumable state, and the pitfalls that distort answers.

The field names used below are documented in `data-model.md`. Canvases (interactive pages for placing
stances) are covered in `canvases.md`; this file says when to reach for one.

## Contents

- The facilitator posture
- Before the first session
- Session shape and pacing
- Step 1: orientation
- Step 2: their words first (abstract style, part one)
- Step 3: define before you weigh
- Step 4: shape each tension
- Step 5: retrospective walkthrough of a real decision
- Step 6: forced-choice scenarios
- Step 7: flip conditions and early warnings
- Step 8: the seed library as a "did we miss anything?" check
- Step 9: contradiction checks
- Step 10: read back, write, render
- The acceptable-opposite test
- Recording answers into the data model
- Saving resumable state
- Starting from a seed drafted from documents
- Wording for different kinds of project
- Pitfalls

---

## The facilitator posture

The agent is a facilitator and a scribe. It helps the maintainer say what they already believe, makes the
trade-offs explicit, and writes them down precisely. It does not supply values of its own, rank the
maintainer's values, or suggest which stance is better. Even when a stance seems unusual, the job is to
record it accurately, with its reasons and its conditions.

Why this matters: preferences are partly built during the interview itself. The way a question is framed, the
first example offered, and the vocabulary the interviewer uses all pull answers toward them. A philosophy that
echoes the agent's priorities is worse than none, because later agents will cite it as the maintainer's.

Practical consequences:

- Ask open questions before closed ones, and the maintainer's words before any framework's.
- Offer examples only after the maintainer has answered in their own terms, and offer several that point in
  different directions.
- Never propose a number, position or weight first. Let the maintainer place it.
- When summarising, quote. When paraphrasing, read the paraphrase back and ask whether it is right.
- Treat "I don't know" and "it depends" as useful answers. "It depends" usually means a flip condition is
  waiting to be named.
- Defer feature ideas that come up ("we should also build X") to a parked list in the session notes. An
  interview session never starts feature work.

## Before the first session

1. **Find the philosophy folder.** If `philosophy.json` exists, this is a resume, not a new interview: read it
   and the session notes for this maintainer (see "Saving resumable state").
2. **Read what already exists** (the detection list is in `SKILL.md`): READMEs, contributing guides, agent
   instruction files, ADR folders, design docs, a Spec Kit constitution, papers or pre-registrations for a
   research project. Note candidate values, tensions, hard limits and, above all, real past decisions that can
   anchor a retrospective walkthrough. Do not show this list to the maintainer before step 2; it would anchor
   them.
3. **Ask who is being interviewed** and choose a handle (`alex`, `maintainer-b`). In a team, each maintainer
   is interviewed separately, before seeing anyone else's answers or the shared file.
4. **Agree the session's goal and length** with the maintainer: a first session usually covers orientation,
   their own words, and three to five tensions in depth.
5. **Ask whether interactive canvases are welcome.** Some people like dragging a point on a triangle; others
   prefer to talk. The canvases need Python's standard library to serve the page, or nothing at all in the
   copy-and-paste fallback (`canvases.md`).

## Session shape and pacing

A good first session runs 30 to 60 minutes. A typical arc:

| Step | Rough time | Output |
|------|-----------|--------|
| 1. Orientation | 5 min | Mission, project type, stakeholders, non-goals |
| 2. Their words first | 10 min | A list of candidate values and tensions in the maintainer's language |
| 3. Define before you weigh | 10 to 15 min | Glossary entries for the key values |
| 4 to 7. Shape, walk through, choose, flip | 15 to 25 min | Three to five tensions with stances, flip conditions, precedents |
| 8. Seed check | 3 min | Any missed tensions, parked for the next session |
| 9. Contradiction check | 5 min | Contradictions resolved or logged as open |
| 10. Read back and write | 5 min | Updated `philosophy.json` and synthesis, rendered views, session notes |

Steps 3 to 7 loop per tension. Steps are a guide, not a script: if the maintainer starts with a story about a
recent decision, follow it (that is step 5) and come back. If a session must end early, save state after the
current tension; never leave a half-recorded stance.

Later sessions pick up from the session notes: finish open tensions, add new ones, run contradiction checks
across sessions, walk through a recent feature, or revisit a stance.

Signs to pause: answers getting shorter, repeated "whatever you think", or the maintainer agreeing with every
read-back without correcting anything. Offer to stop and resume.

## Step 1: orientation

Questions (adapt the nouns to the project):

- "In a sentence or two, what is this project for, and who is it for?" (becomes `mission`)
- "Who uses it directly? Who is affected by it without ever touching it?" (stakeholders; for a library, the
  end users of downstream applications; for a research project, the people the data describes)
- "What could reasonably be a goal here that you have chosen not to pursue?" (becomes `non_goals`)
- "Which kind of project is it closest to: a library, an application, a package manager or platform, a
  research project, a data analysis, documentation, something else?" (becomes `project_types`; used only to
  filter the seed library in step 8)

## Step 2: their words first (abstract style, part one)

The aim is a list of what the maintainer cares about and where they feel pulled, in their own vocabulary,
before any catalog is shown.

Opening questions:

- "When someone proposes a change to this project, what makes you uneasy even before you read the details?"
- "What would you be most upset to see this project become in three years?"
- "What do you find yourself defending in reviews, again and again?"
- "Which compliments about the project mean the most to you? Which ones miss the point?"

Laddering (means-end chains, from consumer research): when the maintainer names a concrete thing, ask why it
matters, then why that matters, until the answer is a value or an outcome for a stakeholder.

- "You mentioned `<concrete thing>`. Why does that matter for this project?"
- "And what does that give the people who use it?"
- Stop when the answer repeats or becomes "it just does". Do not repeat the same question mechanically;
  vary the wording and reflect back what you heard.

Laddering output becomes candidate values, with `serves` links from means to ends. It also stops a means
("fast CI") from being recorded as if it were an end ("contributor velocity").

Triads (repertory grid technique): show three real elements, for example three past features, three
comparable projects, or three design options the maintainer mentioned.

- "In what important way are two of these alike and different from the third?"
- "What is the opposite of that, in your words?"

Each answer is a two-ended construct: a candidate tension whose poles the maintainer named. Triads work only
with real elements the maintainer knows well; do not invent them.

Collect a short candidate list (five to twelve values or tensions). Write it down in the maintainer's words.

## Step 3: define before you weigh

No value is weighed, ranked or traded until it has an explicit, operational definition that the maintainer
has explained in their own words and confirmed. This is the step that stops "Correctness" from meaning one thing in
the interview, another in a decision card six months later, and a third to a new maintainer.

### Proportion

- **Full elaboration** for every value that carries a real tension, and for any word the maintainer used
  with obvious feeling or that sounds generic ("quality", "simplicity", "rigor", "usability").
- **Quick confirm** for values whose meaning is plain and uncontested: draft a definition from what they
  already said, read it back, and ask "Is that what you mean, or would you put it differently?"

### The sequence for a key value

Follow the order. Each step uses the maintainer's words; the agent drafts only at step 5.

1. **Open prompt, in their words.** "When you say `<Correctness>` on this project, what do you mean? Walk me
   through it." Let them talk. Follow up with "Say more about `<phrase they used>`." Laddering fits here:
   "Why does that part matter?"
2. **A concrete example each way.** "Can you think of a time it was done well here?" Then: "And a time it was
   missing, or only looked present, faked or ticked off without really being there?" Ask for real cases from
   this project when possible.
3. **The boundary.** "What do people call `<Correctness>` that you would not?" and "How is it different from
   `<neighbouring value>`?" Name the neighbours from the candidate list (for "Correctness", perhaps
   "Explicitness" or "Performance"). A repertory-grid style probe works well: "Of these three, which two
   belong together, and which is something else?" with the value and two neighbours.
4. **Too little and too much.** "What does too little `<Correctness>` look like in practice?" and "Can you have too
   much of it? What does that look like?" The second answer often becomes the `overdone` text of a polarity
   pole, and the first answer is `too_little`.
5. **Draft and read back.** Only now, the agent drafts the glossary entry from the maintainer's words:
   - a one-sentence `definition` in "The degree to which ..." or "How ..." form, operational enough that an
     observer could tell from an artifact whether there is more or less of it;
   - two to four observable `looks_like` indicators, taken from their good example and their description;
   - `too_little`, `not_to_be_confused_with` (naming the neighbours), and `too_much` if it is not already a
     pole's `overdone` text.

   Read it back: "Here is how I would write that down. What would you change?" Expect corrections; a
   definition the maintainer edits is better than one they merely accept.
6. **Keep their words.** Store the elaboration verbatim or near-verbatim in `in_own_words` (several sentences
   is normal), the examples in `examples.good` and `examples.missing_or_faked`, their handle in `by`, and the
   date in `confirmed`.

A maintainer who prefers writing can answer steps 1 to 4 in a `define` canvas widget (`canvases.md`), which
asks the same questions; the agent then does steps 5 and 6 in conversation.

### When the boundary splits a value

If step 3 or 4 shows one word covering two things ("correctness of the returned table" versus "correctness of the documentation"),
split it into two values with their own IDs and definitions before any weighing. Words that cover two
meanings are the commonest source of later contradictions. Ask: "It sounds like there are two things here,
`<A>` and `<B>`. Should we treat them separately?"

### Terms that are not values

Flip conditions and hard limits often depend on terms such as "public API", "identical results", "supported
platform" or "prototype". When one of these carries weight, define it briefly the same way (open prompt, an example,
the boundary) and record it in `glossary_terms`.

### On every later surface

From this point on, whenever the agent mentions a value in a question, a canvas, a read-back or a card, it
shows or quotes the confirmed one-line definition at first mention, and it uses the word only in that sense.
If the maintainer starts using the word differently, that is worth raising: "Earlier we defined `<Correctness>` as
`<definition>`. You seem to be using it a little differently now. Is this the same thing, or a second
meaning?"

## Step 4: shape each tension

For each candidate tension, settle what it is before asking where the project stands.

1. **Polarity or problem?** (from polarity management) "Is this something you settle once, or something you
   keep rebalancing?" and "If you leaned fully toward `<A>`, what would eventually go wrong?" A one-time
   problem with a right answer is a decision, not a tension; it may belong in an ADR or a hard limit instead.
2. **The acceptable-opposite test** (below). Both poles must be goods a reasonable project could choose.
3. **Two, three or more?** "Is there a third thing that gets squeezed whenever `<A>` and `<B>` are both
   pushed?" A third value makes a triad; four or more, or a group against a group, makes a network. Do not
   force everything into pairs, and do not inflate pairs into networks.
4. **Hard limit or tension?** The floor probe: "Is there any amount of `<B>` that would make you accept `<A>`
   falling below `<level>`?" A firm "no" marks a hard limit (a prohibition or a floor) rather than a weight.
   Keep hard limits few; check that each one truly has no acceptable opposite for this project.
5. **Inherent or contingent?** "Is this a true trade-off, or a current constraint that better tools could
   dissolve?" Record `necessity`. Contingent tensions deserve a `review_by` date.
6. **Mechanisms.** "Has the project found ways to get more of both?" (feature flags, escape hatches,
   experimental namespaces, release channels, a summary layer over a full record). Record them in
   `mechanisms`; agents proposing changes look there first.

## Step 5: retrospective walkthrough of a real decision

Real decisions reveal values that abstract talk hides. The technique adapts the Critical Decision Method,
a cognitive interviewing method built around four "sweeps" over one real incident.

**Sweep 1, choose and tell.** "Think of a recent decision where you had to give something up to get something
else, and where a newer contributor might have chosen differently. Tell it from start to finish." If the
setup step found ADRs, merged pull requests, or a methods section that records a choice, offer two or three as
options. Ask for at least one decision the maintainer now regrets, so the record is not only successes.

**Sweep 2, timeline.** "Let me read the sequence back. Where were the points where it could have gone another
way?"

**Sweep 3, deepen** at each decision point:

- Cues: "What did you notice that told you this mattered?"
- Goals: "What were you trying to protect? What were you trying to achieve?"
- Options: "What else did you consider? Why not that?"
- Uncertainty: "What were you unsure about at the time?"
- Levers: "Was there a single choice that moved several of these concerns at once?"

**Sweep 4, what if:**

- "What would have had to be different for you to choose the other option?" (a flip condition)
- "If the same situation came up today, would you decide the same way?" (tests whether the stance is stable)
- "What would a newcomer have done here, and what would have gone wrong?" (surfaces tacit rules)

**Walking through a recent feature (the review mode).** The same four sweeps work on a feature that just
shipped, read from its pull request, commits and discussion. Prepare by reading them first, then ask the
maintainer to narrate, and compare their account with the record. Each choice point becomes a precedent on
the relevant tension, marked `consistent`, `exception` or `flip`.

## Step 6: forced-choice scenarios

Abstract statements tend toward "both matter". Forced choices reveal the actual lean. Use them once the values
are defined, and show the definitions in the question or canvas.

**Placing a two-pole stance.** "Where does this project sit between `<A: definition>` and `<B: definition>`?
Strongly toward A, clearly toward A, slightly, balanced, slightly toward B ...?" Offer "it depends" as a
separate answer that leads straight to step 7. The spectrum canvas does this with no default handle.

**Three values.** "If you could have only two of `<A>`, `<B>`, `<C>` at full strength, which two? What is the
minimum acceptable level of the third?" Then, to place the point inside the triangle: "Split 10 points of
emphasis among the three." The triangle canvas does this on a 10 percent grid.

**Four or more values.**

- Swing weighting: "Imagine each of these is at its worst plausible level for this project: `<state each
  worst level concretely>`. You can raise one to its best. Which first? Which next?" Then: "Give the first
  swing 100 points. How many is each other swing worth compared with it?" Concrete ranges matter: a weight
  without a range ("how important is security?") is meaningless.
- Best-worst: show four or five values in a shuffled order. "Which matters most for this project? Which
  least?" Repeat with overlapping sets until each value has appeared about three times.
- Allocation: "You have 100 points of effort for the next release across these. Allocate them." The allocate
  canvas shows a running total that must reach 100; it never rebalances automatically.
- Ranking with a line: "Order these, and draw a line above which you would never trade." Values above the line
  are hard-limit candidates; confirm each with the floor probe.

**Dilemma scenarios.** Build realistic options from the project's own levers and precedents, stated as
concrete outcomes: "Option A: `<outcome on value 1, 2, 3>`. Option B: `<a different outcome>`. Which ships?"
Then always: "What would make you pick the other one?" Use situation-and-response phrasing where it helps:
"Under `<condition>`, when `<event>`, the project does `<observable response>`." A maintainer who says "that
would never happen" has told you the scenario was unrealistic; rebuild it from a real case.

## Step 7: flip conditions and early warnings

Every stance is a default. Ask two different questions.

- **Contextual flip:** "When would you lean the other way?" and "What would have to be true about a change for
  `<B>` to win here?" Push for observable conditions: not "when speed matters" but "when the compiled code is an
  optional extra with a pure-Python fallback that gives identical results". If two conditions could both apply, ask which wins.
- **Corrective flip (early warning):** "What early sign would tell you the project has gone too far toward
  `<A>`?" and "What would you do then?" Record `{toward, signal, response}`. Easy-to-collect signals are best.

If the maintainer has no flip condition, record an empty list. That is a real answer: the stance holds
everywhere, and agents will treat any lean the other way as a departure.

## Step 8: the seed library as a "did we miss anything?" check

Only after the maintainer's own list is recorded, show a handful of tensions from `tension-library.md`,
filtered by `project_types`. Present them as prompts:

- "Other projects of this kind often name tensions like these. Does any of them matter here in a way we have
  not covered?"
- Invite the maintainer to rename, split or reject any of them. A library tension adopted here gets the
  maintainer's wording and a glossary entry built through step 3, like any other.
- Mention that respected projects sit on both sides of most of them (Python's "one obvious way" against
  Unix's "distrust one true way"), so neither answer is the "right" one.

New tensions found here are usually parked for the next session rather than squeezed in.

## Step 9: contradiction checks

Contradictions are valuable. Most of them reveal an unstated flip condition or a word used in two senses.

**First, check the definitions.** Before treating two answers as conflicting, ask whether they used a value in
different senses: "When you chose the faster default in the large-file scenario, did 'correctness' mean the same
thing as in our definition, `<definition>`?" If not, the fix is in the glossary (a split value or a clearer boundary), not in
the stance.

**Ways to detect a contradiction:**

- Transitivity: A over B and B over C, but C over A.
- Cross-method: the abstract statement, the forced choice and the precedents point different ways.
- Precedent mismatch: a past decision leaned against the stated default without a recorded flip condition.
- Cross-tension: stances in two tensions imply opposite things for the same kind of change.

**How to raise one without leading:**

1. Describe both statements neutrally, in the maintainer's own words, without saying which is right: "Earlier
   you said `<X>`. In the scenario you chose `<Y>`. Both may be true."
2. Offer explanations as an open menu, not a verdict: "Is something different about the scenario? Are these
   really two different things under one word? Has your view shifted? Or does it genuinely depend on
   something?"
3. Wait. Do not suggest the resolution.

Record each in `contradictions` with a `resolution` of `new-condition`, `split-value`, `revised-stance`,
`elicitation-artifact` (the question was badly posed) or `open`. An open contradiction is fine; it stays
visible until a later session.

Run contradiction checks once there are enough stances to compare (usually from the second half of the first
session on), and never as a "gotcha". If the maintainer seems defensive, stop and acknowledge that tensions
between stances are expected; polarity management predicts oscillation between poles over time.

## Step 10: read back, write, render

1. Read back each tension touched this session in plain language: the definitions of its values, the stance
   summary, the flip conditions, the precedents. Correct anything the maintainer changes.
2. Ask about firmness for each stance: "Is this a working position you expect to evolve, a deliberate
   stance, or core to what the project is?" Use the scale in `data-model.md`.
3. Write `philosophy.json` (or the maintainer's individual file in a team). Fill `evidence.styles` with the
   styles that actually produced the stance, and set `evidence.level`.
4. **Draft or refresh the synthesis.** Write 3 to 5 plain sentences on what the project values and how it
   trades off, using value words only in their defined senses and no IDs or numbers. Read it back: "If someone
   read only this paragraph, would they understand the project the way you do? What would you change?" Record
   the confirmed text in `synthesis.text` and set `synthesis.as_of_version` to the file's version. In a team
   member's individual file, this is their own synthesis; the shared one comes from reconciliation.
5. Validate (the checklist in `data-model.md`) and regenerate the readable view and the map (`SKILL.md` has the
   command).
6. Update the session notes, and add an amendment-log entry if this session changed a confirmed philosophy
   (`amendments.md`). The first confirmed version gets entry `A0001`, which records adoption itself.
7. Suggest a commit message; commit only if the maintainer asks.

## The acceptable-opposite test

A tension is worth recording only if each side is something a reasonable project could prefer. The test comes
from Amazon's practice for writing tenets: "a tenet needs to have an opposite which could be acceptable to an
organisation."

Ask: "Could a respectable project choose the other side of this, for good reasons?"

- "Stability over velocity": passes. Many projects rightly choose velocity.
- "We value correctness": fails as stated. Nobody prefers incorrectness. Ask what correctness costs, and the
  real tension appears ("correctness proofs over shipping speed", "strict validation over accepting messy
  real-world input").
- "Never leak user data": fails as a tension because no one would accept the opposite. It is a hard limit.

The same test, run the other way, checks hard limits: if a maintainer can imagine accepting the opposite under
some pressure, it is a core stance, not a hard limit.

## Recording answers into the data model

| Source | Becomes |
|--------|---------|
| Mission, stakeholders, non-goals (step 1) | `mission`, value `stakeholders`, `non_goals`, `project_types` |
| Laddering (step 2) | Candidate values; `serves` links from means to ends |
| Triads (step 2) | Candidate tensions; each construct's two ends become poles |
| Define before you weigh (step 3) | A `values` glossary entry with `in_own_words`, `examples`, `by`, `confirmed`; or a `glossary_terms` entry |
| Polarity diagnosis and mapping (step 4) | `kind`, poles with `good` and `overdone`, `greater_purpose`, `deeper_fear`, `necessity`, `mechanisms` |
| Floor probe, never-trade line (steps 4, 6) | `hard_limits` |
| Retrospective sweeps (step 5) | `precedents` with `options_considered`, `would_have_changed_it`, `verdict`; candidate `flip_conditions`; `levers` |
| Spectrum placement (step 6) | Polarity `stance.position` |
| Pick-two and triangle (step 6) | Triad `stance.weights`, `pick`, `floors`, `posture` |
| Swing weights, allocation (step 6) | Network `stance.weights` (fractions summing to 1) |
| Best-worst, ranking (step 6) | Network `stance.priority` |
| Dilemma answers (step 6) | A precedent-like note on the tension, plus `flip_conditions` from "what would make you pick the other one?" |
| "When would you lean the other way?" (step 7) | `flip_conditions` |
| "What early sign ...?" (step 7) | `early_warnings` |
| Contradictions (step 9) | `contradictions`, and whatever the resolution changed |
| Firmness question (step 10) | `stance.firmness` |
| The styles that produced a stance | `evidence.styles`, `evidence.level`, short verbatim `evidence.quotes` |

Status: stances confirmed by a solo maintainer are `agreed`; stances in a team member's individual file stay
`provisional` until reconciliation.

## Saving resumable state

Interviews span sessions. After every tension, and at the end of every session, update
`individuals/<handle>/session-notes.md` (the folder layout is in `SKILL.md`). It is a plain Markdown file a
later session reads first.

```markdown
# Session notes: maintainer-b

## Sessions
- 2026-05-20 (45 min): orientation, own words, defined correctness/performance/portability/approachability;
  T01-T03 placed; one walkthrough (the v2.1 ambiguous-date error). Canvases used: spectrum x3.

## State
- Confirmed: T01@1, T02@1, T03@1; values correctness@1, performance@1, portability@1, approachability@1.
- Drafted, not yet confirmed: T04 (weights placed; flip condition unclear).
- Candidate tensions not yet discussed: "release cadence vs. stability", "streaming API vs. whole-file reads".
- Seed-library check: not yet run.
- Open contradictions: X01 (correctness first, but chose the faster default in the large-file dilemma).

## Next session
1. Finish T04: ask the flip question; walk through the read_chunks() decision.
2. Define "explicitness" in full (only quick-confirmed so far).
3. Run the seed-library check.

## Parked (not philosophy work)
- "We should publish benchmark numbers with each release" (feature idea, mentioned during T02).

## Interviewer notes
- Prefers talking to canvases for two-pole tensions; liked the triangle.
- Has read the shared PHILOSOPHY.md: no (matters for team anchoring).
```

The JSON carries the confirmed state; the notes carry the process state. Together they let any later session,
or a different agent, resume without asking the maintainer to repeat themselves.

## Starting from a seed drafted from documents

When a project has substantial documentation, the agent can draft a seed before the first session: candidate
values with draft definitions, tensions with inferred stances, hard limits, and precedents taken from ADRs or
changelogs. Rules for a seed:

- Mark it clearly: `status_note` says it is inferred and unconfirmed, every tension is `provisional`, every
  value has `in_own_words: null` and no `confirmed` date, and `evidence.styles` is `["inferred-from-docs"]`.
- Do not show the seed before step 2. The maintainer's own words come first; the seed is used afterwards as a
  checklist, like the tension library, and as a source of real decisions for walkthroughs.
- Confirm each inferred value through step 3 (the maintainer's elaboration replaces the drafted definition
  where they differ) and each inferred stance through at least one other style before marking it `agreed`.
- Report honestly which parts of the confirmed philosophy came only from documents.

## Wording for different kinds of project

The techniques are the same; the nouns change. Swap examples to match the project.

| Project | "A recent decision" might be | Useful dilemma material | Typical stakeholders |
|---------|------------------------------|-------------------------|---------------------|
| Library or language | An API change, a deprecation, a new dependency | Breaking change versus a long deprecation; a convenient default versus explicitness | Downstream developers; their end users |
| Application | A feature cut, an onboarding change, a performance fix | Ship the feature now versus polish; a setting versus an opinionated default | Users; operators; support staff |
| Package manager or platform | A resolver rule, a lockfile format, a registry policy | Strict resolution versus accepting the existing ecosystem; reproducibility versus staying current | Package authors; installers; security teams |
| Research project | A sampling decision, a pre-registration deviation, an instrument choice | Generalisability versus control; open data versus participant protection | Participants; other researchers; funders; policy readers |
| Data analysis | A method choice, an exclusion rule, a deadline trade-off | Interpretability versus predictive accuracy; a timely answer versus a thorough one | Decision-makers; the people the data describes; reviewers |
| Documentation or teaching | A section cut, a simplification, a recommended path | Completeness versus approachability; one recommended path versus neutral coverage | Learners; experts; maintainers |

## Pitfalls

| Pitfall | What it looks like | Remedy |
|---------|-------------------|--------|
| Leading questions | "Wouldn't you say reliability matters most?" | Ask "what matters most?" with no candidate named. |
| Anchoring | The agent's first example or a default slider position becomes the answer. | Never offer a number first; canvases start with no handle; offer examples pointing in different directions. |
| Framework vocabulary leaking in | The maintainer starts saying "polarity" and "swing weight". | Keep framework names out of questions; use the maintainer's words. |
| Socially desirable answers | Everything matters; quality is top. | Force a choice, use concrete scenarios, ask for a real example. |
| Means recorded as ends | "Fast CI" listed as a core value. | Ladder up: "why does that matter?" |
| Splitting bias | Five flavours of "rigor" and one of "speed" make rigor look weightier. | Keep values at a similar level of detail; record facets as children. |
| Order effects | The first value listed gets ranked first. | Shuffle the order in every ranking, best-worst or allocation task. |
| Hindsight | A past decision retold as if it had been obvious. | Ask what was uncertain at the time, and for a decision now regretted. |
| One story becomes a rule | A memorable incident turns into a sweeping stance. | Ask whether it would decide the same way today, and for a second case. |
| False precision | A stance recorded as -0.73. | Store rough values; say "strongly toward" rather than a number in read-backs. |
| Catching out | The contradiction check feels like a trap. | Present both statements neutrally, offer an open menu of explanations, accept "open". |
| Undefined words | "Simple" means four things across four answers. | Define before you weigh; recheck the definition when answers conflict. |
| Interviewer fatigue or maintainer fatigue | Answers shrink; "whatever you think". | Pause and save state. |
| Scope creep | The session turns into feature planning. | Park the idea in the session notes and return to the philosophy. |
| Team anchoring | A second maintainer has read the first one's answers. | Interview separately; record in the notes whether they had read the shared file. |
