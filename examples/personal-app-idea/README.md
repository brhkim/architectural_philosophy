# Example: Personal App Idea

Personal App Idea is a **fictional** project: a simple personal budgeting app that keeps your money data on your
device. It was invented for this demo. Its maintainers (Maya and Sam), releases, dates and quotes are
illustrative, not a real app's record.

The folder shows what the skill leaves in a project after two interviews and one amendment, and how an AI
assistant's decision card reads for three proposals: one that fits the project's priorities, one that would
cross the line it never crosses, and one that departs from where it stands.

| File | What it is |
|------|-----------|
| [`philosophy.json`](philosophy.json) | The canonical data: mission, values glossary, other terms, one line the app never crosses, three competing priorities with where the project stands on each, and the amendment history |
| [`PHILOSOPHY.md`](PHILOSOPHY.md) | The readable view generated from the JSON; this is what AI assistants read by default |
| [`philosophy-map.html`](philosophy-map.html) | The interactive page: every priority, where the project stands, and Maya's and Sam's positions kept separate |
| [`proposals/encrypted-sync.json`](proposals/encrypted-sync.json) and [`.html`](proposals/encrypted-sync.html) | Automatic bank sync that is opt-in and end-to-end encrypted, with manual entry kept as the default. The review finds it fits the project's priorities, as an exception the project already accepts |
| [`proposals/server-sync.json`](proposals/server-sync.json) and [`.html`](proposals/server-sync.html) | Bank sync that stores transactions unencrypted on the app's server. The review flags the line the app never crosses and asks for a decision |
| [`proposals/forecast-charts.json`](proposals/forecast-charts.json) and [`.html`](proposals/forecast-charts.html) | Spending forecast charts placed on the home screen for everyone. The review finds they depart from "simple by default" and suggests the opt-in Advanced view |
| [`canvas-demo.html`](canvas-demo.html) and [`canvas-spec.json`](canvas-spec.json) | An interview canvas: three questions (a spectrum, a definition check and a dilemma) that a person answers in the browser, then copies or downloads the answers |

In a real project the amendment history would also be written out to `AMENDMENTS.md`. Here it lives only in
the `amendment_log` field of `philosophy.json`.

## Opening the pages

The HTML files are single self-contained pages with no network requests. GitHub shows HTML as source, so clone
or download the repository and open the files straight from disk in any browser.

To regenerate the pages from the data with the skill's helper script (Python 3, standard library only), run
this from this folder:

```bash
python3 ../../skills/philosophical-alignment/scripts/render.py philosophy.json \
  --html philosophy-map.html --md PHILOSOPHY.md
python3 ../../skills/philosophical-alignment/scripts/render.py philosophy.json \
  --html proposals/encrypted-sync.html --proposal proposals/encrypted-sync.json
```
