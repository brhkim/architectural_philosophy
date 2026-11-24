#!/usr/bin/env python3
"""Render a philosophical-alignment philosophy JSON file to an HTML map and a Markdown view.

Python 3 standard library only. Usage:

    python3 render.py philosophy.json --html OUT.html [--md OUT.md] [--proposal proposal.json]

The HTML is assets/philosophy-map.html with the philosophy (and the optional proposal)
inlined into its JSON script blocks, so the result is one self-contained file that works
opened straight from disk. Both outputs open with the bottom line: the philosophy's
`synthesis`, and with --proposal, the proposal review (its `bluf`, overall verdict and the
decision needed) ahead of everything else. Exit codes: 0 ok, 1 validation error, 2 usage or
I/O error.

Display labels are plain words (hard_limits are "Lines we never cross", tensions are
"Priorities", a stance is "Where we stand", flip_conditions are "Exceptions we'd accept", the
flip_condition_met verdict is "Allowed exception"); the data field names do not change. Files
labelled with the skill's earlier schema name, "architectural-philosophy/0.x", are read exactly
like "philosophical-alignment/0.x" files.
"""
# §§ IMPORTS
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "philosophy-map.html"
KNOWN_KINDS = {"polarity", "triad", "network"}
OVERALL_LABEL = {"consistent": "Fits your priorities", "departs": "Departs from your priorities (explained)",
                 "needs_decision": "Needs your decision"}
# Schema labels this renderer reads. "architectural-philosophy" is the skill's earlier name; files
# written under it are accepted unchanged.
SCHEMA_FAMILIES = ("philosophical-alignment", "architectural-philosophy")
VERDICT_LABEL = {"consistent": "consistent", "departs": "departs", "flip": "allowed exception"}
FIRM_LABEL = {"core": "Core position", "firm": "Firm position", "working": "Working position",
              "exploratory": "Exploratory position", "soft": "Soft position",
              "provisional": "Provisional position", "loose": "Loose position"}
STATUS_LABEL = {"provisional": "not yet confirmed", "agreed": "agreed by everyone",
                "consented": "agreed, with concerns noted", "rough": "decided over an objection",
                "scoped": "differs by area", "contested": "not agreed yet", "superseded": "replaced",
                "retired": "retired"}
ENDORSE_LABEL = {"endorse": "agrees", "consent": "has no objection", "consent with concern": "agrees, with a concern",
                 "stand aside": "stands aside", "in the rough": "still objects; the objection was heard",
                 "object": "objects"}
STRICT_NOTE = {"advisory": "the AI assistant explains and proceeds",
               "flag-and-ask": "the AI assistant stops and asks first",
               "review-gate": "changes wait for written approval"}


def schema_known(label, suffix=""):
    """True when label is missing or belongs to one of SCHEMA_FAMILIES (suffix: "", "-proposal", ...)."""
    if not label:
        return True
    return any(str(label).startswith(f"{fam}{suffix}/") for fam in SCHEMA_FAMILIES)


# §§ VALIDATION
def validate(doc):
    """Return (errors, warnings). Errors stop rendering; warnings are printed."""
    errors, warnings = [], []
    if not isinstance(doc, dict):
        return ["top level must be a JSON object"], warnings
    if not doc.get("project"):
        errors.append("missing 'project' (the project's name)")
    if not schema_known(doc.get("schema")):
        warnings.append(f"schema {doc.get('schema')!r} is not a philosophical-alignment/0.x label; rendering it anyway")
    tensions = doc.get("tensions")
    if not isinstance(tensions, list):
        errors.append("missing 'tensions' list")
        tensions = []
    syn = doc.get("synthesis")
    if not isinstance(syn, dict) or not syn.get("text"):
        warnings.append("no 'synthesis' (bottom line up front): views will say none is written yet")
    elif syn.get("as_of_version") and doc.get("version") and syn["as_of_version"] != doc["version"]:
        warnings.append(f"synthesis is for version {syn['as_of_version']} but the philosophy is {doc['version']}: "
                        "refresh it or confirm it still holds")
    glossary = {v.get("id"): v for v in doc.get("values") or [] if isinstance(v, dict)}
    names = {str(v.get("name", "")).lower() for v in glossary.values()}
    if not glossary:
        warnings.append("no 'values' glossary: every value will show 'no definition yet'")
    for v in glossary.values():
        if not v.get("definition"):
            warnings.append(f"value '{v.get('id')}' has no definition yet")
    seen = set()
    for i, t in enumerate(tensions):
        where = f"tensions[{i}]"
        if not isinstance(t, dict):
            errors.append(f"{where} is not an object")
            continue
        tid = t.get("id")
        if not tid:
            errors.append(f"{where} has no 'id'")
        elif tid in seen:
            errors.append(f"duplicate tension id {tid}")
        seen.add(tid)
        where = f"tension {tid or i}"
        kind = t.get("kind")
        stance = t.get("stance") or {}
        if kind not in KNOWN_KINDS:
            warnings.append(f"{where}: kind {kind!r} has no dedicated view; shown as plain fields")
        if kind == "polarity":
            poles = t.get("poles") or []
            if len(poles) != 2:
                errors.append(f"{where}: polarity needs exactly 2 poles, found {len(poles)}")
            pos = stance.get("position")
            if pos is not None and not (isinstance(pos, (int, float)) and -1 <= pos <= 1):
                errors.append(f"{where}: stance.position must be a number from -1 to 1")
        elif kind == "triad":
            vals = t.get("values") or []
            if len(vals) != 3:
                errors.append(f"{where}: triad needs exactly 3 values, found {len(vals)}")
            w = stance.get("weights")
            if isinstance(w, dict) and w:
                total = sum(x for x in w.values() if isinstance(x, (int, float)))
                if abs(total - 1) > 0.02:
                    warnings.append(f"{where}: stance.weights sum to {total:.2f}, not 1 (shown normalized)")
        elif kind == "network":
            vals = [value_name(v) for v in t.get("values") or []]
            for e in t.get("edges") or []:
                for end in (e.get("a"), e.get("b")):
                    if end not in vals:
                        warnings.append(f"{where}: edge end {end!r} is not one of its values")
        for v, ref in value_refs(t):
            if ref and ref not in glossary:
                warnings.append(f"{where}: ref {ref!r} is not in the values glossary")
            elif not ref and str(v).lower() not in names:
                warnings.append(f"{where}: value {v!r} has no glossary entry (no definition yet)")
    for h in doc.get("hard_limits") or []:
        if not isinstance(h, dict) or not h.get("id") or not h.get("text"):
            errors.append(f"hard limit {h!r} needs 'id' and 'text'")
    return errors, warnings


def validate_proposal(prop, doc):
    errors, warnings = [], []
    if not isinstance(prop, dict) or not isinstance(prop.get("touched"), list):
        return ["proposal must be an object with a 'touched' list"], warnings
    ids = {t.get("id") for t in doc.get("tensions") or [] if isinstance(t, dict)}
    if not prop.get("bluf"):
        warnings.append("proposal has no 'bluf' (bottom line up front); its summary is shown instead")
    if not schema_known(prop.get("schema"), "-proposal"):
        warnings.append(f"proposal schema {prop.get('schema')!r} is not a philosophical-alignment-proposal/0.x label")
    if prop.get("overall") is not None and prop.get("overall") not in OVERALL_LABEL:
        warnings.append(f"proposal 'overall' should be one of {', '.join(OVERALL_LABEL)}; found {prop.get('overall')!r}")
    for t in prop["touched"]:
        if t.get("id") not in ids:
            warnings.append(f"proposal touches unknown tension {t.get('id')!r}")
        v = re.sub(r"[^a-z]", "", str(t.get("verdict", "")).lower())
        if not (v.startswith("consist") or v.startswith("depart") or v.startswith("flip")):
            warnings.append(f"proposal verdict for {t.get('id')} should be consistent, departs or flip_condition_met")
    return errors, warnings


# §§ HELPERS
def value_name(v):
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get("value") or v.get("name") or v.get("label") or "?"
    return str(v)


def value_refs(t):
    """Yield (name, ref) for every value a tension uses."""
    if t.get("kind") == "polarity":
        for p in t.get("poles") or []:
            yield value_name(p), (p.get("ref") if isinstance(p, dict) else None)
    else:
        refs = t.get("refs") or []
        for i, v in enumerate(t.get("values") or []):
            ref = v.get("ref") if isinstance(v, dict) else None
            yield value_name(v), ref or (refs[i] if i < len(refs) else None)


def plain(label_map, key):
    """Plain display wording for a data keyword; unknown keywords pass through unchanged."""
    k = re.sub(r"[_-]+", " ", str(key or "")).strip().lower()
    return label_map.get(k) or label_map.get(str(key or "").lower()) or str(key or "")


def display_name(handle, doc=None):
    """A person as shown to readers: maintainers[].name when given, else the handle, capitalised."""
    for m in (doc or {}).get("maintainers") or []:
        if isinstance(m, dict) and m.get("handle") == handle and m.get("name"):
            return str(m["name"])
    return " ".join(p[:1].upper() + p[1:] for p in re.split(r"[-_.\s]+", str(handle or "?")) if p)


def as_list(x):
    """Examples may be one string or a list of strings (bug fix: lists printed as Python syntax)."""
    if x is None or x == "":
        return []
    return [str(e) for e in x] if isinstance(x, list) else [str(x)]


def script_json(obj):
    """JSON safe to place inside <script type="application/json">."""
    text = json.dumps(obj, ensure_ascii=False, indent=1)
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def inline_block(html, block_id, payload):
    pattern = re.compile(
        r'^(<script type="application/json" id="' + re.escape(block_id) + r'">)(.*?)(</script>)', re.S | re.M)
    if not pattern.search(html):
        raise ValueError(f"template has no {block_id} block")
    return pattern.sub(lambda m: m.group(1) + payload + m.group(3), html, count=1)


# §§ MARKDOWN
def md_escape(s):
    return str(s or "").replace("\n", " ").strip()


def strictness_level(st):
    if isinstance(st, str):
        return st
    if isinstance(st, dict):
        return st.get("level") or "advisory"
    return "advisory"


def strictness_lines(st):
    """Readable strictness: the default level, then any raised levels as a short list."""
    if not st:
        return []
    lvl0 = strictness_level(st)
    note = f" ({STRICT_NOTE[lvl0]})" if lvl0 in STRICT_NOTE else ""
    out = [f"**Strictness:** {lvl0} by default{note}."]
    if isinstance(st, dict):
        extra = []
        for firm, lvl in (st.get("by_firmness") or {}).items():
            extra.append(f"- {firm} positions: {lvl}")
        for tid, lvl in (st.get("by_tension") or {}).items():
            extra.append(f"- {tid}: {lvl}")
        for k, v in st.items():
            if k not in ("level", "by_firmness", "by_tension", "set_by", "date", "note") and v not in (None, "", {}, []):
                extra.append(f"- {k.replace('_', ' ')}: {v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}")
        if extra:
            out += ["Raised for:", ""] + extra
        if st.get("note"):
            out += ["", md_escape(st["note"])]
        if st.get("set_by") or st.get("date"):
            out += ["", f"*Set by {st.get('set_by', 'unknown')}{', ' + st['date'] if st.get('date') else ''}.*"]
    return out + [""]


def fmt_pos(p):
    return f"{p:+.2f}" if isinstance(p, (int, float)) else "n/a"


def lean_phrase(p, a, b):
    if not isinstance(p, (int, float)):
        return "no position recorded"
    m = abs(p)
    if m < 0.15:
        return f"balanced between {a} and {b}"
    word = "leans toward" if m < 0.45 else "favors" if m < 0.75 else "strongly favors"
    return f"{word} {a if p < 0 else b}"


def verdict_key(v):
    k = re.sub(r"[^a-z]", "", str(v or "").lower())
    return "consistent" if k.startswith("consist") else "departs" if k.startswith("depart") else \
        "flip" if k.startswith("flip") else ("other" if k else "")


def strict_for(doc, t):
    st = doc.get("strictness")
    if not st:
        return "advisory"
    if isinstance(st, str):
        return st
    firm = (t.get("stance") or {}).get("firmness")
    return ((st.get("by_tension") or {}).get(t.get("id")) or (st.get("by_firmness") or {}).get(firm)
            or st.get("level") or "advisory")


def overall_of(prop, doc):
    """(key, computed): the proposal's own 'overall', else the documented rules."""
    if prop.get("overall") in OVERALL_LABEL:
        return prop["overall"], False
    by_id = {t.get("id"): t for t in doc.get("tensions") or [] if isinstance(t, dict)}
    risk = bool(prop.get("hard_limits_at_risk"))
    contested = gated = departs = False
    for p in prop.get("touched") or []:
        t = by_id.get(p.get("id")) or {}
        if str(t.get("status", "")).lower() == "contested":
            contested = True
        if verdict_key(p.get("verdict")) == "departs":
            departs = True
            if strict_for(doc, t) != "advisory":
                gated = True
    return ("needs_decision" if risk or contested or gated else "departs" if departs else "consistent"), True


def proposal_markdown(prop, doc):
    """The proposal review, written first when a proposal is given."""
    key, computed = overall_of(prop, doc)
    out = [f"## Proposal review: {md_escape(prop.get('title') or 'Untitled proposal')}", ""]
    out += [f"**Overall: {OVERALL_LABEL[key]}.**" + (" *(Worked out from the verdicts below.)*" if computed else ""), ""]
    out += [f"**Bottom line.** {md_escape(prop.get('bluf') or prop.get('summary') or 'No bottom line written yet.')}", ""]
    if prop.get("decision_needed"):
        out += [f"> **Decision needed:** {md_escape(prop['decision_needed'])}", ""]
    if prop.get("philosophy_version") and doc.get("version") and prop["philosophy_version"] != doc["version"]:
        out += [f"*Checked against version {prop['philosophy_version']}; the philosophy is now version {doc['version']}.*", ""]
    limits = {h.get("id"): h for h in doc.get("hard_limits") or [] if isinstance(h, dict)}
    risks = [h if isinstance(h, dict) else {"id": h} for h in prop.get("hard_limits_at_risk") or []]
    if risks:
        out += ["**Lines we never cross that are at risk:**" if len(risks) > 1 else "**A line we never cross is at risk:**", ""]
        for r in risks:
            text = md_escape((limits.get(r.get("id")) or {}).get("text"))
            out.append(f"- **{r.get('id')}** {text}" + (f" *At risk because:* {md_escape(r['reason'])}" if r.get("reason") else ""))
        out.append("")
    by_id = {t.get("id"): t for t in doc.get("tensions") or [] if isinstance(t, dict)}
    if prop.get("touched"):
        out += ["**Priorities this change touches:**", ""]
        for p in prop["touched"]:
            t = by_id.get(p.get("id")) or {}
            verdict = VERDICT_LABEL.get(verdict_key(p.get("verdict")), p.get("verdict") or "no verdict")
            line = f"- **{md_escape(t.get('name') or p.get('id'))}** (`{p.get('id')}`): {verdict.capitalize()}. {md_escape(p.get('reason'))}"
            if p.get("flip_condition"):
                line += f" *Exception cited:* \u201c{md_escape(p['flip_condition'])}\u201d"
            out.append(line)
        out.append("")
    if prop.get("bluf") and prop.get("summary"):
        out += [f"*As submitted:* {md_escape(prop['summary'])}", ""]
    out += ["---", ""]
    return out


def to_markdown(doc, prop=None):
    gl = {v.get("id"): v for v in doc.get("values") or [] if isinstance(v, dict) and v.get("id")}
    by_name = {str(v.get("name", "")).lower(): v for v in gl.values()}

    def entry(name, ref):
        return gl.get(ref) if ref else by_name.get(str(name).lower())

    def term(name, ref=None):
        g = entry(name, ref)
        if not g:
            return f"{name} *(no definition yet)*"
        return f"[{name}](#value-{g['id']})"

    def define(name, ref=None):
        g = entry(name, ref)
        if not g:
            return f"{name}: *no definition yet.*"
        return f"`{g['id']}@{g.get('rev', 1)}` {md_escape(g.get('definition')) or '*(definition missing)*'}"

    out = [f"# {md_escape(doc.get('project'))}: philosophy", ""]
    if prop:
        out += proposal_markdown(prop, doc)
    out += ["## Philosophy bottom line" if prop else "## Bottom line", ""]
    syn = doc.get("synthesis") if isinstance(doc.get("synthesis"), dict) else {}
    if syn.get("text"):
        out += [md_escape(syn["text"]), ""]
        if syn.get("as_of_version") and doc.get("version") and syn["as_of_version"] != doc["version"]:
            out += [f"*Written for version {syn['as_of_version']}; the philosophy is now version {doc['version']}, "
                    "so this summary may be out of date.*", ""]
    else:
        out += ["*No synthesis yet. Your AI assistant drafts one after the first interview, and the maintainers confirm it.*", ""]
    meta = []
    if doc.get("version"):
        meta.append(f"Version {doc['version']}")
    if doc.get("schema"):
        meta.append(f"schema `{doc['schema']}`")
    if doc.get("strictness"):
        meta.append(f"strictness: {strictness_level(doc['strictness'])}")
    if not schema_known(doc.get("schema")):
        meta.append("*(schema label not recognised; shown as best it can be)*")
    if meta:
        out += [" · ".join(meta), ""]
    if doc.get("status_note"):
        out += [f"> **Status:** {md_escape(doc['status_note'])}", ""]
    out += strictness_lines(doc.get("strictness"))
    if doc.get("mission"):
        out += [f"**Mission.** {md_escape(doc['mission'])}", ""]
    if doc.get("maintainers"):
        out.append("**Maintainers.** " + "; ".join(
            f"{display_name(m.get('handle'), doc) if isinstance(m, dict) else display_name(m)}"
            + (f" ({m['role']})" if isinstance(m, dict) and m.get("role") else "")
            for m in doc["maintainers"]))
        out.append("")

    out += ["## Lines we never cross", "", "Never traded against anything. Crossing one needs a change to the philosophy itself.", ""]
    for h in doc.get("hard_limits") or []:
        src = f" *(Source: {md_escape(h.get('source'))})*" if h.get("source") else ""
        out.append(f"- **{h.get('id')}**: {md_escape(h.get('text'))}{src}")
    out.append("")

    out += ["## Glossary", "", "What each value means in this project. The priorities below link here.", ""]
    if not gl:
        out += ["*No values glossary yet.*", ""]
    for g in gl.values():
        out += [f'<a id="value-{g["id"]}"></a>', f"### {md_escape(g.get('name') or g['id'])} (`{g['id']}@{g.get('rev', 1)}`)", ""]
        out.append(md_escape(g.get("definition")) or "*No definition yet.*")
        out.append("")
        if g.get("looks_like"):
            out.append("- **Looks like:** " + "; ".join(md_escape(x) for x in g["looks_like"]))
        if g.get("too_little"):
            out.append(f"- **Too little looks like:** {md_escape(g['too_little'])}")
        if g.get("not_to_be_confused_with"):
            out.append(f"- **Not to be confused with:** {md_escape(g['not_to_be_confused_with'])}")
        out.append("- **In the maintainer's own words:** " + (
            f"\"{md_escape(g['in_own_words'])}\"" if g.get("in_own_words") else "*not yet captured*"))
        ex = g.get("examples") or {}
        if as_list(ex.get("good")):
            out.append("- **Done well:** " + "; ".join(md_escape(x) for x in as_list(ex.get("good"))))
        if as_list(ex.get("missing_or_faked")):
            out.append("- **Missing or faked:** " + "; ".join(md_escape(x) for x in as_list(ex.get("missing_or_faked"))))
        out.append("")

    # bug 3: glossary_terms (other terms the philosophy relies on) were never rendered
    terms = [g for g in doc.get("glossary_terms") or [] if isinstance(g, dict) and (g.get("id") or g.get("name"))]
    if terms:
        out += ["### Other terms", "", "Words the philosophy relies on that are not values, and what they mean here.", ""]
        for g in terms:
            tid = g.get("id") or re.sub(r"[^a-z0-9]+", "-", str(g.get("name")).lower())
            out.append(f'- <a id="term-{tid}"></a>**{md_escape(g.get("name") or tid)}** (`{tid}@{g.get("rev", 1)}`): '
                       f'{md_escape(g.get("definition")) or "*no definition yet*"}')
        out.append("")

    out += ["## Priorities", "", "Each one names two or more good things that pull against each other, and where this project stands.", ""]
    for t in doc.get("tensions") or []:
        st = t.get("stance") or {}
        rev = f"@{t['rev']}" if t.get("rev") is not None else ""
        out += [f"### {md_escape(t.get('name') or t.get('slug') or t.get('id'))} (`{t.get('id')}{rev}`)", ""]
        facts = []
        if st.get("firmness"):
            facts.append(FIRM_LABEL.get(st["firmness"], f"{st['firmness']} position"))
        if t.get("status"):
            facts.append(plain(STATUS_LABEL, t["status"]))
        if facts:
            out += [" · ".join(facts), ""]
        kind = t.get("kind")
        if kind == "polarity":
            poles = t.get("poles") or [{}, {}]
            names = [value_name(p) for p in poles]
            out.append(f"**Between:** {term(names[0], poles[0].get('ref'))} (−1) ↔ {term(names[1], poles[1].get('ref'))} (+1)")
            out.append("")
            for p in poles:
                n = value_name(p)
                out.append(f"- **{term(n, p.get('ref'))}**: {define(n, p.get('ref'))}")
                if p.get("good"):
                    out.append(f"  - Good: {md_escape(p['good'])}")
                if p.get("overdone"):
                    out.append(f"  - Overdone: {md_escape(p['overdone'])}")
            pos = st.get("position")
            out += ["", f"**Where we stand:** {lean_phrase(pos, names[0], names[-1])} ({fmt_pos(pos)})."]
        elif kind in ("triad", "network"):
            pairs = list(value_refs(t))
            out.append("**Values:**")
            out.append("")
            vals = t.get("values") or []
            for i, (n, ref) in enumerate(pairs):
                good = vals[i].get("good") if isinstance(vals[i], dict) else None
                out.append(f"- **{term(n, ref)}**: {define(n, ref)}" + (f" Good: {md_escape(good)}" if good else ""))
            out.append("")
            refmap = dict(pairs)
            if kind == "triad" and isinstance(st.get("weights"), dict):
                out.append("**Where we stand:** " + ", ".join(
                    f"{term(k, refmap.get(k))} {round(v * 100)}%" for k, v in st["weights"].items()) + ".")
            if kind == "network":
                if st.get("priority"):
                    out.append("**Where we stand (in order):** " + " > ".join(term(v, refmap.get(v)) for v in st["priority"]) + ".")
                for e in t.get("edges") or []:
                    out.append(f"- {term(e.get('a'), refmap.get(e.get('a')))} ↔ {term(e.get('b'), refmap.get(e.get('b')))}: {md_escape(e.get('note'))}")
        else:
            out.append(f"*Kind {kind!r} shown as raw data:* `{json.dumps({k: v for k, v in t.items() if k not in ('id', 'rev', 'name', 'stance')}, ensure_ascii=False)[:400]}`")
        if st.get("summary"):
            out += ["", f"> {md_escape(st['summary'])}"]
        out += ["", "**Exceptions we'd accept:**"]
        flips = t.get("flip_conditions") or []
        out += [f"- {md_escape(f if isinstance(f, str) else f.get('text', f))}" for f in flips] or ["- None recorded."]
        if t.get("precedents"):
            out += ["", "**Precedents:**"]
            for p in t["precedents"]:
                if isinstance(p, str):
                    out.append(f"- {md_escape(p)}")
                else:
                    href = p.get("link") or p.get("url")  # "link" is the schema field; "url" is read too
                    title = f"[{p.get('title') or href}]({href})" if href else p.get("title", "")
                    out.append(f"- **{title}**" + (f": {md_escape(p.get('note'))}" if p.get("note") else ""))
        if t.get("positions"):
            out += ["", "**Maintainer positions** (kept separate, never averaged):"]
            for m in t["positions"]:
                bits = []
                if "position" in m:
                    if kind == "polarity":
                        bits.append(f"{lean_phrase(m['position'], names[0], names[-1])} ({fmt_pos(m['position'])})")
                    else:
                        bits.append(f"position {fmt_pos(m['position'])}")
                if isinstance(m.get("weights"), dict):
                    bits.append(", ".join(f"{k} {round(v * 100)}%" for k, v in m["weights"].items()))
                if m.get("priority"):
                    bits.append(" > ".join(m["priority"]))
                if m.get("endorsement"):
                    bits.append(plain(ENDORSE_LABEL, m["endorsement"]))
                line = f"- **{display_name(m.get('holder'), doc)}**: " + "; ".join(bits)
                if m.get("note"):
                    line += f". {md_escape(m['note'])}"
                out.append(line)
        if t.get("amendments"):
            out += ["", "**Revisions:**"]
            for a in t["amendments"]:
                out.append(f"- {t.get('id')}@{a.get('rev')} ({a.get('date', '')}): {md_escape(a.get('summary'))}")
        out.append("")

    out += ["## Update history", ""]
    log = doc.get("amendment_log") or []
    out += [f"- **{a.get('version') or a.get('id', '')}** ({a.get('date', '')}): {md_escape(a.get('summary'))}" for a in log] or ["*Empty.*"]
    out.append("")
    return "\n".join(out)


# §§ MAIN
def load_json(path, label):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: {label} file not found: {path}")
    except json.JSONDecodeError as e:
        sys.exit(f"error: {label} is not valid JSON ({path}, line {e.lineno}, column {e.colno}): {e.msg}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render a philosophy JSON to an interactive HTML map and Markdown.")
    ap.add_argument("philosophy", help="path to the philosophy JSON")
    ap.add_argument("--html", help="write the interactive HTML map here")
    ap.add_argument("--md", help="write the Markdown view here")
    ap.add_argument("--proposal", help="proposal JSON: the HTML map becomes a proposal review, and the Markdown opens with it")
    ap.add_argument("--template", default=str(TEMPLATE), help="map template (default: assets/philosophy-map.html)")
    args = ap.parse_args(argv)
    if not args.html and not args.md:
        ap.error("give --html and/or --md")

    doc = load_json(args.philosophy, "philosophy")
    errors, warnings = validate(doc)
    prop = None
    if args.proposal:
        prop = load_json(args.proposal, "proposal")
        e2, w2 = validate_proposal(prop, doc if isinstance(doc, dict) else {})
        errors += e2
        warnings += w2
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    if args.html:
        try:
            html = Path(args.template).read_text(encoding="utf-8")
            html = inline_block(html, "philosophy-data", script_json(doc))
            html = inline_block(html, "proposal-data", script_json(prop) if prop else "null")
            title = f"{doc.get('project', 'Project')} philosophy"
            html = re.sub(r"<title>.*?</title>", lambda m: "<title>" + title.replace("&", "&amp;").replace("<", "&lt;") + "</title>", html, count=1)
            Path(args.html).write_text(html, encoding="utf-8")
        except (OSError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        print(f"HTML: {args.html}")
    if args.md:
        Path(args.md).write_text(to_markdown(doc, prop), encoding="utf-8")
        print(f"MD: {args.md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
