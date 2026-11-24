# Data model: `philosophy.json`

The canonical record of a project's philosophy (its values and priorities) is one JSON file, `philosophy.json`. Everything
else is generated from it (the readable `PHILOSOPHY.md` and the interactive map page) or sits beside it (the
amendment log, governance notes, individual maintainers' files). This reference documents every field, says
which fields are required, and gives an example for each tension shape.

The examples come from rowfold, a fictional pure-Python library for reading tabular files whose complete
philosophy ships with this skill's repository (`examples/rowfold/philosophy.json`). Where an example shows a
field that file does not use, the example says so.

JSON was chosen because a browser and Python's standard library can both read it with no extra software, and
because a structured file lets agents and scripts find tensions by ID, compare maintainers, and draw the map.
Humans read the generated `PHILOSOPHY.md`; nobody should need to hand-edit JSON unless they want to.

## Contents

- Design rules that shape the schema
- Top-level fields
- Synthesis (bottom line up front)
- Hard limits
- Values glossary (required)
- Tensions: common fields
- Tension shape 1: polarity (two poles)
- Tension shape 2: triad (three values)
- Tension shape 3: network (four or more values, many-to-many)
- Stances, firmness, status
- Flip conditions and early warnings
- Precedents
- Evidence
- Per-maintainer positions and dissent
- Stable IDs, revisions and citation (`T04@2`)
- Contradictions log
- Strictness
- Amendment entries in the JSON
- Individual maintainers' files
- Validation checklist
- Compatibility rules

---

## Design rules that shape the schema

1. **Define before you weigh.** Every value has one explicit, operational definition in the `values`
   glossary, written from the maintainer's own explanation and confirmed by them. Tensions refer to values by
   ID, and every surface (interview questions, canvases, the generated `PHILOSOPHY.md`, the map page, decision
   cards) shows the glossary definition instead of restating the value in its own words. This keeps a word
   like "Correctness" from drifting between documents, people and months. Definitions can change, but only
   through an explicit, logged revision (`correctness@2`).
2. **Both sides of every tension are goods.** A tension records values a reasonable project could prefer. A
   "value" with no acceptable opposite (for example "no security holes") is a hard limit, not a tension. See
   the "acceptable opposite" test in `interview-playbook.md`.
3. **Hard limits sit outside the trade-off space.** They are checked first and never weighed. A value can be
   both a hard-limit floor and a tradeable value above that floor.
4. **Tensions come in three shapes:** a polarity (two poles), a triad (three values), or a network (four or
   more values, possibly with pairwise links). The shape decides the form of the stance.
5. **Stances are stored at the precision they were elicited.** A position of `-0.75` means "strongly toward
   the first pole", not a measurement. Never report more precision than the conversation produced.
6. **Current text only.** A tension carries its current stance. History lives in the amendment log and git,
   so an agent reading the file sees today's ruling, not the argument that led to it.
7. **Stable IDs, never reused.** Values, tensions, hard limits, precedents and amendments keep their IDs
   forever, including after they are retired or superseded.
8. **Additive evolution.** New optional fields may be added; existing fields are never renamed or removed
   within a major schema version. Readers ignore fields they do not know.
9. **Field names are not display labels.** The generated pages and `PHILOSOPHY.md` show plain wording for
   people; the JSON keeps its field names, and agents cite IDs exactly:

   | Field or value | Shown as |
   |----------------|----------|
   | `hard_limits` | "Lines we never cross" |
   | `tensions` | "Priorities" (each card still shows its ID, such as T02, in a quieter style) |
   | `stance` | "Where we stand"; `firmness: "firm"` shows as "Firm position" |
   | `flip_conditions` | "Exceptions we'd accept" |
   | verdict `flip_condition_met` | "Allowed exception" |
   | `status: "agreed"` / `"consented"` | "agreed by everyone" / "agreed, with concerns noted" |
   | `positions[].endorsement` `"endorse"` / `"consent with concern"` | "agrees" / "agrees, with a concern" |
   | `positions[].holder` | a capitalised first name: `maintainers[].name` when given, else the handle (`maya` → Maya) |
   | `glossary_terms` | "Other terms", after the values glossary |
   | proposal `overall` `"consistent"` / `"departs"` | "Fits your priorities" / "Departs from your priorities (explained)" |

## Top-level fields

| Field | Required | Type | Meaning |
|-------|----------|------|---------|
| `schema` | yes | string | Schema identifier. v0.1 files use `"philosophical-alignment/0.1-draft"`. Readers accept any `philosophical-alignment/0.x` value, and also `architectural-philosophy/0.x`, the label written under the skill's earlier name: those files are read unchanged, so there is no need to edit them. |
| `project` | yes | string | Project name as the maintainers write it. |
| `version` | yes | string | Document version `MAJOR.MINOR.PATCH` (rules in `amendments.md`). |
| `mission` | yes | string | One or two sentences: what the project is for. Everything else is read in light of this. |
| `synthesis` | yes once confirmed | object | `{"text", "as_of_version"}`: the bottom-line summary, 3 to 5 plain sentences. See "Synthesis". |
| `maintainers` | yes | array | `[{handle, role}]`; optional `status` (`"active"` or `"emeritus"`) and `scopes` (subsystems they own). |
| `values` | yes | array | The glossary: one operational definition per value. See "Values glossary". |
| `hard_limits` | yes | array | Non-negotiable constraints (may be empty). See below. |
| `tensions` | yes | array | The trade-offs and stances. See below. |
| `amendment_log` | yes | array | One index entry per document version (see "Amendment entries"). |
| `status_note` | no | string | Free text about the file's state, for example "Seed draft inferred from docs; not yet confirmed." |
| `holder` | no | string | `"project"` for the shared file (default), or a maintainer handle for an individual file. |
| `project_types` | no | array of strings | Any of `library`, `language`, `application`, `package-manager`, `infrastructure`, `research`, `data-analysis`, `documentation`, `other`. Used to filter the tension library. |
| `ratified` | no | date string | Date the philosophy was first adopted (first version a maintainer confirmed). |
| `last_amended` | no | date string | Date of the most recent amendment. |
| `glossary_terms` | no | array | Definitions of other terms the philosophy relies on that are not values (for example "public API", "identical results"). Same entry shape as `values`. |
| `non_goals` | no | array of strings | Things that could reasonably be goals but are deliberately not. Explains many rejected proposals. |
| `strictness` | no | object | How binding the philosophy is on agents. See "Strictness". Absent means advisory. |
| `contradictions` | no | array | Detected inconsistencies and how each was resolved. See "Contradictions log". |
| `levers` | no | array | Design decisions that move several values at once. See the network shape. |
| `interop` | no | object | Existing documents detected at setup and pointer sections added. See below. |

Dates are ISO `YYYY-MM-DD` strings throughout.

### `interop`

```json
"interop": {
  "detected": [
    {"path": "AGENTS.md", "kind": "agent-instructions"},
    {"path": "docs/adr/", "kind": "adr-folder", "note": "14 records; used as precedent sources"},
    {"path": ".specify/memory/constitution.md", "kind": "spec-kit-constitution"}
  ],
  "pointers": [
    {"file": "AGENTS.md", "section": "Project philosophy (values and priorities)", "added": "2026-11-20", "approved_by": "maintainer-a"}
  ]
}
```

`kind` values in use: `agent-instructions`, `claude-md`, `cursor-rules`, `kiro-steering`, `copilot-instructions`,
`spec-kit-constitution`, `adr-folder`, `proposal-process`, `product-doc`, `design-doc`, `architecture-doc`,
`contributing`, `other`. Recording these lets a later session know what was read and where pointers live.

## Synthesis (bottom line up front)

Every philosophy opens with a short narrative summary, so a reader who reads nothing else still knows what the
project values and how it trades off. Views (the generated `PHILOSOPHY.md`, the map page) show it first, with
the detail one step away.

```json
"synthesis": {
  "text": "Example package: rowfold is a library other projects build on, so it protects the people downstream first: installing it never needs a compiler, and nothing is removed without a deprecation period. Correct results come before speed and before convenience; when rowfold cannot be sure what a file means, it says so instead of guessing. Portability comes before raw speed, and compiled code is welcome only as an optional extra that gives the same results as the pure-Python path. The core stays small, and integrations with other tools live in plugins. When an old API is unclear, the project keeps it working and adds a clearer one beside it, saving clean breaks for major releases with a migration guide.",
  "as_of_version": "1.1.1"
}
```

| Field | Meaning |
|-------|---------|
| `text` | 3 to 5 plain sentences on what the project values and how it trades off. No jargon, no IDs, no numbers. Value words are used only in their glossary senses. It names the most important stances and hard limits in everyday language; it does not list every tension. |
| `as_of_version` | The document `version` the text was last confirmed against. If it differs from `version`, the synthesis is stale and views should say so. |

Rules:

- **The agent drafts it; the maintainers confirm it.** Read it back and expect edits. In a team, the synthesis
  of the shared file is confirmed under the team's decision rule like any other change.
- **Refresh it with every amendment** that changes a stance, a hard limit or a definition, and set
  `as_of_version` to the new version. A patch-level change (wording, a new illustrative precedent) only needs
  `as_of_version` updated if the text still holds; say so in the amendment entry.
- **Write it for a newcomer.** Someone who has never seen the project should come away knowing what it
  protects, what it is willing to give up, and where it draws hard lines.
- A seed drafted from documents may carry a draft synthesis; mark it unconfirmed in `status_note` until a
  maintainer confirms it.

## Hard limits

```json
"hard_limits": [
  {"id": "H1",
   "text": "pip install works everywhere we support, with no compiler required: installing rowfold succeeds on every supported Python version and platform from a pure-Python wheel.",
   "source": "Example: the project README's install promise",
   "kind": "floor",
   "protects": ["Portability"],
   "override": "Only by an amendment every active maintainer endorses.",
   "status": "agreed"}
]
```

(rowfold's file leaves out the optional `override` and `status`; they are shown here for completeness.)

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | `H` plus a number, never reused. |
| `text` | yes | The limit, as an observable rule an agent can check a proposal against. |
| `source` | yes | Where it came from: an interview, a document, a license, a funder's requirement. |
| `kind` | no | `prohibition` (never do X), `floor` (value Y never drops below a level), or `ceiling` (Z never exceeds a level). |
| `protects` | no | Names of the values the limit protects. |
| `override` | no | What it would take to change it. Usually "an amendment every active maintainer endorses". |
| `status` | no | Same vocabulary as tensions (default `agreed`). |
| `rev` | no | Revision number, as for tensions (default 1). |

Hard limits are deliberately few. If a maintainer names more than about five, ask which of them they would
actually trade under extreme pressure; those belong in tensions with `firmness: "core"`.

## Values glossary

The glossary is required. It defines each value once, operationally, so that "Correctness" means the same thing in
every tension, every card and every maintainer's mouth, and so a reader months later can tell exactly what was
meant. Every tension refers to its values by glossary `id`, and every surface displays the glossary definition.

```json
"values": [
  {"id": "correctness", "name": "Correctness", "rev": 1,
   "definition": "The degree to which every table rowfold returns matches what the file actually holds, or rowfold raises a clear error instead of returning a guess.",
   "looks_like": ["Round-trip tests on a corpus of real, messy files", "Errors on ambiguous input instead of silent choices", "Property-based tests on the parser"],
   "too_little": "Silent data corruption: shifted columns, dropped rows, misread dates.",
   "not_to_be_confused_with": "Not test coverage: many tests can check the wrong thing. Not Explicitness, though explicit arguments help. Not Performance: a faster path must be exactly as correct.",
   "in_own_words": "Correct means I'd bet a downstream researcher's paper on the table. If we're not sure what a cell means, we stop and say so; we never return a plausible guess.",
   "examples": {"good": ["The ambiguous-date error added in v2.1"],
                "missing_or_faked": ["A 95% coverage badge on a parser that still drops the last row without a trailing newline"]},
   "by": "maintainer-a",
   "confirmed": "2026-06-02",
   "amendments": []}
]
```

(rowfold's file leaves out the optional `by`, `confirmed` and `amendments`; they are shown here for completeness.)

### Fields

| Field | Required | Meaning |
|-------|----------|---------|
| `id` | yes | Short lowercase slug (`correctness`), stable and never reused. Tensions refer to values by this. |
| `name` | yes | Display name. Must match the `value` strings used in that value's tensions exactly (case and spelling), because stance `weights` and `priority` are keyed by name. |
| `rev` | yes | Definition revision, starting at 1. Increments when the meaning changes (see below). |
| `definition` | yes | One sentence, ISO 25010 style: "The degree to which ..." or "How ...". Operational: an observer could tell from an artifact whether there is more or less of it. Written from the maintainer's own explanation. |
| `looks_like` | yes | Two to four observable indicators: what you would see in a commit, a review, an output or a paper when this value is present. |
| `too_little` | yes | What it looks like when this value is missing. |
| `not_to_be_confused_with` | yes | The boundary: what people wrongly call by this name, and how it differs from its nearest neighbouring values (name them). |
| `in_own_words` | yes, may be `null` in a seed | The maintainer's own elaboration, kept verbatim or near-verbatim. A string; several sentences is normal for a value that carries a real tension. `null` marks a definition that was drafted (for example from documentation) and has not yet been explained by a maintainer. |
| `too_much` | no | What over-serving this value looks like, when that is not already the `overdone` text of a polarity pole. |
| `examples` | no | `{"good": [...], "missing_or_faked": [...]}`: concrete cases from this project, in the maintainer's words. |
| `by` | no | Whose words `in_own_words` and `examples` are. Matters in teams: each maintainer's elaboration lives in their individual file, and the shared glossary names whose framing it adopted (or `"shared"` after reconciliation). |
| `confirmed` | no | Date the maintainer confirmed the drafted definition. Absent means not yet confirmed. |
| `amendments` | no | Definition history `[{rev, date, summary}]`. Full entries go in `AMENDMENTS.md`. |
| `serves` | no | IDs of higher-level values or plain-language outcomes this value is a means to (from laddering). Helps avoid double counting a means and its end. |
| `stakeholders` | no | `{"direct": [...], "indirect": [...]}`: who uses the project, and who is affected without using it. |
| `facets` | no | Sub-values, recorded as children rather than as separate peers, so a value does not gain weight just by being split into detailed parts. |
| `source` | no | Where the entry came from (interview session, document, canvas result). |

### How tensions refer to values

- **Polarity:** each pole carries `"ref": "<value id>"` beside its `value` name.
- **Triad:** each entry in `values` carries `"ref": "<value id>"`.
- **Network:** the tension carries `"refs": [...]`, a list of value IDs in the same order as its `values`
  list of names.
- Stance `weights`, `priority` and `positions` stay keyed by value **name**, as in the original format. The
  `ref` links the name to its definition.

A pole's `good` and `overdone` text describe why the value matters *in that tension*; the glossary
`definition` says what the value *is*. Keep them consistent: if a pole's `good` text implies a different
meaning from the glossary, that is a definitional drift to raise with the maintainer.

### Revising a definition (`correctness@2`)

- **Clarification without a change of meaning** (better wording, a new indicator that fits the old meaning):
  edit in place, no `rev` change, a PATCH entry in the amendment log.
- **Change of meaning** (the boundary moves, an indicator is added that the old definition excluded, a
  facet is split off into its own value): increment the value's `rev`, add a per-value `amendments` entry,
  and write a full entry in `AMENDMENTS.md`. Cite a definition by `id@rev`, for example `correctness@2`.
- A definition change does not by itself change the revision of the tensions that use the value. Decision
  cards cite both (`T04@1`, `correctness@2`), so a reader can see exactly which meaning and which stance applied.
- **Splitting a value** (one word covered two meanings) creates new IDs; the old value gets
  `"status": "superseded"` and `"superseded_by": [...]`, and the affected tensions are revised.
- Agents never silently use a value word in a different sense. An agent that needs a new sense proposes a
  glossary amendment instead.

### Other glossary terms

Philosophy text often relies on terms that are not values but whose meaning matters for applying a stance:
"public API", "identical results", "supported platform", "major release". Put them in the optional top-level
`glossary_terms` array, with the same entry shape (at minimum `id`, `name`, `rev`, `definition`). A flip
condition that depends on such a term should use the exact term name.

## Tensions: common fields

Every tension, whatever its shape, has these fields.

| Field | Required | Type | Meaning |
|-------|----------|------|---------|
| `id` | yes | string | `T` plus a two-digit number in the shared file (`T07`). Never reused. |
| `rev` | yes | integer | Stance revision, starting at 1. Increments when the meaning of the stance changes. |
| `slug` | yes | string | Short kebab-case handle (`portability-vs-performance`). Used to match tensions across maintainers' files. |
| `kind` | yes | string | `polarity`, `triad` or `network`. |
| `name` | yes | string | Human name ("Portability vs. raw speed"). |
| `stance` | yes | object | Where the project stands. Shape depends on `kind`. Has `summary` and `firmness`. |
| `flip_conditions` | yes | array of strings | Contextual conditions under which the stance changes (may be empty). |
| `precedents` | yes | array | Past decisions that illustrate the stance (may be empty). |
| `status` | yes | string | Agreement state (vocabulary below). |
| `positions` | no | array | Per-maintainer positions (teams). |
| `amendments` | no | array | Short per-tension history index `[{rev, date, summary}]`. |
| `early_warnings` | no | array | Corrective signals that the project has over-rotated. |
| `evidence` | no | object | How well the stance was elicited. |
| `greater_purpose` | no | string | The shared goal that needs both poles (polarity mapping). |
| `deeper_fear` | no | string | What happens if the project falls into the downside of both. |
| `mechanisms` | no | array of strings | Ways the project softens the tension to get more of both (feature flags, escape hatches, release channels). Agents look here first. |
| `necessity` | no | string | `inherent` (a true trade-off) or `contingent` (a current constraint that better tools might dissolve). |
| `scope` | no | string or array | `"project"` (default) or the subsystems the stance covers. |
| `owner` | no | string | Maintainer handle when the stance is owned by a subsystem owner. |
| `review_by` | no | date | When to revisit ("good enough for now, safe enough to try"). |
| `dissent` | no | array | Recorded objections and concerns (teams). |
| `decision` | no | object | Which rule decided the shared stance and who applied it (teams). |
| `framing_status` | no | string | `agreed` or `disputed`: whether maintainers agree on what the tension is. |
| `supersedes` / `superseded_by` | no | string | Tension IDs linking a split, merge or replacement. |
| `origin` | no | string | The local ID in an individual file this tension came from, for example `individuals/alex/philosophy.json#T03@2`. |

## Tension shape 1: polarity (two poles)

```json
{
  "id": "T02", "rev": 2, "slug": "portability-vs-performance", "kind": "polarity",
  "name": "Portability vs. raw speed",
  "poles": [
    {"value": "Portability", "ref": "portability",
     "good": "Runs anywhere Python runs: new Python releases on day one, Alpine, Pyodide, unusual CPUs, locked-down machines.",
     "overdone": "Users with large files leave for faster libraries, and the project refuses help that would cost nothing to anyone else."},
    {"value": "Performance", "ref": "performance",
     "good": "Large files parse in seconds, not minutes, so rowfold stays usable as data grows.",
     "overdone": "A build matrix nobody can maintain, and installs that fail on the platforms the project promised to support."}
  ],
  "stance": {"position": -0.5,
             "summary": "Portability first: the pure-Python parser is the reference. Compiled extras are welcome when optional.",
             "firmness": "firm"},
  "flip_conditions": ["Compiled code is welcome as an optional extra with a pure-Python fallback that gives identical results."],
  "precedents": [{"title": "Optional [zstd] compression extra (v2.3)",
                  "note": "Zstandard support came through a compiled library as an opt-in extra; gzip and bz2 from the standard library keep working without it."}],
  "status": "agreed",
  "amendments": [{"rev": 2, "date": "2026-09-14",
                  "summary": "After three optional compiled extras shipped without problems, the flip condition was promoted into the stance: compiled extras are welcome when optional."}]
}
```

- `poles` has exactly two entries. Each has `value` (required, the glossary `name`), `ref` (required, the
  glossary `id`), `good` (required: why a reasonable project would want this), and `overdone` (strongly recommended: what goes wrong when this pole is pushed too far).
  `good` and `overdone` together are the upside and downside quadrants of a polarity map.
- `stance.position` is a number from `-1` to `+1`. **Negative means toward `poles[0]`, positive toward
  `poles[1]`, and `0` is balanced.** Rough labels: about 0.25 is "slight", 0.5 "clear", 0.75 "strong", 1.0
  "always, unless a flip condition applies". The spectrum canvas snaps to these steps by default.
- Write `stance.summary` in "A over B" form and acknowledge the losing pole where it helps: "Compatibility
  over clarity. A clearer API is added beside the old one, and the old one leaves only through deprecation."
- `stance.precision` (optional) is `"rough"` or `"considered"`; see "Stances, firmness, status".
- Balanced is a legitimate stance, but ask what "balanced" means: truly equal, undecided, or "it depends".
  "It depends" means a flip condition is waiting to be written down.

## Tension shape 2: triad (three values)

```json
{
  "id": "T04", "rev": 1, "slug": "approachability-performance-correctness", "kind": "triad",
  "name": "Approachability, performance, correctness",
  "values": [
    {"value": "Approachability", "ref": "approachability", "good": "A newcomer reads a file correctly in one line, from the first example in the docs."},
    {"value": "Performance", "ref": "performance", "good": "Large files parse quickly and within memory."},
    {"value": "Correctness", "ref": "correctness", "good": "The table you get is the table the file holds, or a clear error that says why not."}
  ],
  "rule": "pick-two",
  "stance": {"weights": {"Approachability": 0.3, "Performance": 0.2, "Correctness": 0.5},
             "pick": ["Correctness", "Approachability"],
             "summary": "Correctness is protected first. Within that floor, approachability edges out performance.",
             "firmness": "firm"},
  "flip_conditions": ["A faster code path may become the default only when it passes the same correctness test suite as the path it replaces."],
  "precedents": [{"title": "Ambiguous dates raise an error (v2.1)",
                  "note": "01/02/2024 stopped being guessed as January or February; rowfold asks for a format, at a cost in speed and in friction for newcomers."}],
  "status": "consented"
}
```

(rowfold's T04 also carries both maintainers' `positions`; see "Per-maintainer positions and dissent".)

- `values` has exactly three entries `{value, ref, good}`; `overdone` is optional here too.
- `stance.weights` maps each value name to a fraction; the fractions sum to 1. The point sits inside a
  triangle whose corners are the three values. Store multiples of 0.05 or 0.1; the triangle canvas snaps to
  a 10 percent grid.
- Optional additions:
  - `rule`: `"pick-two"` when the maintainers treat it as "you can have at most two at full strength", or
    `"budget"` when the three share a fixed budget. A rule of thumb, not a law; note known exceptions.
  - `stance.pick`: the values protected when forced to choose.
  - `stance.floors`: value name to a sentence describing the minimum acceptable level (satisficing), for
    example `{"Performance": "Never slower than the previous release on the benchmark corpus."}`.
  - `stance.posture`: `"balanced"` (an uneasy compromise among all three) or `"corner"` (maximise one or two
    and accept the cost on the rest). Comes from McGrath's dilemmatics.

## Tension shape 3: network (four or more values, many-to-many)

Use a network when four or more values pull against each other, or when a group of values pulls against
another group ("approachability, compatibility and expressiveness versus robustness, debuggability and
simplicity").

rowfold's published file has no network tension. The one below is invented to show the shape; it uses only
values from rowfold's glossary and stays consistent with its other stances, and it is marked `provisional`
because no maintainer has confirmed it.

```json
{
  "id": "T06", "rev": 1, "slug": "plugin-interface", "kind": "network",
  "name": "The plugin interface",
  "values": ["Compatibility", "Small core", "Batteries included", "Approachability"],
  "refs": ["compatibility", "small-core", "batteries-included", "approachability"],
  "edges": [
    {"a": "Small core", "b": "Batteries included", "note": "Each new plugin hook lets more jobs work, but it is core code two maintainers must keep correct."},
    {"a": "Compatibility", "b": "Approachability", "note": "A public hook keeps its first, sometimes awkward, shape until a major release."},
    {"a": "Compatibility", "b": "Small core", "note": "Fewer hooks means fewer promises to keep.", "relation": "supports"}
  ],
  "sides": [{"label": "Fewer promises", "values": ["Compatibility", "Small core"]},
            {"label": "Easier plugins", "values": ["Batteries included", "Approachability"]}],
  "levers": ["L1"],
  "stance": {"priority": ["Compatibility", "Small core", "Approachability", "Batteries included"],
             "weights": {"Compatibility": 0.35, "Small core": 0.3, "Approachability": 0.2, "Batteries included": 0.15},
             "ordering": "weighted",
             "summary": "Few hooks, kept stable. A hook is added only when two or more plugins need it, and once public it follows the same deprecation rules as the rest of the public API.",
             "firmness": "working"},
  "flip_conditions": ["A hook that an official plugin (such as rowfold-excel) needs may be added in a minor release."],
  "precedents": [{"title": "rowfold-excel reads through read_chunks()",
                  "note": "The Excel plugin was built on the existing streaming hook instead of a new one."}],
  "status": "provisional"
}
```

- `values` is a list of value names (strings) and `refs` the matching glossary IDs, in the same order.
  Readers should also accept `{value, ref, good}` objects in `values`, the same form a triad uses. Name
  every value as a good ("Economy", not "Cost"; "Responsiveness", not "Latency"), so the acceptable-opposite
  test still works in a network.
- `edges` are pairwise links. `relation` defaults to `"conflicts"`; use `"supports"` when one value helps
  another and `"depends"` when one requires the other. A `note` says why.
- `sides` (optional) groups values into two camps for a group-versus-group tension.
- `stance.priority` (required for networks) is the tie-breaking order, first to last. `stance.weights`
  (optional) is an allocation that sums to 1, from the allocate canvas. `stance.ordering` is `"weighted"`
  (the order is a default that strong reasons can overturn) or `"lexicographic"` (an earlier value always
  wins). Prefer `weighted`; a lexicographic first value is usually better written as a hard limit.
- `levers` lists IDs from the top-level `levers` array:

```json
"levers": [
  {"id": "L1", "description": "How many hooks the plugin interface exposes",
   "moves": {"Batteries included": "up", "Approachability": "up", "Small core": "down", "Compatibility": "down"}}
]
```

A lever is a single design choice that moves several values at once (an ATAM "trade-off point"). Levers let an
agent say which knob a proposal turns. In `moves`, `"up"` means the lever improves that value and `"down"`
means it costs that value.

## Stances, firmness, status

### `stance` fields shared by every shape

| Field | Required | Meaning |
|-------|----------|---------|
| `summary` | yes | One or two sentences in plain language, quotable by agents. |
| `firmness` | yes | How hard the holders would resist changing it (scale below). |
| `position` / `weights` / `priority` | per shape | The stance itself (see each shape). |
| `precision` | no | `"rough"` (default assumption) or `"considered"` when the maintainers deliberately tuned it. |

### Firmness scale

| Value | Meaning | How agents cite it |
|-------|---------|--------------------|
| `exploratory` | Said once; the maintainer is unsure or thinking aloud. | "A tentative position, not yet tested." |
| `working` | Held, but expected to change as the project grows. | "Current practice, expected to evolve." |
| `firm` | Held deliberately; changing it needs a stated reason and an amendment entry. | "A deliberate stance." |
| `core` | Central to the project's identity; reversing it is a major version. | "A core stance of the project." |

Truly non-negotiable rules are not a firmness level; they are hard limits.

### Status vocabulary

| Status | Meaning | Agent default |
|--------|---------|---------------|
| `provisional` | Captured from one person or inferred from documents; not yet confirmed or reconciled. | Apply lightly and label it provisional. |
| `agreed` | Every active maintainer endorses it. For a solo project, the maintainer has confirmed it. | Cite and apply. |
| `consented` | No unresolved objection; concerns recorded. | Cite and apply; mention concerns when relevant. |
| `rough` | Decided over a recorded, addressed objection; holdouts named. | Apply; name the holdout's view when a proposal touches it. |
| `scoped` | Different stances per subsystem, each with an owner. Use `scope` and `owner`, or several tensions with the same slug prefix and different scopes. | Apply the stance for the subsystem being changed; ask the owner when unclear. |
| `contested` | No shared stance; positions listed. `stance.summary` describes the disagreement. | Never pick a side. Present both and ask, at any strictness. |
| `superseded` | Replaced by another tension (see `superseded_by`). | Do not apply; may cite as history. |
| `retired` | No longer relevant; kept for its ID and history. | Do not apply. |

A seeded draft inferred from documentation should be `provisional` until a maintainer confirms each tension.

## Flip conditions and early warnings

The stance is a default. Two different things can move it.

**Contextual flips (`flip_conditions`).** A different situation calls for a different stance, the way PACELC
says "during a partition choose A or C, else choose L or C". Write each as an observable condition plus the
direction of the change, so an agent can test whether it applies to a proposal:

- Good: "Compiled code is welcome as an optional extra with a pure-Python fallback that gives identical
  results." (rowfold's T02; "identical results" is defined in its `glossary_terms`.)
- Weak: "Sometimes speed matters more." (Not observable; no direction.)

`flip_conditions` is an array of plain strings in v0.1. If two conditions can both apply, say in the text which
wins ("This takes precedence over the official-plugin exception"). The more specific condition usually wins.

**Corrective flips (`early_warnings`).** The situation is the same, but the project has over-rotated toward one
pole and should rebalance. This comes from polarity management.

```json
"early_warnings": [
  {"toward": "Compatibility", "signal": "Three or more deprecated names have outlived two major releases.",
   "response": "Remove them in the next major release, with a migration guide."}
]
```

(Illustrative, on rowfold's T01; the published file records no early warnings.)

`toward` names the over-served value, `signal` is an easy-to-observe sign, and `response` is the agreed
corrective action.

## Precedents

Precedents are past decisions that show how the stance was actually applied. They are case law: they
illustrate a stance but do not decide a new case on their own.

```json
"precedents": [
  {"id": "P04", "title": "Ambiguous dates raise an error (v2.1)",
   "note": "01/02/2024 stopped being guessed as January or February; rowfold asks for a format, at a cost in speed and in friction for newcomers.",
   "link": "https://example.org/rowfold/pull/482",
   "verdict": "consistent",
   "options_considered": ["Keep guessing month-first", "Raise an error that shows both readings and the argument that picks one"],
   "would_have_changed_it": "If the file itself declared its date format.",
   "source": {"style": "retrospective", "holder": "maintainer-b", "session": "2026-05-20"}}
]
```

(rowfold's T04 records this precedent with only `title` and `note`; the other fields are illustrative.)

| Field | Required | Meaning |
|-------|----------|---------|
| `title` | yes | Short name of the decision. |
| `note` | yes | What was chosen and what was given up. |
| `id` | no | `P` plus a number, unique across the file, never reused. Recommended once a project has more than a handful. |
| `date`, `link` | no | When, and a pointer to the PR, issue, commit, ADR or paper. |
| `verdict` | no | `consistent` (followed the stance), `exception` (departed with a reason), or `flip` (a flip condition applied). |
| `options_considered` | no | The alternatives that were on the table. |
| `would_have_changed_it` | no | The maintainer's answer to "what would have made you choose differently?" Often becomes a flip condition. |
| `source` | no | Which interview style and session it came from. |

Precedents are append-only: correct a typo, but do not delete one because it now looks awkward. Annotate it
(`"note": "... Superseded as an illustration by P09."`) instead.

## Evidence

Firmness says how strongly a stance is held; evidence says how well it was elicited. A firmly stated stance
that was never tested against a real decision is still weak evidence.

```json
"evidence": {"styles": ["abstract", "retrospective", "forced-choice"],
             "level": "strong",
             "quotes": [{"holder": "maintainer-a", "text": "If we're not sure what a cell means, we stop and say so; we never return a plausible guess.", "session": "2026-05-20"}],
             "canvases": ["individuals/maintainer-a/canvases/2026-05-20_T04_triangle.result.json"]}
```

- `styles`: any of `abstract`, `retrospective`, `forced-choice`, `contradiction-check`, `inferred-from-docs`.
- `level`: `weak` (one style, no precedent), `medium` (two styles agree, or one style plus a precedent),
  `strong` (abstract, forced-choice and retrospective agree and no contradiction is open).
- `quotes`: the maintainer's own words. Keep them short and verbatim.

Agents phrase citations using both: "a firm stance with weak evidence: the maintainer's stated position, not
yet tested against a real case".

## Per-maintainer positions and dissent

In a team's shared file, each tension can carry the named positions behind it, even when everyone agrees.

```json
"positions": [
  {"holder": "maintainer-a", "weights": {"Approachability": 0.3, "Performance": 0.2, "Correctness": 0.5}, "endorsement": "endorse"},
  {"holder": "maintainer-b", "weights": {"Approachability": 0.15, "Performance": 0.35, "Correctness": 0.5},
   "endorsement": "consent with concern",
   "note": "Worries that slow defaults send users with large files to faster libraries before they ever see rowfold's guarantees.",
   "interests": "Users with large files judge a parser by its speed first.",
   "source": "individuals/maintainer-b/philosophy.json#T02@1"}
],
"dissent": [
  {"holder": "maintainer-b", "kind": "concern",
   "note": "Slow defaults may send users with large files elsewhere.",
   "reopen_trigger": "Two or more issues a month from users leaving over parse speed.",
   "settling_test": null, "review_by": "2027-06-01"}
],
"decision": {"rule": "consent", "decided_by": ["maintainer-a", "maintainer-b"], "caller": "maintainer-a",
             "date": "2026-06-02", "cycle": "reconciliation/2026-05-27_first-synthesis"}
```

(rowfold's T04 carries the two `positions` with `holder`, `weights`, `endorsement` and `note`; `interests`,
`source`, `dissent` and `decision` are illustrative.)

- A position uses the same stance field as the tension's shape: `position` for a polarity, `weights` for a
  triad, `priority` (and optionally `weights`) for a network. Use `stance_text` for a quoted summary.
- `endorsement` vocabulary: `endorse`, `consent`, `consent with concern`, `stand aside`, `in the rough`,
  `object`. Meanings are in `reconciliation.md`.
- `intensity` (optional) is a number from -1 to +1 in the Apache voting style ("-0.5: I don't like it but
  won't block").
- `dissent[].kind` is `objection` (a reasoned risk; blocks until addressed) or `concern` (recorded, does not
  block). `reopen_trigger` says what evidence would reopen the question.
- `decision.rule` is one of `consensus`, `consent`, `rough-consensus`, `lazy-consensus`, `owner`, `vote`,
  `arbiter`.

Never compute the shared `stance` from the positions by averaging. The shared stance is whatever the team's
decision rule produced; positions are kept beside it as the record.

## Stable IDs, revisions and citation (`T04@2`)

- **Values** use a lowercase slug (`correctness`) and are cited `correctness@2`. **Tensions** use `T` plus a number
  (`T04`), **hard limits** `H`, **precedents** `P`, **levers** `L`,
  **contradictions** `X`, **amendments** `A` plus four digits (`A0007`). IDs are never reused.
- **`rev`** increments when the meaning of a stance changes: the stance moves, a flip condition is added,
  removed or changed, the set of values or poles changes, or firmness changes. It does not increment for a
  wording fix.
- **Citation form:** `T04@2` means tension T04 at revision 2. Decision cards, ADRs, PR descriptions and code
  comments cite this form, so a reader can see whether a card was written against the current stance. A card
  that cites `T04@2` when the file has `T04@3` is visibly stale.
- **Splits and merges** create new IDs; the old tension gets `status: "superseded"` and `superseded_by`.
- **Individual files** use their own local numbering. Shared numbers are assigned only when a tension enters
  the shared file, which prevents collisions when maintainers draft in parallel. The `slug` is the matching
  key during reconciliation, and `origin` records where a shared tension came from.

## Contradictions log

When two of a maintainer's answers disagree, record it rather than silently picking one. Most contradictions
turn out to be an unstated flip condition.

```json
"contradictions": [
  {"id": "X01", "date": "2026-05-20", "holder": "maintainer-a", "tensions": ["T05"],
   "detected_by": "cross-method",
   "statement": "Placed T05 toward explicitness, but in the dilemma chose to let peek() guess the delimiter by default.",
   "resolution": "new-condition",
   "result": "Added to T05: interactive helpers (such as rowfold.peek) may guess by default, as long as they print what they guessed.",
   "status": "resolved"}
]
```

(Illustrative: rowfold's file has no `contradictions` log, but its T05 flip condition is the one this
resolution produced.)

- `detected_by`: `transitivity` (A over B, B over C, C over A), `cross-method` (abstract answer versus
  forced choice), `precedent-mismatch` (a past decision against the stated stance), `cross-tension` (stances
  in two tensions imply opposite things), or `reviewer` (a teammate or agent noticed it).
- `resolution`: `new-condition`, `split-value` (one word covered two values), `revised-stance`,
  `elicitation-artifact` (the question was badly posed), or `open` (a real unresolved tension, kept visible).
- `status`: `open` or `resolved`.

## Strictness

How binding the philosophy is on agents. Absent means advisory.

```json
"strictness": {
  "level": "advisory",
  "by_firmness": {"core": "flag-and-ask"},
  "by_tension": {"T02": "review-gate"},
  "set_by": "maintainer-a", "date": "2026-06-02",
  "note": "Advisory overall; a departure from a core stance stops and asks, and portability changes wait for written approval."
}
```

(rowfold's file has `level`, `by_firmness` and a shorter `note`; `by_tension`, `set_by` and `date` are
added here to show them.)

- `level` is the project default: `advisory`, `flag-and-ask` or `review-gate` (meanings in
  `decision-cards.md`).
- `by_firmness` and `by_tension` raise the level for particular stances. They never lower it below the
  project default.
- The effective level for a proposal is the strictest of: the project level; the `by_firmness` level of any
  touched tension; the `by_tension` level of any touched tension; `flag-and-ask` whenever a hard limit is at
  risk or a touched tension is `contested`.
- A plain string (`"strictness": "advisory"`) is accepted as shorthand for `{"level": "advisory"}`.

## Amendment entries in the JSON

Two places record change, at two levels of detail.

**Top-level `amendment_log`:** one short index entry per document version. The map page and agents use it to
show a timeline without reading the full log.

```json
"amendment_log": [
  {"version": "1.0.0", "date": "2026-06-02", "id": "A0001", "change_type": "adopt",
   "tensions": ["T01@1", "T02@1", "T03@1", "T04@1", "T05@1"], "ratified_by": ["maintainer-a", "maintainer-b"],
   "summary": "First confirmed philosophy after interviews with both maintainers (illustrative)."},
  {"version": "1.1.0", "date": "2026-09-14", "id": "A0002", "change_type": "revise-stance",
   "tensions": ["T02@2"], "ratified_by": ["maintainer-a", "maintainer-b"],
   "summary": "Portability vs. raw speed moved to revision 2 (compiled extras are welcome when optional); synthesis refreshed."},
  {"version": "1.1.1", "date": "2026-11-20",
   "summary": "Recorded both maintainers' positions on T01; maintainer-b consents with a concern. No stance changed."}
]
```

(rowfold's log has the three `version`, `date` and `summary` lines; `id`, `change_type`, `tensions` and
`ratified_by` are added to the first two to show them.)

Required: `version`, `date`, `summary`. Optional: `id` (matching the full entry in `AMENDMENTS.md`),
`change_type`, `tensions` (with the new revision), `ratified_by`.

**Per-tension `amendments`:** `[{rev, date, summary}]`, a one-line history of that tension's revisions.

**Full entries** (before and after text, rationale, dissent, impact, commit) live in `AMENDMENTS.md`, which is
append-only. See `amendments.md`. Keeping the prose out of the JSON keeps the file an agent loads focused on
today's rulings.

## Individual maintainers' files

In a team, each maintainer's own philosophy lives at `individuals/<handle>/philosophy.json`, using the same
schema with `"holder": "<handle>"`. Differences from the shared file:

- IDs are local; `slug` matters most.
- `positions`, `dissent` and `decision` are not used; the stance is the person's own.
- `status` is normally `provisional`; `agreed` here means "I have confirmed this is my view".
- The file has its own `values` glossary in that maintainer's words (`by` is their handle). Two maintainers
  may define the same word differently; that is exactly what reconciliation needs to see.
- The file is never edited by reconciliation. It is the person's record, changed only by that person (through
  the skill or by hand).

## Validation checklist

Before saving, an agent checks:

- [ ] Every value has `id`, `name`, `rev`, `definition`, `looks_like`, `too_little`,
      `not_to_be_confused_with` and `in_own_words` (possibly `null` in a seed).
- [ ] Every pole and triad value has a `ref`, every network has `refs`, and each one resolves to a glossary
      entry whose `name` matches the value string.
- [ ] No value word is used in tension text, flip conditions or summaries in a sense its definition
      excludes.
- [ ] Every tension has `id`, `rev`, `slug`, `kind`, `name`, `stance.summary`, `stance.firmness`,
      `flip_conditions`, `precedents` and `status`.
- [ ] Polarities have exactly two `poles`, each with `value` and `good`; `position` is between -1 and 1.
- [ ] Triads have exactly three `values`; `weights` keys match the value names and sum to 1 (within 0.01).
- [ ] Networks have at least four values or explicit `sides`; `priority` lists every value once.
- [ ] Every value name used in a stance, edge, lever or position matches a name in that tension.
- [ ] No ID is duplicated, and no ID that appears in `AMENDMENTS.md` has been reused for something else.
- [ ] Every hard limit passes the opposite test the other way round: its opposite is NOT something the
      maintainers would ever accept.
- [ ] Every tension passes the acceptable-opposite test: each pole's `good` is something a reasonable
      project could choose.
- [ ] `version`, `last_amended` and `amendment_log` were updated if anything meaningful changed.
- [ ] `synthesis.text` is 3 to 5 plain sentences, uses value words in their defined senses, and
      `synthesis.as_of_version` equals `version` (or the staleness is deliberate and noted).

A quick syntax check needs only the standard library: `python3 -m json.tool philosophy.json > /dev/null`.

## Compatibility rules

- Readers ignore unknown fields. Writers keep fields they do not understand when they rewrite a file.
- Existing fields are never renamed or removed within schema 0.x.
- The core of the values glossary (`values` with `id`, `name`, `rev`, `definition`, `looks_like`,
  `too_little`, `not_to_be_confused_with`, `in_own_words`) and the `ref`/`refs` links are fixed. Optional
  glossary fields: `too_much`, `examples`, `by`, `confirmed`, `amendments`, `serves`, `stakeholders`,
  `facets`, `source`, `status`, `superseded_by`; plus the top-level `glossary_terms`.
- `synthesis` (`text`, `as_of_version`) exists so every view can open with a bottom line a newcomer can read
  on its own; the field names are fixed.
- Other optional fields in v0.1 of this skill, beyond the core: `holder`, `project_types`,
  `ratified`, `last_amended`, `non_goals`, `strictness`, `contradictions`, `levers`, `interop`; on
  hard limits `kind`, `protects`, `override`, `status`, `rev`; on tensions `early_warnings`, `evidence`,
  `greater_purpose`, `deeper_fear`, `mechanisms`, `necessity`, `scope`, `owner`, `review_by`, `dissent`,
  `decision`, `framing_status`, `supersedes`, `superseded_by`, `origin`, `rule`, `sides`, `edges[].relation`,
  `levers`; on stances `precision`, `pick`, `floors`, `posture`, `weights` (networks), `ordering`; on
  precedents `id`, `date`, `link`, `verdict`, `options_considered`, `would_have_changed_it`, `source`; on
  positions `stance_text`, `interests`, `intensity`, `source`; on log entries `id`, `change_type`, `tensions`,
  `ratified_by`.
