# Elicitation canvases

Canvases are small interactive pages the agent opens during an interview so the maintainer can place a stance
directly: click a point on a spectrum, drag a point inside a triangle, split 100 points, drag values into an
order, or choose between two concrete options. Each widget also takes a free-text note, and the answers flow
back into the conversation as JSON. Canvases are optional; every question they ask can also be asked in plain
text.

## Contents

- When a canvas helps, and when plain questions are better
- The widget catalog
- Definitions on every widget
- Writing a canvas spec
- Choosing a delivery route (the ladder)
- Route a: a native return channel
- Route b: the local helper server
- Route c: VS Code's built-in browser
- Route d: a host preview without a return channel
- Route e: the plain file (always available)
- Route f: no canvas
- Checking pasted answers
- The result JSON
- Mapping results into the data model
- Pitfalls: anchoring, false precision, and others

---

## When a canvas helps, and when plain questions are better

| A canvas helps when | Plain questions are better when |
|---------------------|--------------------------------|
| The maintainer must place a stance among three or more values (a triangle or an allocation is much easier to do than to describe) | The maintainer is still finding words for their values (steps 2 and 3 of the playbook) |
| Several tensions need placing in one sitting, and seeing them side by side helps consistency | The stance is obvious from what they already said; read it back instead |
| Ranking six or more values, with a "never trade" line | The point is a story (a retrospective walkthrough) |
| A forced choice between two concrete options, where seeing both laid out side by side matters | The maintainer prefers talking, or is on a device where the page is awkward |
| A team: each maintainer answers the same canvas privately before any comparison | The question is about a definition or a boundary; that usually needs conversation (the `define` widget is for maintainers who prefer to write) |

Canvases come after "define before you weigh" (`interview-playbook.md`, step 3): a value is placed only once it
has a confirmed definition, and the canvas shows that definition.

Ask the maintainer once, early, whether they want canvases at all, and respect the answer.

## The widget catalog

The canvas template (`assets/canvas.html`) provides six widgets. Each implements an established elicitation
technique.

| Widget | What the maintainer does | Technique it implements | Fits |
|--------|--------------------------|-------------------------|------|
| `spectrum` | Clicks a position between two poles; snaps to a few steps; separate "it depends" and "don't know" buttons | Rating on a two-ended construct (repertory grid); polarity lean | Polarity `stance.position` |
| `triangle` | Places a point inside a triangle whose corners are three values; snaps to a 10 percent grid | Three-way point allocation; "pick two" | Triad `stance.weights` |
| `allocate` | Splits 100 points across four or more values, with a visible running total that must reach 100 | Budget allocation; the second step of swing weighting | Network `stance.weights` |
| `rank` | Drags values into order and can place a "never trade above this line" marker; allows ties | Ranking; lexicographic order; value "dams" from value sensitive design | Network `stance.priority`; hard-limit candidates |
| `dilemma` | Chooses between concrete options and says what would make them pick the other | Conjoint-style choice; scenario from architecture trade-off analysis | Flip conditions; precedent-like evidence |
| `define` | Explains a value in their own words: what it means here, an example done well, an example missing or faked, what people wrongly call by that name, and how it differs from a named neighbouring value; then marks any draft definition "looks right" or "needs changes" | Laddering and repertory-grid style boundary probes; the "define before you weigh" sequence | Glossary `in_own_words`, `examples`, `not_to_be_confused_with` |

Every widget has a note box, and every widget except `define` asks how firm the answer is (Loose, Firm,
Non-negotiable) and requires one line of reason for the firmer two. A number without a reason is weak
evidence.

The `define` widget suits a maintainer who prefers writing to talking, or a team where each maintainer explains
the key values privately before reconciliation. It does not replace the conversation in playbook step 3: the
agent still drafts the definition from the answers, reads it back, and gets a confirmation.

Widgets start empty. There is no default handle on a spectrum, no default point in a triangle, no pre-filled
allocation, and ranking lists start shuffled. This is deliberate (see "Pitfalls").

## Definitions on every widget

Every value a widget shows is displayed with its glossary definition, taken from the `values` glossary in
`philosophy.json` and carried in the spec's `glossary` array. The maintainer should never place a stance on a bare word. Show at
least the one-line `definition`; show `looks_like`, `too_little` and `not_to_be_confused_with` on hover or
expansion where space allows. If a value has no confirmed definition yet, define it first (playbook step 3, or
a `define` widget) rather than placing it on a canvas. Each displayed value also has an "Edit this definition"
control; anything the maintainer writes there comes back as `definition_feedback`, which the agent treats as a
proposed glossary change to discuss, never as an automatic edit.

## Writing a canvas spec

A spec is a small JSON file the agent writes for one canvas session. It names the respondent, carries the
glossary entries for every value shown, and lists the widgets. The authoritative field list is the comment at
the top of `assets/canvas.html`; if this reference and the template ever disagree, the template wins.

```json
{
  "schema": "architectural-philosophy-canvas/0.1",
  "id": "2026-05-20_maintainer-a_session2",
  "title": "Where does rowfold stand?",
  "project": "rowfold (example package)",
  "intro": "Place each stance. There are no right answers; add a sentence on why.",
  "respondent": "maintainer-a",
  "glossary": [
    {"id": "correctness", "name": "Correctness", "rev": 1,
     "definition": "The degree to which every table rowfold returns matches what the file actually holds, or rowfold raises a clear error instead of returning a guess."},
    {"id": "performance", "name": "Performance", "rev": 1,
     "definition": "How quickly, and within how little memory, rowfold reads and transforms large files on a single machine."},
    {"id": "portability", "name": "Portability", "rev": 1,
     "definition": "The range of Python versions, operating systems, CPU architectures and runtimes on which rowfold installs and gives the same results without extra tools."}
  ],
  "widgets": [
    {"id": "def-correctness", "kind": "define", "prompt": "Tell me what Correctness means in rowfold.",
     "value": {"value": "Correctness", "ref": "correctness"}, "neighbor": {"value": "Performance", "ref": "performance"}},
    {"id": "T02-spectrum", "kind": "spectrum", "tension_id": "T02",
     "prompt": "When rowfold could be faster with compiled code, where should it sit?",
     "poles": [{"value": "Portability", "ref": "portability"}, {"value": "Performance", "ref": "performance"}], "steps": 5},
    {"id": "T04-triangle", "kind": "triangle", "tension_id": "T04",
     "prompt": "If rowfold can only protect two of these fully, how would you weight all three?",
     "values": [{"value": "Approachability", "ref": "approachability"}, {"value": "Performance", "ref": "performance"},
                {"value": "Correctness", "ref": "correctness"}]},
    {"id": "T06-allocate", "kind": "allocate", "tension_id": "T06",
     "prompt": "Split 100 points of emphasis for the plugin interface.",
     "values": [{"value": "Compatibility", "ref": "compatibility"}, {"value": "Small core", "ref": "small-core"},
                {"value": "Batteries included", "ref": "batteries-included"}, {"value": "Approachability", "ref": "approachability"}],
     "total": 100, "step": 5},
    {"id": "core-rank", "kind": "rank",
     "prompt": "Order these. Move the line above anything you would never trade away.",
     "values": [{"value": "Correctness", "ref": "correctness"}, {"value": "Compatibility", "ref": "compatibility"},
                {"value": "Portability", "ref": "portability"}, {"value": "Clarity", "ref": "clarity"}]},
    {"id": "D1", "kind": "dilemma", "tension_id": "T01",
     "prompt": "A confusing argument",
     "scenario": "The skip argument of read() skips rows, but many users expect it to skip columns. About forty downstream packages pass skip= today.",
     "options": [
       {"id": "A", "label": "Add a clearer skip_rows and deprecate skip", "detail": "skip keeps working with a warning for two minor releases, then goes away in the next major release."},
       {"id": "B", "label": "Keep skip and fix the documentation", "detail": "No downstream code changes; the name stays confusing for new users."}],
     "flip_prompt": "What would make you pick the other option?"}
  ]
}
```

(The glossary entries for `approachability`, `compatibility`, `small-core`, `batteries-included` and `clarity`
are omitted above for brevity; a real spec includes every value it uses. T06 is the illustrative network
tension from `data-model.md`. A complete, working spec for rowfold, with its rendered page, is in the skill
repository's `examples/rowfold/` folder.)

Guidance:

- A value in a widget is a plain name or `{"value", "ref", "definition", "good"}`. Its displayed definition comes
  from the value itself, else from `glossary[ref]`, else from the glossary entry with the same name. Use `ref`
  and copy the glossary entries from `philosophy.json`, so the canvas shows exactly the confirmed definitions.
- Link widgets to tensions with `tension_id`.
- The template shuffles the order of values, options and triangle corners by default (`randomize`), and can
  swap spectrum sides (`randomize_sides`). Leave that on unless order carries meaning.
- `spectrum` takes `steps` of 5 or 7 (default 7). `allocate` takes `total` (default 100) and `step` (default 5).
  `rank` takes an optional `line_label`. Any widget can set `"firmness": false` to skip the firmness question.
- One canvas per sitting, usually three to six widgets. More invites fatigue.
- Dilemma options are built from the project's real levers and precedents, phrased as concrete outcomes, with
  roughly equal detail on each side.
- Save specs and results under `individuals/<handle>/canvases/`, named by date, for example
  `2026-11-21_session2.spec.json` and `2026-11-21_session2.result.json`.

## Choosing a delivery route (the ladder)

A canvas page has to reach the maintainer's browser, and the answers have to come back to the agent. Showing
HTML is easy on most hosts; getting structured answers back without the maintainer pasting them is possible on
only a few. So the skill offers a ladder. Walk down it and use the first route that works where you are
running. Every route ends with the same answer JSON (see "The result JSON"), so nothing after this step depends
on which route ran. Copy and paste is the guaranteed floor: it works on every host.

```
Which route?
├─ a. A native return channel is available (an Artifact tool in Claude Code), and the user agrees to publish
│     → publish the canvas as a private Artifact; read the saved answers back
├─ b. Python 3 runs here AND the user's browser can reach this machine
│     (local terminal, VS Code Remote or Dev Containers, Codespaces, a container with a published port)
│     → local helper server
├─ c. Running as a VS Code agent with browser tools → open the canvas in VS Code's built-in browser; read it back
├─ d. The host previews HTML but has no return channel (a claude.ai chat Artifact, ChatGPT's HTML preview)
│     → show the canvas there; the maintainer copies the answers back
├─ e. Otherwise, including every cloud sandbox → the plain HTML file; copy and paste, or download
└─ f. The maintainer prefers no canvas, or there is no browser → ask the same questions in text
```

Tell the maintainer which route you chose and what they will need to do (open a link, open a file, copy the
answers back), in one or two sentences. If a route fails, drop to the next one without fuss.

**Cloud sandboxes cannot reach a helper server.** In Claude Code on the web, Codex cloud and the GitHub Copilot
cloud agent, there is no documented way for the maintainer's browser to reach a port inside the sandbox. Start
at route a (where an Artifact tool exists) or go straight to route e.

**The agent cannot reliably detect whether a port is reachable.** The safe pattern is to start the server, give
the maintainer the URL, and ask them to confirm it opened. Hints that route b can work: a local session, or
environment variables such as `TERM_PROGRAM=vscode`, `REMOTE_CONTAINERS` or `CODESPACES`.

Host capabilities change often. The statements below come from a documentation review dated 2026-11-20 (the
project's portability research); items marked "unverified" were not confirmed in that review.

## Route a: a native return channel

**Claude Code with an Artifact tool.** When the agent's tool list includes an Artifact tool (Claude Code signed
in with a claude.ai account), the canvas can be published as a private Artifact. The page stores the answers in
the Artifact's saved data, or the maintainer sends them to the session, and the agent reads them back with the
platform's own tools, with no pasting. To build it, inline the spec into the canvas template as in route e, and
give the page a way to save its answers through the platform's data mechanism. If that wiring is not available,
the page's "Copy answers" button still works, which makes this route d.

- **Ask before publishing.** Publishing puts the page, including the project's values and definitions, on a
  hosted service, even when it is private. Some users and projects require explicit consent, and some never
  want it.
- Whether this works the same in Claude Code's cloud sessions is unverified; fall back to route e if not.

**MCP Apps (optional add-on, not part of the core skill).** Some hosts (ChatGPT, VS Code with Copilot, Cursor,
Claude on the web and desktop, and others) render interactive pages supplied by an MCP server, and those pages
can send messages back to the conversation. This route counts only if the project has already installed an MCP
server that serves this skill's canvases. The core skill does not include one, because it would add a server
to install, against the skill's minimal-dependency design.

## Route b: the local helper server

Use when Python 3 is available and the maintainer's browser can reach the machine the agent runs on: a local
terminal; VS Code Remote (SSH, WSL) or Dev Containers, which forward ports (forwarded ports look like localhost,
so the default `127.0.0.1` bind works); or GitHub Codespaces, which turns a `http://localhost:PORT` URL printed
in the terminal into a forwarded, clickable link. It needs only Python's standard library.

```bash
python3 <skill-dir>/scripts/canvas_server.py SPEC.json --out RESULT.json \
    [--port N] [--host H] [--url-port N] [--timeout SECONDS] [--overwrite]
```

1. **Start it in the background** and wait for it to exit. It prints one line, `CANVAS URL:
   http://localhost:PORT/?t=TOKEN`; hand that URL to the maintainer and ask them to confirm it opened.
2. The maintainer fills the canvas and presses "Send to interviewer". The server checks the one-time token and
   the request's origin, accepts exactly one submission, writes `RESULT.json`, prints `RESULT: <path>`, and
   exits with code 0.
3. When the background process exits, read the result file and continue.
4. With no submission before the timeout (default 1800 seconds), it prints a `TIMEOUT` line and exits with code
   3, so a background wait always ends. Exit code 2 means a usage or startup error.
5. If the link does not open, stop the server and drop to route c, d or e with the same spec. The served page
   also has "Copy answers" and "Download answers", so answers are never trapped.

**Docker without VS Code forwarding:** the port must be published (for example `-p 127.0.0.1:3000:3000`) and
the server must bind `--host 0.0.0.0 --port 3000` inside the container; an app bound only to localhost inside a
container is not reachable through a published port. If the browser uses a different port number than the
container, pass it as `--url-port` so the printed URL and the server's host check match. Without a published
port, use route e.

Do not end a turn with the server still running unless you say so, with its process ID and how it will end.

## Route c: VS Code's built-in browser

When the agent runs in VS Code with its browser tools (the integrated browser, which an agent can open pages in
and read), open the canvas there: either the helper server's URL or the plain file from route e. When the
maintainer presses "Copy answers", the page fills a visible "Your answers" box with the answer JSON, and the agent
reads the page. Two points are unverified: whether the browser tools open `file://` pages, and whether reading
the page returns the contents of that box. If either fails, ask the maintainer to paste the answers instead.

## Route d: a host preview without a return channel

Some hosts render HTML but give the page no way to send data into the current conversation: a claude.ai or
Claude desktop chat Artifact, or ChatGPT's code-block HTML preview. Show the canvas there (the self-contained
page from route e), and the maintainer presses "Copy answers" and pastes the result into the chat. Ask before
publishing anything hosted, as in route a.

## Route e: the plain file (always available)

Needs nothing but a browser.

1. Copy `assets/canvas.html` to the session's canvas folder and replace the contents of its
   `<script type="application/json" id="canvas-spec">` block (which holds `null`) with the spec. If any text
   in the spec contains `</`, write it as `<\/` so it cannot close the script block early. If Python is
   available a short script can do this; if not, the agent writes the HTML file directly.
2. Give the maintainer the file path and ask them to open it in a browser. In a cloud session they download it
   from the session's branch or files first.
3. When they are done, they press **Copy answers** and paste into the chat (if the clipboard is blocked, the
   page shows the same JSON in a visible box to select and copy), or press **Download answers** and save the file
   into the project where the agent can read it.
4. Check the pasted answers (below), save them as the session's result file, and continue.

## Route f: no canvas

If the maintainer prefers text, or there is no browser at all (a terminal over SSH, a phone), ask the same
questions in plain text, showing each value's definition:

| Widget | Text form |
|--------|-----------|
| `spectrum` | "On a scale from -3 (strongly `<A>`) to +3 (strongly `<B>`), with 0 for even, where does the project sit? Or is it 'it depends'?" |
| `triangle` | "Split 100 percent among `<A>`, `<B>` and `<C>`, in steps of 10." |
| `allocate` | "Split 100 points among these, in steps of 5." |
| `rank` | "Put these in order, and say which, if any, you would never trade away." |
| `dilemma` | "Option 1 ... Option 2 ... Which ships? What would make you pick the other?" |
| `define` | The six-step sequence in `interview-playbook.md`, step 3. |

Record the answers exactly as a canvas result would be recorded (a -3 to +3 answer divides by 3 to give the
position), with `"via": "text"` noted in the session notes.

## Checking pasted answers

Pasted text can be truncated, edited, or from an older canvas. Before recording anything:

1. Confirm it parses as one JSON object whose `schema` is `architectural-philosophy-canvas-result/0.1` (or a
   later 0.x version).
2. Confirm `canvas_id` matches the spec you sent and `respondent` is the person you are interviewing.
3. Confirm each `results[].widget` matches a widget in the spec, and note any widget with `answered: false`.
4. If any check fails, say what is wrong and ask the maintainer to copy again. Never guess at missing values.

## The result JSON

Every submission has the same envelope (schema `architectural-philosophy-canvas-result/0.1`; the exact list is
in the template's header):

```json
{
  "schema": "architectural-philosophy-canvas-result/0.1",
  "canvas_id": "2026-05-20_maintainer-a_session2", "canvas_title": "Where does rowfold stand?",
  "project": "rowfold (example package)", "respondent": "maintainer-a", "submitted_at": "2026-05-20T15:02:11Z", "via": "server",
  "results": [
    {"widget": "T02-spectrum", "kind": "spectrum", "tension_id": "T02",
     "result": {"choice": "position", "position": -0.5, "step_index": 1, "steps": 5,
                "label": "...", "scale": "-1 = fully Portability, +1 = fully Performance"},
     "initial_state": null, "adjustments": 2, "seconds_spent": 41, "answered": true,
     "firmness": "firm", "reason": "Install failures cost us more users than slow parsing does.",
     "note": "Optional compiled extras are fine.", "definition_feedback": [],
     "presentation_order": ["Portability", "Performance"], "respondent": "maintainer-a", "timestamp": "2026-05-20T15:01:30Z"}
  ]
}
```

Per-kind `result` shapes:

| Kind | `result` |
|------|----------|
| `spectrum` | `{choice: "position", position, step_index, steps, label, scale}`, or `{choice: "depends", depends_on}`, or `{choice: "dont_know"}` |
| `triangle` | `{weights: {name: share}, refs, precision: 0.1}` |
| `allocate` | `{points: {name: n}, total, sum, complete, refs}` |
| `rank` | `{order, above_line, below_line, refs, confirmed}` |
| `dilemma` | `{chosen, chosen_label, would_flip_if, leans_toward}` |
| `define` | `{value, ref, neighbor, own_words, example_good, example_missing, misnomers, differs_from_neighbor, draft_verdict, requested_change}` |

`initial_state` and `adjustments` let the agent notice an answer that never moved, or one adjusted many times
(real uncertainty worth asking about). `presentation_order` records the shuffled order the maintainer saw.

## Mapping results into the data model

Canvas results are drafts. Read each one back in words before recording it ("You put the project clearly toward
Portability and marked it firm, noting that optional compiled extras are fine. Is that right?").

| Widget | Becomes | Notes |
|--------|---------|-------|
| `spectrum` | Polarity `stance.position` | The canvas reports -1 for the first pole shown in the spec's `poles`. Check that this matches the tension's `poles[0]`, and flip the sign if the spec listed them the other way. `depends` leads straight to a flip-condition question ("Depends on what?"); `dont_know` leaves the stance unplaced. |
| `triangle` | Triad `stance.weights` | Ask the pick-two and floor questions next, for `pick` and `floors`. |
| `allocate` | Network `stance.weights` (points divided by the total) and a derived `priority` (largest first) | Ties in points become a question; check the derived order with the maintainer. An incomplete allocation (`complete: false`) is not recorded. |
| `rank` | Network `stance.priority` | Values `above_line` are hard-limit candidates; confirm each with the floor probe before adding it to `hard_limits`. |
| `dilemma` | A `flip_conditions` entry from `would_flip_if`, and evidence for the stance | It was a hypothetical, not a real decision; record it as evidence, not as a precedent. |
| `define` | Material for the glossary entry: `in_own_words` (from `own_words`), `examples.good`, `examples.missing_or_faked`, `not_to_be_confused_with` (from `misnomers` and `differs_from_neighbor`) | The agent drafts the definition from these answers and reads it back for confirmation (playbook step 3). `needs_changes` with a `requested_change` means the draft is revised. |
| `firmness` | `stance.firmness` | Canvas "Loose" maps to `working` (or `exploratory` if the note says the maintainer is unsure); "Firm" to `firm`; "Non-negotiable" (`core`) needs one question: "Is this never traded at all (a hard limit), or core to the project but tradeable in extreme cases?" Record `core` or a hard limit accordingly. |
| `reason`, `note` | `evidence.quotes` | Keep verbatim. |
| `definition_feedback` | A proposed glossary change | Discuss it with the maintainer; if confirmed, revise the definition (and its `rev`, if the meaning changed) through an amendment. Never apply it silently. |

Then add `"forced-choice"` to the tension's `evidence.styles`, and the result file path to `evidence.canvases`.
Store numbers at the precision the widget produced (spectrum steps, a 10 percent triangle grid, 5-point
allocation steps). A canvas result alone is one style of evidence; it still benefits from a real precedent or an
abstract statement that agrees with it.

## Pitfalls: anchoring, false precision, and others

| Pitfall | Why it happens | What the canvas and the agent do |
|---------|----------------|----------------------------------|
| **Default anchoring** | Survey experiments show respondents pick a slider's starting value far more often when one is preset. | No starting handle, point or allocation; ranking lists start shuffled. The agent never suggests a position before the maintainer places one. |
| **False precision** | A slider at 73 looks more exact than the judgment behind it. | Snap to coarse steps; record rough values; read back in words ("clearly toward"), not decimals. |
| **Continuous sliders cost effort without adding information** | Studies of web surveys found sliders lowered response quality compared with clicking a position. | Click-to-place on a few positions rather than free dragging. |
| **Midpoint ambiguity** | "Balanced" can mean equal, unsure or "it depends". | Separate "it depends" and "don't know" buttons; "it depends" leads to a flip condition. |
| **Order effects** | The first value listed gets ranked higher. | Shuffle values; vary which pole is on the left across widgets. |
| **Splitting bias** | Values described in more detail attract more weight. | Show definitions at similar length; keep values at the same level of abstraction. |
| **Automatic rebalancing** | Moving one bar silently moves others, hiding the real choice. | The allocate widget shows a running total that must reach 100 and never rebalances. |
| **Number without reason** | A position with no note is weak evidence. | Every widget asks for a sentence. |
| **Unrealistic dilemmas** | "That would never happen" yields nothing. | Build options from the project's own levers and precedents. |
| **Answering for an audience** | Visible results invite answering as the maintainer thinks others expect. | In teams, each maintainer fills the canvas privately, before any comparison is shown. |
| **Fatigue** | Long canvases degrade later answers. | Three to six widgets per canvas. |
