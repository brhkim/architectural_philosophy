# Decision cards

How an agent uses the philosophy when it proposes or reviews a change. The decision card is a short, fixed
format that says which of the project's trade-offs a proposal touches, which way it leans on each, whether that
fits the recorded stance, and what the human needs to decide. This file also defines the proposal JSON that
overlays a proposal on the map page, the strictness levels, and when to skip the card.

## Contents

- The contract in one paragraph
- Bottom line first, and keep it short
- Before writing a card: read, then check hard limits first
- When to write a card, and when to skip it
- The card template
- Field rules
- Verdicts
- Using values and their definitions in a card
- Strictness levels and what they change
- The proposal JSON (map overlay)
- Reviewing someone else's change
- When a stance no longer fits
- Converting a card into an ADR
- Worked example: rowfold, a required C extension or an optional fast parser

---

## The contract in one paragraph

When a proposal touches one or more tensions in the philosophy, the agent reads the current file, checks the
hard limits first, and writes a card that opens with a two-to-four-sentence "Bottom line" and then names each touched tension by ID and revision (`T01@1`), quotes the
one-line definitions of the values involved, gives one of three verdicts per tension (Consistent, Departs, Flip
condition met), lists the options including doing nothing, and ends with the decision the human needs to make.
The philosophy is advisory by default: the card informs; the human decides. The agent never invents a stance
the file does not contain, never uses a value word in a sense its definition excludes, and never silently
overrides a recorded stance.

## Bottom line first, and keep it short

Every card opens with a **Bottom line** paragraph of 2 to 4 plain sentences, written for a reader who reads
nothing else. It says what is proposed, how it fits the philosophy overall (consistent, departs, or needs a
decision), and the one decision needed, or that none is needed. Everything after it is supporting detail.

Then stay brief:

- List only the tensions the proposal actually touches, with one line of reason each.
- Put the details (the options, precedents, the departure explanation) after the table, and only the ones that
  matter for the decision.
- Do not restate the philosophy; cite it.

**When writing by hand** (no scripts, a Markdown card or a hand-written `PHILOSOPHY.md`), follow the same
design intent as the generated pages: summary first, detail later or collapsed (for example in a
`<details>` block where the reader's tool renders one), plain text over decoration, few headings, no badges,
emoji or colour cues standing in for words. A calm page that a reader can stop reading after the first
paragraph is the goal.

## Before writing a card: read, then check hard limits first

1. **Read the current philosophy,** not a remembered version. Prefer the generated `PHILOSOPHY.md` for prose and
   `philosophy.json` for exact revisions, positions and definitions. Note the document `version` and the
   `strictness` setting.
2. **Check the hard limits before anything else.** Hard limits are not traded. If the proposal would cross one,
   say so at the top of the card, mark it in `hard_limits_at_risk`, and stop for a decision at every strictness
   level. The only ways forward are to change the proposal or to amend the philosophy (which, for a hard limit,
   usually needs every active maintainer).
3. **Find the touched tensions.** A proposal touches a tension when it moves the project along that tension's
   axis, or when it chooses between options that sit at different poles. Look at `levers` and `mechanisms`
   first: a known lever tells you which values move, and a known mechanism may let the proposal get more of both.
4. **Look up the precedents** on each touched tension. They show how the stance has actually been applied.

## When to write a card, and when to skip it

Write a card when:

- the agent proposes a feature, refactor, dependency, workflow change or design direction that touches at least
  one tension;
- the user asks "why" about a design choice, or asks for a review against the philosophy;
- strictness is above advisory and the work in progress touches a tension (see the table below).

Skip the card, and say so in one line ("No philosophy tensions touched."), when:

- the change is mechanical or local (a typo, a rename, a test for existing behaviour, a version bump that changes
  nothing a tension describes);
- the change touches no tension, even though it is large;
- a card for the same proposal and the same philosophy version already exists in the conversation or the PR.

A card that would merely restate "consistent with everything" for a small change is noise. A design document
that does not discuss trade-offs is not worth writing, and neither is a card that has none.

## The card template

Keep the order fixed so a reader can scan any card the same way. Aim for about fifteen lines of rendered text;
never pad to fill the template, and omit the "If this departs" block when every verdict is Consistent. The
Bottom line always comes first.

```markdown
#### Decision card: <short noun phrase naming the proposal>

**Bottom line:** <2 to 4 plain sentences: what is proposed, how it fits the philosophy overall, and the one
decision needed (or "No decision needed").>

**Philosophy:** <path> v<version> · **Strictness:** <effective level for this proposal>

**Hard limits:** <"None at risk." or "H1 at risk: <why>." Always first.>

**In one sentence:** In the context of <feature or component>, facing <tension names with IDs>,
I propose <option> over <the strongest alternative>, to gain <values favoured>, accepting <values given up>.

**Values involved:** <value>@<rev>: "<one-line glossary definition>"; <value>@<rev>: "<definition>"

**Tensions touched**

| Tension | Project stance | This proposal | Verdict |
|---------|----------------|---------------|---------|
| T02@2 Portability vs. raw speed | Portability first (firm) | Leans performance: adds compiled code as an optional extra | Flip condition met: "<quote>" |
| T04@1 Approachability, performance, correctness | Correctness first, then approachability | Same output, faster | Consistent |

**Options** (at least two, including doing nothing)
- **<Option A, proposed>:** Good, because ...; Bad, because ...
- **<Option B, closest to the stance>:** Good, because ...; Bad, because ...
- **Do nothing:** what happens if we don't.

**Precedents:** follows P04; differs from P07 because ...

**If this departs from a stance:** why this case is different; whether a flip condition is met (quoted) or
whether this is really a proposed amendment; which consistent alternative was set aside and why.

**Decision needed:** <"None; proceeding (advisory)." or one specific question>

**Confidence and open questions:** <what the agent is unsure of, such as a tension it could not classify>
```

## Field rules

0. **The Bottom line comes first** and stands alone: what is proposed, the overall fit, the one decision
   needed. Plain words, no IDs needed there (they follow in the table), value words in their defined senses.
   Its overall fit matches the `overall` field of the proposal JSON.
1. **The one-sentence summary is a Y-statement** (Olaf Zimmermann's six-part decision sentence), phrased as a
   proposal: "I propose ... over ...". It must make sense on its own.
2. **Cite tensions as `ID@rev`** (`T04@2`) and values as `id@rev` (`correctness@1`), and put the document version
   in the header. A card citing `T04@2` when the file has moved to `T04@3` is visibly stale.
3. **Read stances from the current file,** quoting the stance summary or paraphrasing it closely. Never fill
   in a stance from general knowledge or from another project.
4. **Say which values gain and which give up,** by name, not "left" and "right". For a triad or network, list
   them: "gains Batteries included and Approachability; gives up Small core".
5. **Use "gain" and "give up" (or "favour" and "accept")** for direction. Avoid "violates": trade-offs are not
   rules. Reserve "conflicts with" for hard limits.
6. **Options include doing nothing and at least one option at the stance's preferred pole,** so a departure is
   always weighed against the consistent alternative.
7. **Precedents illustrate; they do not decide.** Cite as "follows P04" or "differs from P07 because ...".
8. **Self-check before showing the card:** Are the hard limits checked? Are there at least two real options? Was
   every stance read from the current file? Is every departure explained? Is there exactly one clear question
   for the human, or an explicit "none"?
9. **Permission to question.** Any card may end with "This stance may no longer fit because ...; consider an
   amendment." The philosophy holds unless the maintainers know better; an agent that sees a mismatch says so
   rather than adding workarounds to obey an outdated stance.

## Verdicts

Use exactly one per touched tension. Never "partially aligned".

| Verdict | Meaning | JSON value |
|---------|---------|------------|
| **Consistent** | The proposal leans where the stance leans (or stays within its weights or priority). | `"consistent"` |
| **Departs** | The proposal leans the other way, and no flip condition applies. | `"departs"` |
| **Flip condition met** | The proposal leans the other way, and a recorded flip condition applies. Quote it. | `"flip_condition_met"` |

Special cases:

- **Contested tension** (status `contested`): there is no stance to be consistent with. Present the recorded
  positions side by side and ask; use verdict `departs` only against a named position, and say so.
- **Provisional tension:** give the verdict but label the stance provisional.
- **Scoped tension:** use the stance for the subsystem the change touches; if the scope is unclear, ask its
  owner.
- **Firmness and evidence:** a core stance with weak evidence is cited as "the maintainer's stated position, not
  yet tested against a real case"; a working stance is cited as "current practice, expected to evolve".

## Using values and their definitions in a card

- At first mention in a card, quote the value's one-line glossary definition (the "Values involved" line), so
  the card explains itself to a reader who has not opened the philosophy.
- Use each value word only in the sense its definition gives. If the proposal needs a different sense ("correctness"
  meaning test coverage, when the glossary defines it as returned tables matching what the file holds), do not
  stretch the word. Either use a different, defined word, or say plainly that the glossary lacks this sense and
  propose a glossary amendment (`amendments.md`).
- Respect `not_to_be_confused_with`. If the glossary says Correctness is not Explicitness ("though explicit
  arguments help"), a card must not use them interchangeably.

## Strictness levels and what they change

The project sets a default level and may raise it for particular stances (`strictness` in `data-model.md`).
The effective level for a proposal is the strictest of: the project level, any `by_firmness` or `by_tension`
level of a touched tension, and `flag-and-ask` whenever a hard limit is at risk or a touched tension is
contested.

| Level | When a card is produced | What happens on Departs |
|-------|------------------------|--------------------------|
| **advisory** (default) | For significant proposals and when the user asks why | The agent states the departure and its reason, and proceeds if the user's instruction already covers it. |
| **flag-and-ask** | Before implementing anything that touches a tension | The agent stops and asks the "Decision needed" question; nothing proceeds without a yes. |
| **review-gate** | Always, and the card is saved with the change (PR description, design doc, ADR) | Implementation waits until a human approves the departure in writing, or the stance is amended through the amendment workflow. |

Why the levels are principled rather than arbitrary:

- **Advisory by default** because the philosophy records judgment, not law, and agents tend to apply recorded
  decisions more rigidly than people do. The default asks the agent to explain, not to block.
- **Raising strictness by firmness** follows the stakes: a core stance is one the maintainers would resist
  changing, so a departure deserves a human's eyes.
- **Hard limits and contested tensions always stop** because an agent has no legitimate way to resolve them on
  its own: one is not tradeable, and the other has no agreed answer.
- **Honesty about enforcement:** these levels are a contract the agent follows. They become a hard gate only if
  the team adds a check of its own (a CI step that looks for a card in the PR description, for example). Say so
  when a user chooses review-gate.

Explicit instructions from the user in the conversation take precedence over the philosophy, except that the
agent still names a hard limit at risk before acting.

## The proposal JSON (map overlay)

The map page can overlay a proposal, drawing where it would push each touched tension. Write the proposal as
JSON and pass it to the renderer (`--proposal`, see `SKILL.md`), or paste it into the map page's "Overlay a
proposal" box.

```json
{
  "schema": "architectural-philosophy-proposal/0.1",
  "title": "Short noun phrase naming the proposal",
  "bluf": "Two to four plain sentences: what is proposed, how it fits overall, and the one decision needed.",
  "overall": "needs_decision",
  "summary": "One or two sentences.",
  "philosophy_version": "1.1.1",
  "touched": [
    {"id": "T01", "rev": 1, "position": 0.3,
     "verdict": "departs", "reason": "Why this verdict."},
    {"id": "T04", "rev": 1, "weights": {"Approachability": 0.3, "Performance": 0.3, "Correctness": 0.4},
     "verdict": "flip_condition_met",
     "flip_condition": "The quoted flip condition.", "reason": "Why it applies."},
    {"id": "T06", "rev": 1, "priority": ["Small core", "Compatibility", "Approachability", "Batteries included"],
     "note": "Free text for any kind.", "verdict": "consistent", "reason": "..."}
  ],
  "hard_limits_at_risk": [{"id": "H1", "reason": "..."}],
  "decision_needed": "The one question the human must answer."
}
```

| Field | Meaning |
|-------|---------|
| `schema` | `"architectural-philosophy-proposal/0.1"`. |
| `title`, `summary` | The proposal in a phrase and in one or two sentences. |
| `bluf` | Bottom line up front: 2 to 4 plain sentences covering what is proposed, how it fits the philosophy overall, and the one decision needed. Shown first on the map; the same text as the card's "Bottom line". |
| `overall` | Optional overall fit: `consistent` (every verdict consistent or flip condition met, no hard limit at risk), `departs` (at least one departure, no hard limit at risk, and the effective strictness lets the agent proceed with an explanation), or `needs_decision` (a hard limit at risk, a contested tension touched, or the effective strictness requires a human yes). |
| `philosophy_version` | The document version the card was checked against; the map warns if it differs. |
| `touched[].id` | Tension ID without the revision (`"T01"`), so the map can match it. Put the revision in `rev`. |
| `touched[].position` | Polarity: where the project would sit if the proposal shipped, from -1 (toward `poles[0]`) to +1. |
| `touched[].weights` | Triad: the implied shares, summing to 1. |
| `touched[].priority` | Network: the ordering the proposal implies, if it changes one. |
| `touched[].note` | Free text, for any kind (often the only useful field for a network). |
| `touched[].verdict` | `consistent`, `departs` or `flip_condition_met`. |
| `touched[].flip_condition` | The quoted flip condition, when the verdict is `flip_condition_met`. |
| `touched[].reason` | One sentence explaining the verdict. |
| `hard_limits_at_risk` | `[{id, reason}]`, or plain IDs. Empty list when none. |
| `decision_needed` | The one question for the human, or `"None"` at advisory with only consistent verdicts. |

Positions and weights in a proposal are as rough as the stances themselves. They show direction and rough
size, not a measurement. Save proposal files beside the change they describe (for example
`<philosophy folder>/proposals/2026-11-20_optional-fast-parser.json`) if the team wants to keep them.

## Reviewing someone else's change

The same card works for review. Read the diff and the description, identify touched tensions from what the
change does (not from what the description claims), and write the card with "This change ..." in place of "I
propose ...". In the options, "Do nothing" becomes "Do not merge". For a contributor who has not read the
philosophy, link the relevant tensions and quote their definitions; the card doubles as an introduction.

## When a stance no longer fits

If the agent sees that following a stance would produce a poor result here, it says so in the card instead of
contorting the proposal to obey. The card's last line can propose an amendment: what the new flip condition or
stance might be, and the precedents that support it. If departures from the same stance keep being approved
for the same reason, that pattern is itself a proposed amendment (`amendments.md`). The agent never edits the
philosophy as a side effect of feature work; amendments are a separate, explicit step.

## Converting a card into an ADR

When a card leads to a durable decision and the project keeps architecture decision records, the card maps
directly onto common ADR templates (Nygard, MADR):

- the one-sentence summary becomes the decision summary;
- the tensions table becomes the "Decision Drivers" list, one bullet per tension, for example
  `* T02@2 Portability vs. raw speed (portability first; compiled extras welcome when optional)`;
- the options become "Considered Options" with their good and bad points.

Then add the ADR to the touched tensions' `precedents` with a `link`, which records the case for future cards.

---

## Worked example: rowfold, a required C extension or an optional fast parser

This example uses rowfold, a fictional pure-Python library for reading tabular files that many downstream
projects depend on. Its philosophy (version 1.1.1, advisory, with core stances at flag-and-ask) and both
proposal files ship in the skill repository's `examples/rowfold/` folder, with rendered review pages. A
contributor opens a pull request whose agent rewrote the core parser as a required C extension, about ten
times faster on large files. A maintainer asks their own agent to review it against the philosophy.

#### Decision card: core parser rewritten as a required C extension

**Bottom line:** This change replaces rowfold's pure-Python parser with a required C extension for about ten
times the speed. The speed is welcome, but making compiled code mandatory goes against the portability-first
stance and breaks the promise that installing rowfold never needs a compiler. The same speed-up fits the
philosophy as an optional extra with the pure-Python parser kept as the fallback. Decision needed: ask the
contributor to reshape it that way?

**Philosophy:** `docs/philosophy/philosophy.json` v1.1.1 · **Strictness:** flag-and-ask (a hard limit is at
risk; the project default is advisory)

**Hard limits:** H1 at risk. "pip install works everywhere we support, with no compiler required: installing
rowfold succeeds on every supported Python version and platform from a pure-Python wheel." Platforms without a
prebuilt wheel (a new Python release, musl or Alpine, Pyodide, less common CPUs) would need a C compiler.

**In one sentence:** In the context of the core parser, facing T02 Portability vs. raw speed and T04
Approachability, performance, correctness, this change chooses a required compiled parser over an optional one
with a pure-Python fallback, to gain Performance, giving up Portability and the independent check on
Correctness.

**Values involved:** portability@1: "The range of Python versions, operating systems, CPU architectures and
runtimes on which rowfold installs and gives the same results without extra tools." performance@1: "How
quickly, and within how little memory, rowfold reads and transforms large files on a single machine."
correctness@1: "The degree to which every table rowfold returns matches what the file actually holds, or
rowfold raises a clear error instead of returning a guess."

**Tensions touched**

| Tension | Project stance | This change (required C extension) | Reshaped: optional `rowfold[fast]` |
|---------|----------------|-----------------------------------|------------------------------------|
| T02@2 Portability vs. raw speed | Portability first (-0.5, firm) | Departs: compiled code becomes required and the pure-Python parser is removed | Flip condition met: "Compiled code is welcome as an optional extra with a pure-Python fallback that gives identical results." |
| T04@1 Approachability, performance, correctness | Correctness 50%, approachability 30%, performance 20% (firm) | Departs: with the reference parser gone, nothing independent checks the C parser's output | Consistent: both parsers must give identical output on the full test corpus |
| T03@1 Small core vs. batteries included | Small core (-0.7, firm) | Not touched | Consistent: the compiled code ships as an extra, so the core install gains no dependency |

**Options**

- **Merge as is:** Good, because every user gets the speed with no extra step; Bad, because it crosses H1, and
  the C parser becomes its own reference.
- **Reshape as an optional `rowfold[fast]` extra (closest to the stance):** Good, because users who want speed
  get it with one install flag, while plain installs and the reference parser stay unchanged; Bad, because two
  parsers must be kept in step, and users without the extra stay slow.
- **Do not merge:** nothing is at risk, and users with large files keep waiting, the downside T02's
  portability pole warns about.

**Precedents:** the reshaped option follows "Optional [zstd] compression extra (v2.3)", where compiled code
arrived as an opt-in extra and the standard-library path kept working without it. Merging as is would be the
first required compiled dependency.

**If this departs from a stance:** the change as submitted departs from two firm stances and crosses H1, so it
could only proceed through an amendment that every active maintainer endorses, not through this card. The
reshaped option departs from nothing; it is the case T02's flip condition was written for.

**Decision needed:** Ask the contributor to reshape it as an optional extra with a pure-Python fallback?

**Confidence and open questions:** The speed-up is the contributor's own measurement. "Identical results" is
defined in `glossary_terms` (byte-for-byte equal tables, column types, missing-value markers and error messages
on the full test corpus), so the reshaped version has a concrete test to pass.

The contributor's change as a proposal file (`proposals/required-c-extension.json` in the example):

```json
{
  "schema": "architectural-philosophy-proposal/0.1",
  "title": "Rewrite the core parser as a required C extension",
  "summary": "A contributor's agent proposes rewriting rowfold's core parser in C, as a required compiled extension, for about ten times the speed on large files. (Example package.)",
  "bluf": "A contributor's agent proposes replacing rowfold's pure-Python parser with a required C extension for about ten times the speed. The speed is welcome, but making compiled code mandatory goes against the portability-first stance and breaks the promise that installing rowfold never needs a compiler. Decision needed: ask the contributor to reshape it as an optional extra with a pure-Python fallback?",
  "overall": "needs_decision",
  "philosophy_version": "1.1.1",
  "touched": [
    {"id": "T02", "rev": 2, "position": 0.8, "verdict": "departs",
     "reason": "Compiled code becomes required and the pure-Python parser is removed; the flip condition welcomes compiled code only as an optional extra with a pure-Python fallback, so it does not apply."},
    {"id": "T04", "rev": 1, "weights": {"Approachability": 0.15, "Performance": 0.55, "Correctness": 0.3},
     "verdict": "departs",
     "reason": "With the reference parser gone, nothing independent checks the new C parser's output, so performance gains weight at correctness's expense."}
  ],
  "hard_limits_at_risk": [
    {"id": "H1", "reason": "Platforms without a prebuilt wheel (a new Python release, musl or Alpine, Pyodide, less common CPUs) would need a C compiler to install rowfold."}
  ],
  "decision_needed": "Ask the contributor to reshape it as an optional extra with a pure-Python fallback?"
}
```

The reshaped version (`proposals/optional-fast-parser.json`), whose card would open with this bottom line and
carry the right-hand column of the table above:

```json
{
  "schema": "architectural-philosophy-proposal/0.1",
  "title": "Optional compiled fast parser (rowfold[fast])",
  "summary": "Add an optional compiled parser, installed with \"pip install rowfold[fast]\", with the pure-Python parser as the fallback, and test both for identical output. (Example package.)",
  "bluf": "Add an optional compiled parser, installed with \"pip install rowfold[fast]\"; rowfold uses it when present and falls back to the pure-Python parser otherwise, and one shared test suite checks that both give identical output. This is the case the philosophy already welcomes, compiled code as an optional extra with an identical-results fallback, so plain installs and correctness are untouched. Decision needed: approve the optional [fast] extra?",
  "overall": "consistent",
  "philosophy_version": "1.1.1",
  "touched": [
    {"id": "T02", "rev": 2, "position": 0.2, "verdict": "flip_condition_met",
     "flip_condition": "Compiled code is welcome as an optional extra with a pure-Python fallback that gives identical results.",
     "reason": "The compiled parser is opt-in, the pure-Python parser stays the default and the reference, and the shared test suite checks identical results on every release."},
    {"id": "T04", "rev": 1, "weights": {"Approachability": 0.3, "Performance": 0.25, "Correctness": 0.45},
     "verdict": "consistent",
     "reason": "Correctness stays protected first: both parsers must produce identical output on the full test corpus before any release."},
    {"id": "T03", "rev": 1, "position": -0.6, "verdict": "consistent",
     "reason": "The compiled code ships as an extra, so the core install gains no dependency."}
  ],
  "hard_limits_at_risk": [],
  "decision_needed": "Approve the optional [fast] extra?"
}
```

Overlaying both on the map shows the difference at a glance: the required extension pulls T02 far toward
Performance and flags H1, while the optional extra stays near the stance.
