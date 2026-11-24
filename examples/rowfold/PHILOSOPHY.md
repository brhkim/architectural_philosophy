# rowfold (example package): philosophy

## Bottom line

Example package: rowfold is a library other projects build on, so it protects the people downstream first: installing it never needs a compiler, and nothing is removed without a deprecation period. Correct results come before speed and before convenience; when rowfold cannot be sure what a file means, it says so instead of guessing. Portability comes before raw speed, and compiled code is welcome only as an optional extra that gives the same results as the pure-Python path. The core stays small, and integrations with other tools live in plugins. When an old API is unclear, the project keeps it working and adds a clearer one beside it, saving clean breaks for major releases with a migration guide.

Version 1.1.1 · schema `philosophical-alignment/0.1-draft` · strictness: advisory

> **Status:** EXAMPLE PACKAGE. rowfold is fictional, invented for the Philosophical Alignment demo on 2026-11-20 (the name was unregistered on PyPI that day). Its maintainers, releases, dates and quotes are illustrative, not a real project's record.

**Strictness:** advisory by default (the AI assistant explains and proceeds).
Raised for:

- core positions: flag-and-ask

Advisory overall; a departure from a core stance stops and asks.

**Mission.** Example package: rowfold is a small, pure-Python library for reading and transforming tabular files (CSV, TSV and fixed-width), and many downstream projects depend on it.

**Maintainers.** Maintainer A (lead maintainer (fictional)); Maintainer B (co-maintainer, owns the parser (fictional))

## Lines we never cross

Never traded against anything. Crossing one needs a change to the philosophy itself.

- **H1**: pip install works everywhere we support, with no compiler required: installing rowfold succeeds on every supported Python version and platform from a pure-Python wheel. *(Source: Example: the project README's install promise)*
- **H2**: No breaking change to the public API without a deprecation period: the old behaviour keeps working, with a warning, for at least two minor releases before it is removed. *(Source: Example: the project's versioning policy)*
- **H3**: The public API stays fully typed: every public function, class and argument ships with type annotations that pass a strict type checker. *(Source: Example: the project's contributing guide)*

## Glossary

What each value means in this project. The priorities below link here.

<a id="value-compatibility"></a>
### Compatibility (`compatibility@1`)

The degree to which code written against an earlier rowfold release keeps working, unchanged, on the latest one.

- **Looks like:** Old arguments still accepted, with a DeprecationWarning; Downstream test suites pass after an upgrade; Changelog entries that say 'no action needed'
- **Too little looks like:** Downstream projects pin old versions and stop upgrading.
- **Not to be confused with:** Not stability of internals: private modules may change freely. Not Portability, which is about where rowfold runs, not which code still runs.
- **In the maintainer's own words:** "If someone wrote rowfold.read(path, ',') in 2023 and never touched it again, it should still work, or it should have warned them loudly for a long time first. We're a dependency, not an app."
- **Done well:** The 2.0 keyword-only signature shipped beside the positional one
- **Missing or faked:** A 'minor' release that renamed a return column and broke three plugins

<a id="value-clarity"></a>
### Clarity (`clarity@1`)

How easily a reader can predict what an API call does from its name, arguments and type hints alone.

- **Looks like:** Keyword-only arguments with descriptive names; One obvious way to do each task; No arguments whose meaning depends on another argument
- **Too little looks like:** Users read the source to find out what skip=3 skips.
- **Not to be confused with:** Not Approachability, which is about a newcomer's first success; a clear API can still take some learning. Not brevity.
- **In the maintainer's own words:** "Clear means you can read a call in someone else's code review and know what it does without opening our docs."
- **Done well:** read(path, *, schema=...) replacing a positional types argument
- **Missing or faked:** A mode string argument with seven undocumented values

<a id="value-portability"></a>
### Portability (`portability@1`)

The range of Python versions, operating systems, CPU architectures and runtimes on which rowfold installs and gives the same results without extra tools.

- **Looks like:** Pure-Python wheel tagged py3-none-any; CI on Linux, macOS, Windows, musl and Pyodide; Works on a new Python release the day it ships
- **Too little looks like:** Install failures on platforms without a prebuilt wheel; 'please install a C compiler' issues.
- **Not to be confused with:** Not Compatibility (which old code still runs). Not a ban on compiled code: optional extras do not reduce portability while the pure-Python path stays complete.
- **In the maintainer's own words:** "The test is a fresh Raspberry Pi or a browser tab running Pyodide. If pip install rowfold works there and gives the same answers, we're portable."
- **Done well:** Day-one support for a new CPython release with no rebuild
- **Missing or faked:** 'Supports all platforms' on the README while the Alpine wheel is missing

<a id="value-performance"></a>
### Performance (`performance@1`)

How quickly, and within how little memory, rowfold reads and transforms large files on a single machine.

- **Looks like:** Rows per second on the benchmark corpus; Peak memory on a 1 GB file; Streaming reads that never load the whole file
- **Too little looks like:** Users with large files switch libraries or write their own parser.
- **Not to be confused with:** Not Correctness: a fast wrong answer is not performance. Not Approachability: a fast API can still be hard to use.
- **In the maintainer's own words:** "Performance is the 2 GB log file someone actually has. Microbenchmarks on ten rows don't count."
- **Done well:** Streaming read_chunks() that kept memory flat on multi-gigabyte files
- **Missing or faked:** A benchmark chart that only measured files that fit in the CPU cache

<a id="value-small-core"></a>
### Small core (`small-core@1`)

How few features, dependencies and lines of code the core rowfold package carries.

- **Looks like:** Zero runtime dependencies beyond the standard library; New formats arrive as plugins; Issues closed with 'this belongs in a plugin'
- **Too little looks like:** The core gains dependencies that every downstream project must install and audit.
- **Not to be confused with:** Not minimal usefulness: the core still does its one job completely. Not Clarity.
- **In the maintainer's own words:** "Two of us maintain this. Everything in the core is something we promise to keep correct forever, so the core holds only what we can keep that promise for."
- **Done well:** Excel support shipped as rowfold-excel
- **Missing or faked:** A 'tiny' helper that pulled in a 40 MB dependency

<a id="value-batteries-included"></a>
### Batteries included (`batteries-included@1`)

How many common tabular jobs a user can do with the core install alone, without finding and installing anything else.

- **Looks like:** Built-in readers for the formats users ask about most; Recipes in the docs that need no extra install
- **Too little looks like:** Every user hunts for plugins and writes the same glue code.
- **Not to be confused with:** Not Approachability, which is about how easy a feature is to use once present; this is whether it is present at all.
- **In the maintainer's own words:** "The person who just wants to turn a TSV into JSON on a locked-down work laptop shouldn't need three packages."
- **Done well:** JSON Lines output in the core, since it needs only the standard library
- **Missing or faked:** A 'built-in' feature that fails with ImportError until you install an extra

<a id="value-approachability"></a>
### Approachability (`approachability@1`)

How quickly someone new to rowfold gets a correct first result from the documentation, without help.

- **Looks like:** The first docs example works unchanged; Error messages that say what to type next; Defaults that fit the common case
- **Too little looks like:** New users give up at the first error and pick another library.
- **Not to be confused with:** Not Convenience (guessing on the user's behalf) and not Clarity (predictability for an experienced reader).
- **In the maintainer's own words:** "Approachable means a grad student with a CSV and fifteen minutes gets the right table, and if something is wrong, the error tells them exactly what to change."
- **Done well:** The date error that prints the two possible readings and the argument to choose one
- **Missing or faked:** A quickstart that only works on the bundled sample file

<a id="value-correctness"></a>
### Correctness (`correctness@1`)

The degree to which every table rowfold returns matches what the file actually holds, or rowfold raises a clear error instead of returning a guess.

- **Looks like:** Round-trip tests on a corpus of real, messy files; Errors on ambiguous input instead of silent choices; Property-based tests on the parser
- **Too little looks like:** Silent data corruption: shifted columns, dropped rows, misread dates.
- **Not to be confused with:** Not test coverage: many tests can check the wrong thing. Not Explicitness, though explicit arguments help. Not Performance: a faster path must be exactly as correct.
- **In the maintainer's own words:** "Correct means I'd bet a downstream researcher's paper on the table. If we're not sure what a cell means, we stop and say so; we never return a plausible guess."
- **Done well:** The ambiguous-date error added in v2.1
- **Missing or faked:** A 95% coverage badge on a parser that still drops the last row without a trailing newline

<a id="value-explicitness"></a>
### Explicitness (`explicitness@1`)

The degree to which every choice rowfold makes about a file (encoding, delimiter, types) is either stated by the caller or reported back to them.

- **Looks like:** Full type hints on the public API; Guesses returned in a report object; No behaviour that depends on global state
- **Too little looks like:** The same call gives different tables on two machines and nobody can tell why.
- **Not to be confused with:** Not verbosity: a short call can be explicit if its defaults are documented and fixed. Not Clarity, which is about naming.
- **In the maintainer's own words:** "I don't mind defaults. I mind defaults that change based on what's in the file and don't tell you."
- **Done well:** peek() printing 'guessed delimiter: tab'
- **Missing or faked:** A locale-dependent number parser enabled by default

<a id="value-convenience"></a>
### Convenience (`convenience@1`)

How few arguments and steps the common case takes, because rowfold infers sensible settings for the user.

- **Looks like:** One-line reads for ordinary files; Delimiter and header detection on request
- **Too little looks like:** Ordinary jobs need a page of boilerplate.
- **Not to be confused with:** Not Approachability, which can also come from good errors and docs. Not silent guessing: convenience here always reports what it inferred.
- **In the maintainer's own words:** "Most files are boring. If the file is a plain comma CSV with a header, the user shouldn't have to tell us that."
- **Done well:** rowfold.peek('data.csv') for a first look
- **Missing or faked:** Auto-detection that worked on every demo and failed on the first semicolon-separated file

### Other terms

Words the philosophy relies on that are not values, and what they mean here.

- <a id="term-public-api"></a>**public API** (`public-api@1`): Every name importable from rowfold without a leading underscore, plus the documented arguments and return types of those names.
- <a id="term-identical-results"></a>**identical results** (`identical-results@1`): Byte-for-byte equal output tables, including column types, missing-value markers and error messages, on the project's full test corpus of files.

## Priorities

Each one names two or more good things that pull against each other, and where this project stands.

### Backward compatibility vs. API clarity (`T01@1`)

Core position · agreed, with concerns noted

**Between:** [Compatibility](#value-compatibility) (−1) ↔ [Clarity](#value-clarity) (+1)

- **[Compatibility](#value-compatibility)**: `compatibility@1` The degree to which code written against an earlier rowfold release keeps working, unchanged, on the latest one.
  - Good: Downstream code keeps working after every upgrade, so thousands of projects can update without reading release notes.
  - Overdone: Confusing old names and arguments live forever; every new user pays for a mistake made years ago.
- **[Clarity](#value-clarity)**: `clarity@1` How easily a reader can predict what an API call does from its name, arguments and type hints alone.
  - Good: The API reads the way it works; one obvious way to do each thing.
  - Overdone: Constant renames; downstream maintainers spend their weekends chasing the library.

**Where we stand:** favors Compatibility (-0.60).

> Compatibility over clarity. A clearer API is added beside the old one, and the old one leaves only through deprecation.

**Exceptions we'd accept:**
- A major release may remove an unclear API for clarity's sake when it ships with a published migration guide.

**Precedents:**
- **v2.0 kept the old read() signature for two releases**: The clearer keyword-only read(path, *, schema=...) shipped beside the old positional form, which warned through 2.1 and 2.2 and was removed in 3.0 with a migration guide.

**Maintainer positions** (kept separate, never averaged):
- **Maintainer A**: favors Compatibility (-0.60); agrees
- **Maintainer B**: balanced between Compatibility and Clarity (-0.10); agrees, with a concern. Example: keeping old signatures around slows down new contributors and makes the docs harder to follow.

### Portability vs. raw speed (`T02@2`)

Firm position · agreed by everyone

**Between:** [Portability](#value-portability) (−1) ↔ [Performance](#value-performance) (+1)

- **[Portability](#value-portability)**: `portability@1` The range of Python versions, operating systems, CPU architectures and runtimes on which rowfold installs and gives the same results without extra tools.
  - Good: Runs anywhere Python runs: new Python releases on day one, Alpine, Pyodide, unusual CPUs, locked-down machines.
  - Overdone: Users with large files leave for faster libraries, and the project refuses help that would cost nothing to anyone else.
- **[Performance](#value-performance)**: `performance@1` How quickly, and within how little memory, rowfold reads and transforms large files on a single machine.
  - Good: Large files parse in seconds, not minutes, so rowfold stays usable as data grows.
  - Overdone: A build matrix nobody can maintain, and installs that fail on the platforms the project promised to support.

**Where we stand:** favors Portability (-0.50).

> Portability first: the pure-Python parser is the reference. Compiled extras are welcome when optional.

**Exceptions we'd accept:**
- Compiled code is welcome as an optional extra with a pure-Python fallback that gives identical results.

**Precedents:**
- **Optional [zstd] compression extra (v2.3)**: Zstandard support came through a compiled library as an opt-in extra; gzip and bz2 from the standard library keep working without it.

**Revisions:**
- T02@2 (2026-09-14): After three optional compiled extras shipped without problems, the flip condition was promoted into the stance: compiled extras are welcome when optional. Before: "Pure Python only; speed comes from better algorithms." After: "Portability first: the pure-Python parser is the reference. Compiled extras are welcome when optional."

### Small core vs. batteries included (`T03@1`)

Firm position · agreed by everyone

**Between:** [Small core](#value-small-core) (−1) ↔ [Batteries included](#value-batteries-included) (+1)

- **[Small core](#value-small-core)**: `small-core@1` How few features, dependencies and lines of code the core rowfold package carries.
  - Good: Few dependencies and a surface two maintainers can actually keep correct.
  - Overdone: Every user re-writes the same Excel or Parquet glue code, badly.
- **[Batteries included](#value-batteries-included)**: `batteries-included@1` How many common tabular jobs a user can do with the core install alone, without finding and installing anything else.
  - Good: Common jobs work out of the box with one install.
  - Overdone: A heavy dependency tree that every downstream project inherits, for features most never use.

**Where we stand:** favors Small core (-0.70).

> Small core. Integrations with other formats and tools live in plugins that depend on rowfold, not the other way round.

**Exceptions we'd accept:**
- An integration may move into the core when it needs nothing beyond the standard library and most downstream users already rely on it.

**Precedents:**
- **Excel reading moved to the rowfold-excel plugin**: Kept out of the core in v2.2 so the core install did not gain a spreadsheet dependency.

### Approachability, performance, correctness (`T04@1`)

Firm position · agreed, with concerns noted

**Values:**

- **[Approachability](#value-approachability)**: `approachability@1` How quickly someone new to rowfold gets a correct first result from the documentation, without help. Good: A newcomer reads a file correctly in one line, from the first example in the docs.
- **[Performance](#value-performance)**: `performance@1` How quickly, and within how little memory, rowfold reads and transforms large files on a single machine. Good: Large files parse quickly and within memory.
- **[Correctness](#value-correctness)**: `correctness@1` The degree to which every table rowfold returns matches what the file actually holds, or rowfold raises a clear error instead of returning a guess. Good: The table you get is the table the file holds, or a clear error that says why not.

**Where we stand:** [Approachability](#value-approachability) 30%, [Performance](#value-performance) 20%, [Correctness](#value-correctness) 50%.

> Correctness is protected first. Within that floor, approachability edges out performance.

**Exceptions we'd accept:**
- A faster code path may become the default only when it passes the same correctness test suite as the path it replaces.

**Precedents:**
- **Ambiguous dates raise an error (v2.1)**: 01/02/2024 stopped being guessed as January or February; rowfold asks for a format, at a cost in speed and in friction for newcomers.

**Maintainer positions** (kept separate, never averaged):
- **Maintainer A**: Approachability 30%, Performance 20%, Correctness 50%; agrees
- **Maintainer B**: Approachability 15%, Performance 35%, Correctness 50%; agrees, with a concern. Worries that slow defaults send users with large files to faster libraries before they ever see rowfold's guarantees.

### Explicit vs. convenient behaviour (`T05@1`)

Working position · agreed by everyone

**Between:** [Explicitness](#value-explicitness) (−1) ↔ [Convenience](#value-convenience) (+1)

- **[Explicitness](#value-explicitness)**: `explicitness@1` The degree to which every choice rowfold makes about a file (encoding, delimiter, types) is either stated by the caller or reported back to them.
  - Good: What rowfold does is visible in the call: no hidden guesses about encodings, types or delimiters.
  - Overdone: Ten keyword arguments to read an ordinary CSV.
- **[Convenience](#value-convenience)**: `convenience@1` How few arguments and steps the common case takes, because rowfold infers sensible settings for the user.
  - Good: Sensible guesses make the common case one short line.
  - Overdone: Magic that works on the demo file and silently mangles the real one.

**Where we stand:** leans toward Explicitness (-0.40).

> Lean explicit. Guessing is allowed when the user asks for it, and rowfold always reports what it guessed.

**Exceptions we'd accept:**
- Interactive helpers (such as rowfold.peek) may guess by default, as long as they print what they guessed.

**Precedents:**
- **Encoding detection is opt-in**: encoding="auto" exists but is never the default; the default is UTF-8 with a clear error on failure.

## Update history

- **1.0.0** (2026-06-02): First confirmed philosophy after interviews with both maintainers (illustrative).
- **1.1.0** (2026-09-14): Portability vs. raw speed moved to revision 2 (compiled extras are welcome when optional); synthesis refreshed.
- **1.1.1** (2026-11-20): Recorded both maintainers' positions on T01; maintainer-b consents with a concern. No stance changed.
