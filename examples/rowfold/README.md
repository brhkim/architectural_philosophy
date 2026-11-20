# Example: rowfold

rowfold is a **fictional** package: a small, pure-Python library for reading and transforming tabular files
(CSV, TSV and fixed-width) that many downstream projects depend on. It was invented for this demo. Its
maintainers (`maintainer-a` and `maintainer-b`), releases, dates and quotes are illustrative, not a real
project's record.

The folder shows what the skill leaves in a project after a couple of interviews and one amendment, and what
an agent's decision card looks like for two competing proposals.

| File | What it is |
|------|-----------|
| [`philosophy.json`](philosophy.json) | The canonical data: mission, values glossary, three hard limits, five tensions (four two-way, one three-way) with stances, and the amendment history |
| [`PHILOSOPHY.md`](PHILOSOPHY.md) | The readable view generated from the JSON; this is what agents read by default |
| [`philosophy-map.html`](philosophy-map.html) | The interactive map of every tension and stance, with both maintainers' positions kept separate |
| [`proposals/required-c-extension.json`](proposals/required-c-extension.json) and [`.html`](proposals/required-c-extension.html) | A contributor's agent proposes making a C extension mandatory. The review flags a hard limit at risk and asks for a decision |
| [`proposals/optional-fast-parser.json`](proposals/optional-fast-parser.json) and [`.html`](proposals/optional-fast-parser.html) | The same speed-up as an optional `rowfold[fast]` extra with a pure-Python fallback. The review finds it fits the philosophy |
| [`canvas-demo.html`](canvas-demo.html) and [`canvas-spec.json`](canvas-spec.json) | An interview canvas: four questions (a spectrum, a three-way triangle, a dilemma and a definition check) that a maintainer answers in the browser, then copies or downloads the answers |

In a real project the amendment history would also be written out to `AMENDMENTS.md`. Here it lives only in
the `amendment_log` field of `philosophy.json`.

## Opening the pages

The HTML files are single self-contained pages with no network requests. GitHub shows HTML as source, so clone
or download the repository and open the files straight from disk in any browser.

To regenerate the pages from the data with the skill's helper script (Python 3, standard library only), run
this from this folder:

```bash
python3 ../../skills/architectural-philosophy/scripts/render.py philosophy.json \
  --html philosophy-map.html --md PHILOSOPHY.md
python3 ../../skills/architectural-philosophy/scripts/render.py philosophy.json \
  --html proposals/optional-fast-parser.html --proposal proposals/optional-fast-parser.json
```
