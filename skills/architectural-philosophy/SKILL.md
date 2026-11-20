---
name: architectural-philosophy
description: >-
  Interviews a project's maintainers to write down its architectural philosophy: defined values, the
  trade-offs it navigates (two-way, three-way and many-to-many), where it stands, when stances flip, hard
  limits and precedents. Keeps it living through versioned amendments, reconciles several maintainers'
  views without averaging, and has agents cite it in decision cards when proposing or reviewing changes. Use
  for capturing design values, principles, tenets or trade-offs of a library, app, package manager, research
  or data-analysis project, onboarding a maintainer, or checking a proposal against the philosophy. Not for
  writing a single ADR.
metadata:
  audience: any-agent
  domain: project-governance
  skill-version: "0.1.0"
  data-schema: "architectural-philosophy/0.1-draft"
---

# Architectural Philosophy

Helps a project write down how it makes trade-offs, keep that record current, and use it. The agent acts as a
neutral facilitator: it interviews each maintainer in four styles (abstract discussion of values, a
retrospective walkthrough of a real decision, forced-choice scenarios, and contradiction checks), defines every
value in the maintainer's own words before anything is weighed, and records the result as one plain JSON file
with a generated readable view and an interactive map page. The philosophy is living: interviews resume across
sessions, stances change through a logged amendment process, and a team's individual philosophies are
reconciled into a shared one through rounds that keep disagreement visible instead of averaging it. Later,
any agent working on the project reads the philosophy and explains its proposals through a short decision card
that cites the trade-offs by ID. It works for open-source libraries, applications, package managers, research
projects and data analyses, assumes no existing documentation system, and needs nothing beyond plain files
(Python's standard library is optional, for the helper scripts).

## What a philosophy contains

| Part | What it is | Example |
|------|-----------|---------|
| **Mission** | What the project is for, in a sentence or two | "A small, pure-Python library for reading and transforming tabular files, which many downstream projects depend on." |
| **Values glossary** | One explicit, operational definition per value, built from the maintainer's own explanation | Correctness: "The degree to which every table rowfold returns matches what the file actually holds, or rowfold raises a clear error instead of returning a guess." |
| **Hard limits** | Constraints that are never traded | "pip install works everywhere we support, with no compiler required." |
| **Tensions** | Trade-offs between values that are each worth wanting: a pair (polarity), three (triad), or four or more (network) | Portability vs. raw speed; Approachability, performance, correctness |
| **Stance** | Where the project sits on each tension, with firmness | "Portability first: the pure-Python parser is the reference. Compiled extras are welcome when optional." (firm) |
| **Flip conditions** | Observable conditions under which the stance changes | "Compiled code is welcome as an optional extra with a pure-Python fallback that gives identical results." |
| **Precedents** | Real past decisions that show the stance applied | "Optional [zstd] compression extra: compiled and opt-in; the standard-library path keeps working without it." |

The examples come from rowfold, a fictional tabular-file library whose full philosophy is in the skill
repository's `examples/rowfold/` folder.

**Bottom line up front.** Every document opens with a short plain-language summary: the philosophy with a
3-to-5-sentence `synthesis` that the agent drafts and the maintainers confirm (refreshed with every amendment
that changes a stance, hard limit or definition), and every decision card with a 2-to-4-sentence "Bottom
line". Detail follows. When writing these by hand, keep the page calm: summary first, detail later or
collapsed, plain text over decoration.

**Define before you weigh.** No value is weighed, ranked or traded until the maintainer has explained in their
own words what it means and confirmed a written definition. Every surface then shows that definition: interview
questions, canvases, `PHILOSOPHY.md`, the map page and decision cards. Agents use a value word only in its
defined sense; a new sense needs a logged glossary amendment. This is what keeps "Correctness" from meaning three
different things in three documents.

## Choose a mode

```
What does the user want?
├─ Write the project's philosophy for the first time ............ New interview → Interview flow below
│   └─ Detailed technique, question templates, pitfalls → ./references/interview-playbook.md
├─ Continue or extend an earlier interview ........................ Resume → session notes, then Interview flow
├─ Walk through a recent feature or decision as evidence ......... Review a feature → playbook step 5
├─ Change a stance, a definition or a flip condition ............. Amend → ./references/amendments.md
├─ Several maintainers' philosophies need to become one ......... Reconcile → ./references/reconciliation.md
├─ A new maintainer is joining ................................... Onboard → reconciliation.md, "Onboarding"
├─ Propose or review a change in a project that has a philosophy  Use it → Decision cards below
│   └─ Card format, proposal JSON, worked example → ./references/decision-cards.md
└─ Understand or edit the data file .............................. ./references/data-model.md
```

Several modes often happen in one session: a resume that turns up a contradiction becomes an amendment.

## Where this runs

The skill uses the open Agent Skills folder format (a `SKILL.md` with `references/`, `assets/` and `scripts/`),
which Claude Code, the claude.ai apps, OpenAI Codex and ChatGPT, GitHub Copilot, Cursor and Gemini CLI all load
natively. No single folder is read by every host, so the recommended layout uses two locations:

- the real folder at `.agents/skills/architectural-philosophy/` (read by Codex, Copilot, Cursor and Gemini CLI);
- a symlink at `.claude/skills/architectural-philosophy` pointing to it (read by Claude Code, Copilot and
  Cursor). On a checkout without symlink support (some Windows setups), copy the folder instead.
- With the user's permission, a two-line pointer in `AGENTS.md` (and in `CLAUDE.md`, `GEMINI.md` or
  `.github/copilot-instructions.md` if the project uses them) naming the skill and its path, for hosts or
  sessions that do not load skills.

| Host | Make the skill available | Canvas routes that usually work |
|------|-------------------------|---------------------------------|
| Claude Code, local terminal | The layout above, or `~/.claude/skills/` for all projects | a (Artifact, if the user agrees), b, e |
| Claude Code on the web | Commit the layout to the repository (or enable the skill on the claude.ai account) | a if available, otherwise e; no helper server |
| claude.ai and Claude desktop chat | Turn on code execution, zip the folder, upload it as a skill | d (chat Artifact plus paste), e |
| Codex (CLI, IDE, desktop app) | `.agents/skills/` (repository) or `~/.agents/skills/` | b when running locally, e |
| Codex cloud, Copilot cloud agent | Commit the layout to the repository (Codex cloud loading is unverified) | e only |
| ChatGPT web | Standalone skills are desktop-only; on the web a skill must come inside a plugin | d (HTML preview plus paste), e |
| Copilot in VS Code, Copilot CLI | Any of `.github/skills/`, `.claude/skills/`, `.agents/skills/` | b (ports forward in Remote, Dev Containers, Codespaces), c, e |
| Cursor | `.agents/skills/` or `.cursor/skills/` (also reads `.claude/skills/`) | b, e |
| Gemini CLI | `.agents/skills/` or `.gemini/skills/`; approve the activation prompt | b, e |

Bundled scripts need only Python's standard library, but a helper server is useful only where the user's
browser can reach it, which rules out cloud sandboxes. Host features change often; this table reflects a
documentation review dated 2026-11-20. When unsure, try a route and drop down the ladder in
`./references/canvases.md`.

## Files the skill creates in the project

Default folder: `docs/philosophy/`. Ask the user before creating it; a project may prefer `philosophy/`,
`.github/philosophy/`, or a folder beside existing design docs. Use a distinct folder rather than mixing files
into an existing docs system, so the philosophy never collides with `PRODUCT.md`, `DESIGN.md`, a Spec Kit
constitution or agent-instruction files. Record the chosen path in the pointer section (below) so later agents
find it.

```
docs/philosophy/
├── philosophy.json          canonical data: glossary, hard limits, tensions, stances (edit this)
├── PHILOSOPHY.md            generated readable view; what agents read by default (do not hand-edit)
├── philosophy-map.html      generated interactive map; one self-contained file, opens from disk
├── AMENDMENTS.md            append-only amendment log, full entries
├── GOVERNANCE.md            teams only: participants, decision rules, comment windows, strictness
├── individuals/<handle>/    one per interviewed maintainer
│   ├── philosophy.json      that person's own philosophy (teams; never edited by reconciliation)
│   ├── session-notes.md     resumable interview state
│   └── canvases/            canvas specs and results (optional to keep)
├── reconciliation/<YYYY-MM-DD>_<slug>/   teams only: one folder per reconciliation cycle
└── proposals/               optional: proposal JSON files for the map overlay
```

A solo maintainer's answers go straight into `philosophy.json`; `individuals/<handle>/` then holds only
session notes and canvases. In a team, each person's answers go into their individual file, and the shared file
is produced by reconciliation.

## First steps in any project

1. **Look for an existing philosophy.** If `philosophy.json` exists (check the pointer section in the agent
   instructions, then `docs/philosophy/`), read it, the relevant session notes and `GOVERNANCE.md`, and treat
   the request as resume, amend, reconcile or use.
2. **Detect what the project already has, and assume none of it.** Check for: `AGENTS.md` (root and nested),
   `CLAUDE.md` and `.claude/rules/`, `.cursor/rules/`, `.kiro/steering/`, `.github/copilot-instructions.md`,
   a Spec Kit constitution (`.specify/memory/constitution.md`), ADR folders (`doc/adr/`, `docs/adr/`,
   `docs/decisions/`, `doc/architecture/decisions/`, files named `NNNN-*.md` or `adr-*.md`), proposal processes
   (`rfcs/`, `peps/`, `keps/`, `docs/design/`), `CONTRIBUTING.md`, `README`, `ARCHITECTURE.md`, `PRODUCT.md`,
   `DESIGN.md`, and for research or analysis projects any pre-registration, protocol or methods document.
   Record what was found in `interop.detected`.
3. **Read them as inputs, not answers.** They supply real decisions for retrospective walkthroughs, candidate
   values, and possible contradictions to raise. They are not shown to the maintainer before the maintainer has
   spoken in their own words. A Spec Kit constitution's non-negotiable rules usually map to hard limits; record
   them as such rather than duplicating or contradicting them.
4. **Agree the plan with the user:** the folder, who is being interviewed (and their handle), solo or team,
   whether canvases are welcome, and roughly how long this session runs.
5. **Pointer section, only with permission.** Once a philosophy exists, offer to add a short section to the
   agent-instruction file the project already uses. Never create a new instruction file unasked, and never edit
   one without the user's yes. Record what was added in `interop.pointers`. A generic stanza:

```markdown
## Architectural philosophy
This project records its core trade-offs in `docs/philosophy/PHILOSOPHY.md` (tensions like T02, values like
`correctness`, each with a definition). Before proposing or reviewing a change that touches one of those
trade-offs, read the current file, check its hard limits, and include a decision card (format: the
architectural-philosophy skill, or the "Decision cards" section of PHILOSOPHY.md). Use value words only in
their defined sense. Strictness: advisory. If a stance no longer seems to fit, say so and suggest an
amendment. Explicit instructions from the user take precedence.
```

## Interview flow at a glance

The full method, with question templates for software and research projects, is in
`./references/interview-playbook.md`. In outline:

1. **Orientation.** Mission, project type, who is affected, non-goals.
2. **Their words first.** Open questions and "why does that matter?" chains, and three-way comparisons of real
   past features, produce a candidate list of values and tensions in the maintainer's vocabulary. No catalog is
   shown yet.
3. **Define before you weigh.** For each key value: an open prompt ("When you say Correctness here, what do
   you mean?"), an example done well and one missing or faked, the boundary ("What do people call Correctness that you
   would not?"), too little and too much. Only then does the agent draft the definition and indicators, read
   them back, and record the maintainer's elaboration verbatim. Obvious values get a quick confirm instead.
   (A `define` canvas widget asks the same questions in writing, for maintainers who prefer that.)
4. **Shape each tension.** Problem or ongoing tension? Does each side pass the acceptable-opposite test (could a
   reasonable project prefer it)? Two, three or more values? Hard limit or tradeable? Inherent or contingent?
5. **Retrospective walkthrough** of one or two real decisions: the story, the decision points, what was
   noticed and weighed, and "what would have made you choose differently?"
6. **Forced choice:** place each stance (spectrum, triangle, allocation, ranking) and test with concrete
   dilemmas. **Open a canvas here** when placing three or more values, ranking six or more, or placing several
   stances at once; otherwise ask in plain text.
7. **Flip conditions and early warnings:** "When would you lean the other way?" and "What early sign would tell
   you the project has gone too far?"
8. **Seed check:** a few tensions from `./references/tension-library.md`, filtered by project type, as "did we
   miss anything?"
9. **Contradiction check:** first ask whether two answers used a value in different senses; then raise the
   remaining conflicts neutrally, as probable undiscovered flip conditions.
10. **Read back, write, render, save.** Update the JSON, draft or refresh the `synthesis` and read it back for
    confirmation, regenerate the views, update the session notes, and suggest a commit message.

Pace: 30 to 60 minutes and three to five tensions per session; save state after every tension so any session
can stop and resume.

## Tools

All tools are optional conveniences with a plain-file fallback. They need only Python 3's standard library: no
packages, no network, no build step. `<skill-dir>` is this skill's folder.

| Tool | Command | Fallback without Python |
|------|---------|------------------------|
| Render the readable view and map | `python3 <skill-dir>/scripts/render.py docs/philosophy/philosophy.json --html docs/philosophy/philosophy-map.html --md docs/philosophy/PHILOSOPHY.md` | Write `PHILOSOPHY.md` by hand from the JSON; open `assets/philosophy-map.html` and use its "Open a philosophy file" control, or paste the JSON into its data block |
| Overlay a proposal on the map | add `--proposal docs/philosophy/proposals/<name>.json` | Paste the proposal JSON into the map page's "Overlay a proposal" box |
| Serve a canvas and collect the answers | `python3 <skill-dir>/scripts/canvas_server.py SPEC.json --out RESULT.json [--port N] [--host H] [--timeout S]` | Inline the spec into a copy of `assets/canvas.html`; the maintainer opens the file and uses "Copy answers" or "Download answers" |
| Check the JSON parses | `python3 -m json.tool docs/philosophy/philosophy.json > /dev/null` | Validation checklist in `./references/data-model.md` |

**Running the canvas server:** start it in the background with a timeout, read the printed `CANVAS URL: ...`
line and hand that URL to the maintainer, then wait for the process to exit. It accepts one token-checked
submission, writes the result file, prints `RESULT: <path>`, and exits. Do not end a turn with it still
running unless you say so.

**Choosing how to deliver a canvas:** use the first route that works: (a) a native return channel such as a
published Artifact in Claude Code, only with the user's consent; (b) the local helper server, when Python runs
and the browser can reach this machine; (c) VS Code's built-in browser, read back by the agent; (d) a host's HTML
preview with copy and paste; (e) the plain HTML file with copy and paste or download, which always works; (f) no
canvas, the same questions in text. Pasted answers are one JSON object with a schema version; check it before
recording anything (`./references/canvases.md`).

## Using the philosophy when proposing or reviewing a change

Any agent working in a project with a philosophy follows this contract (details and a worked example in
`./references/decision-cards.md`):

1. **Read the current file**, not memory. Note the version and strictness.
2. **Check hard limits first.** A proposal that crosses one stops for a human decision at every strictness
   level.
3. **Find the touched tensions,** looking at levers and mechanisms first.
4. **Write a decision card** that opens with a 2-to-4-sentence **Bottom line** (what is proposed, the overall
   fit, the one decision needed), then: a one-sentence proposal ("In the context of ..., facing T02 Portability vs. raw speed, I
   propose X over Y, to gain ..., accepting ..."); each value cited by `id@rev` with its one-line definition
   quoted at first mention; a table of touched tensions cited as `T02@1`, each with exactly one verdict
   (Consistent, Departs, Flip condition met, with the condition quoted); options including doing nothing and
   one option at the stance's preferred pole; precedents followed or departed from; and the one decision needed.
5. **Skip the card** for mechanical or local changes, and say "No philosophy tensions touched."
6. **Contested tensions:** present the recorded positions and ask; never pick a side.
7. **Permission to question:** if a stance no longer fits, say so and propose an amendment rather than
   contorting the proposal. Never edit the philosophy as a side effect of feature work.

## Strictness

The philosophy is advisory by default. A project can raise strictness overall or for particular stances in
`philosophy.json` (`strictness`, see `./references/data-model.md`).

| Level | What the agent does when a proposal departs from a stance |
|-------|-----------------------------------------------------------|
| **advisory** (default) | Explains the departure in a card for significant proposals; proceeds if the user's instruction covers it. |
| **flag-and-ask** | Stops before implementing and asks the card's "Decision needed" question. |
| **review-gate** | Saves the card with the change; implementation waits for written human approval or an amendment. |

The effective level for a proposal is the strictest of the project level, any level set for a touched
tension's firmness (for example `core` stances at flag-and-ask), any level set for a touched tension, and
flag-and-ask whenever a hard limit is at risk or a touched tension is contested. To change the setting, ask
which stances deserve a stop-and-ask and why, record it, and log it as an amendment. Be honest that these levels
are a contract the agent follows: they become a hard gate only if the team adds its own check, such as a CI step
that looks for a card in the pull request.

## Facilitator posture

- Surface and record the maintainers' judgments; never supply values of your own or rank theirs.
- Their words first, framework vocabulary later; quote rather than paraphrase.
- Never propose a number, position or weight before the maintainer places one.
- Treat "it depends" as a flip condition waiting to be named, and contradictions as probable missing conditions
  or words used in two senses, never as errors to catch.
- Keep sessions to philosophy work; park feature ideas in the session notes.
- Never average maintainers' stances, declare consensus, or edit someone's individual file during
  reconciliation.
- Suggest commit messages; commit only when asked.

## Topic index

| Topic | Reference |
|-------|-----------|
| Facilitator posture, session pacing, resumable session notes | `./references/interview-playbook.md` |
| Define before you weigh: the six-step definition sequence | `./references/interview-playbook.md` |
| Abstract style: opening questions, laddering, triads | `./references/interview-playbook.md` |
| Retrospective walkthrough (four sweeps); reviewing a recent feature | `./references/interview-playbook.md` |
| Forced choice: swing weights, best-worst, allocation, dilemmas, floor probe | `./references/interview-playbook.md` |
| Contradiction checks and how to raise them | `./references/interview-playbook.md` |
| Acceptable-opposite test; seeding from documents; wording by project type | `./references/interview-playbook.md` |
| JSON schema, field by field; glossary, tension shapes, firmness, status | `./references/data-model.md` |
| Stable IDs and citation (`T04@2`, `correctness@2`); validation checklist | `./references/data-model.md` |
| Strictness settings in the data file | `./references/data-model.md` |
| Starter tensions by project type; value palettes; stance forms | `./references/tension-library.md` |
| Canvas widgets, specs, delivery ladder, result mapping, pitfalls | `./references/canvases.md` |
| Decision card template, verdicts, proposal JSON, review use, rowfold example | `./references/decision-cards.md` |
| Team reconciliation: governance, alignment classes, rounds, decision rules | `./references/reconciliation.md` |
| Endorsement levels, recording dissent, onboarding a new maintainer | `./references/reconciliation.md` |
| Revisions, document versions, amendment log format, git practice | `./references/amendments.md` |
| Agent-proposed amendments; repeated departures; splits and retirements | `./references/amendments.md` |
