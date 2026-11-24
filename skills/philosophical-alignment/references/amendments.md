# Amendments and versioning

How the philosophy changes over time without losing its history or its clarity. Stances and definitions are
expected to change as a project grows; what matters is that every change is explicit, explained, dated and
findable, and that the text agents read always carries only today's ruling.

## Contents

- Three layers that change differently
- What counts as an amendment
- Revision numbers: tensions, values, hard limits
- The document version (major, minor, patch)
- The amendment log (`AMENDMENTS.md`)
- The amendment workflow
- How agents propose amendments
- When repeated departures suggest an amendment
- Splits, merges and retirements
- Git practice
- Review dates

---

## Three layers that change differently

| Layer | Examples | Rule |
|-------|----------|------|
| **Current text** | The synthesis; glossary definitions; each tension's poles, stance, flip conditions and summary; hard limits | Rewritten in place. Carries only the current ruling, with its revision number. |
| **Precedents** | "P04: ambiguous dates raise an error (v2.1)" | Append-only. May be annotated ("superseded as an illustration by P09") but not deleted. |
| **Amendment log** | Dated entries describing each substantive change | Append-only. Never rewritten, except to fill in a commit hash afterwards. |

Agents load the current text by default, read precedents when building a decision card, and read the log only
when asked about history or when amending. This keeps what an agent reads small and current. Agents given every
past argument tend either to apply obsolete rulings rigidly or to bury the current one in history.

## What counts as an amendment

An amendment is any change to the current text that changes meaning, plus the adoption of the philosophy
itself. Wording fixes and typo corrections are still logged (as patch entries) so the log stays complete, but
they do not change revision numbers.

Feature work never amends the philosophy as a side effect. An amendment is always its own explicit step, even
when a feature discussion prompted it.

## Revision numbers: tensions, values, hard limits

Each tension, value and hard limit carries a `rev` integer, starting at 1.

**A tension's `rev` increments** when the stance moves; a flip condition or early warning is added, removed or
changed in meaning; the poles or value set change; firmness changes; or the status changes between shared
states (for example `contested` to `consented`). It does not increment for wording that keeps the meaning.

**A value's `rev` increments** when its definition changes meaning: the boundary moves, an indicator is added
or removed that the old definition excluded or included, or a facet is split off. Clarifying words that keep
the meaning do not increment it. A definition change does not by itself bump the revisions of the tensions that
use the value; cards cite both (`T04@1` with `correctness@2`).

**A hard limit's `rev` increments** when its text changes meaning.

Citation forms: `T04@2` for a tension, `correctness@2` for a value, `H1@1` for a hard limit. These are what decision
cards, ADRs, pull requests and code comments cite, so a reader can tell which ruling applied at the time.

## The document version (major, minor, patch)

`version` in `philosophy.json` is `MAJOR.MINOR.PATCH`. The rules are adapted from GitHub Spec Kit's versioning
of its "constitution" documents, applied to tensions and definitions.

| Bump | When | Why |
|------|------|-----|
| **MAJOR** | A stance reversed (it now leans toward the other pole, or a different value leads); a tension or value retired, split or merged; a hard limit added, removed or changed in meaning; a value's definition changed so much that earlier citations would read differently; the default strictness raised. | Earlier decision cards may no longer hold. |
| **MINOR** | A new tension or value; a stance moved without reversing; a flip condition added or changed; a definition's boundary refined; firmness changed; a new precedent that sharpens a stance; a status change after reconciliation. | Earlier cards still hold but may be incomplete. |
| **PATCH** | Wording, clarifications that keep meaning, typos, new precedents that only illustrate. | Nothing a card relies on changed. |

When the bump type is unclear, the agent explains its reasoning and the maintainers decide.

Before the first confirmed interview, a seed stays at `0.x`. The first version a maintainer confirms becomes
`1.0.0`, and its log entry `A0001` records adoption itself (who adopted it, under what strictness), the way the
first record of a decision-record system often records the decision to keep records.

Also update `last_amended` (and `ratified` on adoption).

## The amendment log (`AMENDMENTS.md`)

One append-only Markdown file in the philosophy folder. Newest entries at the bottom. Each entry, shown here
for the amendment behind version 1.1.0 of the rowfold example (the PR numbers are illustrative):

```markdown
### A0002 · 2026-09-14 · v1.0.0 → v1.1.0 (MINOR)
- **Changed:** T02 (@1 → @2)
- **Change type:** revise-stance
- **Before:** Pure Python only; speed comes from better algorithms.
  Flip condition: an optional compiled extra may be accepted when a pure-Python fallback gives identical
  results.
- **After:** Portability first: the pure-Python parser is the reference. Compiled extras are welcome when
  optional. Flip condition: compiled code is welcome as an optional extra with a pure-Python fallback that
  gives identical results.
- **Trigger:** Three optional compiled extras shipped without problems, starting with [zstd] in v2.3; each
  was approved under the flip condition.
- **Rationale:** The exception had become the normal case, so the stance should say so.
- **Ratified by:** maintainer-a, maintainer-b (agreed). **Dissent recorded:** none.
- **Impact:** Cards and ADRs citing T02@1: PR #212, #230, #241 (found by searching for "T02@").
  Re-check suggested: no; they remain consistent.
- **Synthesis:** refreshed to say compiled code is welcome only as an optional extra (as_of_version → v1.1.0).
- **Commit:** (filled after commit)
```

Change types: `adopt`, `add` (a new tension, value or hard limit), `revise-stance`, `reverse`,
`add-flip-condition`, `change-flip-condition`, `add-early-warning`, `define` (a new glossary entry),
`redefine` (a value's meaning changed), `clarify` (wording only), `add-precedent`, `change-firmness`,
`change-status`, `split`, `merge`, `retire`, `change-strictness`, `reconcile` (the outcome of a reconciliation
cycle, with a link to its folder).

For a definition change, Before and After quote the old and new `definition` (and `not_to_be_confused_with`
if it changed), and `in_own_words` records whose words the new version follows.

Mirror each entry as a one-line index in the JSON: a top-level `amendment_log` row (`version`, `date`,
`summary`, and optionally `id`, `change_type`, `tensions`, `ratified_by`), plus a per-tension or per-value
`amendments` row (`{rev, date, summary}`). The JSON rows let the map page show a timeline; the Markdown entry
holds the reasoning.

The "Impact" line is produced by searching the repository for the ID with an `@` (for example `T02@`). Stable
IDs make that search reliable.

## The amendment workflow

1. **Propose.** From an interview, a decision card ("this stance may no longer fit"), a maintainer, or a
   reconciliation cycle. Write it as a delta: Before, After, Rationale.
2. **Keep scope.** Any feature work mentioned along the way is noted as a next action and not started.
3. **Check definitions.** If the change uses a value word, confirm it is used in its glossary sense; if the
   change is really about what a word means, make it a definition amendment.
4. **Decide the version bump.** Explain the reasoning when it is ambiguous.
5. **Ratify.** A solo maintainer says yes. A team applies the decision rule in its governance agreement
   (`reconciliation.md`); every objection is addressed, though not necessarily accommodated, and dissent is
   recorded. "Merging the pull request ratifies it" is a convenient option for teams that work through pull
   requests.
6. **Apply.** Rewrite the current text, bump `rev` and `version`, update `last_amended`, append the log entry,
   add the JSON index rows.
7. **Refresh the synthesis.** Every amendment includes this step. If the change touched a stance, a hard limit
   or a definition, redraft `synthesis.text` so it still tells a newcomer the truth in 3 to 5 plain sentences,
   read it back for confirmation, and set `synthesis.as_of_version` to the new version. For other changes,
   confirm the text still holds and update `as_of_version`. Record which happened on the entry's "Synthesis"
   line. Then regenerate `PHILOSOPHY.md` and the map.
8. **Suggest a commit message,** for example `docs(philosophy): T02@2, v1.1.0 (compiled extras welcome when
   optional)`. Commit only when the user asks; fill in the entry's commit hash afterwards if they do.

## How agents propose amendments

An agent proposes, it never applies on its own. A proposal is short:

```markdown
**Proposed amendment to T03@1 (Small core vs. batteries included)**
- **Before:** flip condition "An integration may move into the core when it needs nothing beyond the standard
  library and most downstream users already rely on it."
- **After (proposed):** add a flip condition: "A reader for a format the standard library already parses may
  live in the core even before most users rely on it."
- **Why:** three recent requests (issues #88, #91, #97) asked to read SQLite tables, which needs only the
  standard library's `sqlite3` module, but few users rely on it yet.
- **Version bump:** MINOR (new flip condition).
- **Decision needed:** adopt, revise, or decline?
```

If the maintainers decline, record the decision in the log as a declined proposal (change type with
"(declined)", no version bump) so the same idea is not re-proposed without new reasons. A later proposal that
re-raises it says so explicitly and gives the new reason.

## When repeated departures suggest an amendment

Decision cards create a record of approved departures. When the same stance is departed from, with the same
kind of reason, and approved more than once (two approvals is a reasonable trigger, three a strong one), the
pattern is case law asking to be written down. The agent says so:

"You have approved departing from T03 three times for readers that need only the standard library (PR #250,
#263, #271). Should this become a flip condition on T03?"

The reverse also matters: a flip condition that is never invoked, or a stance that is departed from in most
cards, suggests the recorded stance no longer describes the project. Raise it as a question, not a correction:
the maintainers may want the stance to pull against current habit.

## Splits, merges and retirements

- **Split:** one tension or value turns out to be two. Create new IDs for both; mark the old one `superseded`
  with `superseded_by`; log a MAJOR entry; re-check cards that cited the old ID.
- **Merge:** two tensions are really one. Create a new ID; mark both old ones `superseded`.
- **Retire:** a tension no longer applies (the constraint behind a `contingent` tension dissolved, or the
  project left that domain). Keep the entry with `status: "retired"` and the amendment ID that retired it.

IDs are never reused, so an old citation always points at exactly one thing.

## Git practice

The philosophy folder is meant to live in the project's repository and be tracked by git.

- Commit `philosophy.json`, the generated `PHILOSOPHY.md` and map page, `AMENDMENTS.md`, `GOVERNANCE.md`,
  individual files, session notes and reconciliation folders. They are small plain-text files (the map page is
  one self-contained HTML file).
- Canvas specs and results are optional to keep; they are useful evidence for how a stance was elicited.
- One amendment per commit where practical, with the amendment ID in the message, so `git log --grep A0002`
  finds it.
- Regenerate the rendered files in the same commit as the JSON change, so the readable view never lags.
- Git is the full diff history; the amendment log is the human-readable reasoning. Neither replaces the other.
- Never commit on the user's behalf without being asked, and never rewrite history in the philosophy folder.

## Review dates

Tensions with `necessity: "contingent"`, provisional stances, recorded concerns and dissent carry a `review_by`
date. When a session starts and a date has passed, the agent mentions it: "T04's review date (2027-06-01) has
passed; revisit it?" A review that changes nothing is logged as a PATCH entry ("reviewed; unchanged") with a new
review date, so the log shows the stance was checked rather than forgotten.
