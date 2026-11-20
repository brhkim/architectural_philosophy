# Tension library

A starter set of trade-offs that projects commonly navigate, drawn from published design philosophies,
manifestos and research methodology. It exists to jog memory, not to define the project.

## How to use it

- **Only after the maintainer's own words.** Run steps 1 to 7 of `interview-playbook.md` first. Showing this
  list earlier anchors answers toward its vocabulary and away from what the maintainer actually cares about.
- **As prompts, not a checklist.** Show a handful (five to eight) filtered by project type: "Projects like
  this often name tensions like these. Does any of them matter here in a way we have not covered?"
- **In the maintainer's wording.** A library tension that the maintainer adopts is renamed, split or merged
  as they see fit, and each of its values goes through "define before you weigh" like any other. The library
  names below are not definitions.
- **Neither side is the right side.** Every pole below is phrased as a good. Respected projects sit on each
  side of most of these; saying so helps the maintainer answer honestly.
- **IDs here are library IDs** (`L01` to `L60`), not the project's tension IDs. A project's tensions get their
  own `T` numbers. If a project tension came from this list, the agent can note it in the tension's `origin`
  field (`"library L07"`), which helps later comparisons across projects.

**Shape** marks two-way pairs, three-way triads, and n-way networks (four or more values, or a group against a
group). **Lineage** names where the tension is stated or illustrated; "(added)" marks a tension added from
general knowledge without a cited source. Full citations are in the project's research notes; the short
names here are enough to look them up.

## Contents

- Any project
- Software libraries and languages
- Applications
- Package managers, platforms and infrastructure
- Research projects
- Data analysis
- Documentation and teaching
- Tools built around AI agents
- A palette of value names
- Forms a stance can take, from the same sources

---

## Any project

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L01 | Scope and quality, delivery time, cost and resources | 3-way | Project management triangle ("good, fast, cheap: pick two"); Shape Up's "fixed time, variable scope" |
| L02 | Shipping now and learning, getting it right the first time | 2-way | Cantrill's platform values (velocity against rigor); Zen of Python ("now is better than never / never is often better than right now"); Gabriel's "Worse is Better" |
| L03 | Approachability for newcomers, power and robustness for experts | 2-way | Cantrill (node.js against Joyent) |
| L04 | Practicality, principled purity | 2-way | Zen of Python ("practicality beats purity"); Tao of HashiCorp ("Pragmatism") |
| L05 | Consistency across the whole, the locally best solution for each case | 2-way | Tidy design principles; Go proverb on gofmt; Gabriel |
| L06 | One obvious way, a diversity of approaches | 2-way | Zen of Python against the Unix "Rule of Diversity" |
| L07 | Stability of commitments, freedom to change and improve | 2-way | Cantrill; Amazon tenets ("durable and changeable"); Rust "stability without stagnation" |
| L08 | Growing the community, keeping values coherent | 2-way | Cantrill ("larger communities are more likely to fracture") |
| L09 | Broad inclusion and accessibility, depth for a core audience | 2-way | Tidy design ("inclusive"); ISO 25010 inclusivity |
| L10 | Open, participatory decision-making, decisive and coherent leadership | 2-way | Cantrill ("democracy does not necessarily imply leadership") |
| L11 | Automation and codified process, human judgment and discretion | 2-way | Tao of HashiCorp (codification); the judgment pole is added |
| L12 | Prototype early and throw away, design up front for the long term | 2-way | Unix philosophy (McIlroy's "tried early"; Rule of Optimization against Rule of Extensibility) |

## Software libraries and languages

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L13 | Simplicity, correctness, consistency, completeness | n-way (4) | Gabriel, "Worse is Better": two schools rank the same four values differently |
| L14 | A simple implementation, a simple interface | 2-way | Gabriel |
| L15 | Expressiveness and power, simplicity and learnability | 2-way | Cantrill; Zen of Python |
| L16 | Runtime performance, human ergonomics (time to write and read) | 2-way | Tidy design ("optimise first for humans ... then performance"); Unix Rule of Economy |
| L17 | Reliable, performant, supportive, productive, transparent, versatile | n-way (6, many-to-many) | Rustacean Principles (ordered list with per-value "in tension with" pages) |
| L18 | Explicit, predictable control, convenient implicit behaviour | 2-way | Zen of Python ("explicit is better than implicit"); Rust closure-capture precedent |
| L19 | Exposing low-level control, freedom to optimise behind an abstraction | 2-way | Rustacean Principles (performant against transparent) |
| L20 | Clarity, concision and cleverness | 2-way | Go proverbs ("clear is better than clever"); Unix Rule of Clarity |
| L21 | Fail loudly and early, keep running and degrade gracefully | 2-way | Unix Rule of Repair; Zen ("errors should never pass silently"); Zig Zen; Reactive Manifesto ("resilient") |
| L22 | Approachability, compatibility, expressiveness against robustness, debuggability, simplicity | n-way (3 against 3) | Cantrill's promises debate |
| L23 | Small composable parts, an integrated batteries-included experience | 2-way | Unix; Tao of HashiCorp; tidy design ("composable") |
| L24 | Extensibility, integrity and safety | 2-way | Cantrill's value palette (pairing added) |
| L25 | Backward compatibility with an ecosystem, the project's own values | 2-way | Cantrill ("compatibility with JavaScript will trump robustness") |
| L26 | Portability, platform-specific performance and features | 2-way | Go build-tag proverbs; HPC write-up of Cantrill |
| L27 | Generality (do anything), focus on a well-bounded problem | 2-way | Rustacean "versatile"; SQLite ("competes with fopen()") |
| L28 | Helpful guidance and niceties, raw efficiency | 2-way | Rustacean Principles (supportive against performant) |
| L29 | A little copying (self-containment), reuse of shared dependencies | 2-way | Go proverb ("a little copying is better than a little dependency") |

## Applications

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L30 | Security, usability and ease of onboarding | 2-way | HPC write-up of Cantrill; ISO 25010 |
| L31 | Speed of learning and delivery, unit cost at scale (often flips with lifecycle stage) | 2-way | Amazon tenets (speed first, then cost as the application scales) |
| L32 | Opinionated defaults, user configurability | 2-way | Zen of Python ("one obvious way"); tidy design (added for applications) |
| L33 | Feature breadth, polish of the core experience | 2-way | Shape Up (variable scope); Agile Manifesto (added for applications) |
| L34 | Performance, cost | 2-way | HPC write-up of Cantrill |

Applications also commonly face L01 to L12, L15, L21 and L23.

## Package managers, platforms and infrastructure

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L35 | Reproducible, pinned state, staying current (security fixes, new features) | 2-way | Tao of HashiCorp (immutability); Hinsen on software collapse |
| L36 | Zero administration and independence, scalability and centralised control | 2-way | SQLite, "Appropriate uses" |
| L37 | Performance, observability and measurability | 2-way | HPC write-up; Cantrill (measurability) |
| L38 | Availability, consistency under partition, latency | 3-way | CAP and PACELC (added; not fetched) |
| L39 | Strict, correct resolution and validation, permissive acceptance of the existing ecosystem | 2-way | Unix (generosity in what you accept); package-manager framing added |
| L40 | A stable release channel, fast access to experimental features | 2-way | Rust release channels and feature gates |
| L41 | Central curation and trust, open publishing with low friction | 2-way | (added) |

## Research projects

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L42 | Generalizability, precision and control, realism of context | 3-way | McGrath's "three-horned dilemma" (no single study maximises all three) |
| L43 | Generality, realism, precision of models (contested whether necessary) | 3-way | Levins; Orzack and Sober; Odenbaugh |
| L44 | Openness and sharing, protection (participants' privacy, partners' trust, intellectual property) | 2-way | Levin and Leonelli; Guzzo and colleagues; FAIR principle A1.2 |
| L45 | Confirmatory rigor (pre-registration, fixed plans), exploratory flexibility | 2-way | Guzzo and colleagues |
| L46 | Good-enough practice adoptable now, best practice | 2-way | Wilson and colleagues, "Good enough practices in scientific computing" |
| L47 | Long-term reproducibility and maintenance, moving on to new research | 2-way | Hinsen, "Dealing with software collapse" |
| L48 | Standardised, FAIR, interoperable outputs, local fit and low effort | 2-way | FAIR principles; Levin and Leonelli against one-size-fits-all openness |
| L49 | Replication and robustness, novelty and breadth of research styles | 2-way | Guzzo and colleagues (replication paradox and narrowing) |

## Data analysis

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L50 | Data matching, exhaustive, skeptical, second-order, transparent, reproducible (weights set by audience, time, budget and stakes) | n-way (6) | Hicks and Peng, principles of data analysis |
| L51 | Predictability, computability, stability | 3-way | Yu and Kumbier, veridical data science (tension reading added) |
| L52 | Interpretable mechanism, predictive accuracy | 2-way | Breiman, "Statistical Modeling: The Two Cultures" |
| L53 | Privacy protection, statistical accuracy (an operating point, not a pick) | 2-way | Abowd and Schmutte |
| L54 | Rigor and thoroughness, timeliness of answers | 2-way | Hicks and Peng ("quick analysis" vignette); Cantrill |
| L55 | Fidelity to the real question, data that is available now | 2-way | Hicks and Peng (data matching) |
| L56 | Analyst time, compute time | 2-way | Unix Rule of Economy; tidy design |

## Documentation and teaching

| ID | Goods in tension | Shape | Lineage |
|----|------------------|-------|---------|
| L57 | Completeness, brevity and approachability | 2-way | Gabriel (completeness); Agile Manifesto (working software over comprehensive documentation) |
| L58 | Technical accuracy and nuance, accessible simplification for learners | 2-way | Tidy design on cognitive load (framing added) |
| L59 | Opinionated guidance (one recommended path), neutral coverage of alternatives | 2-way | Zen of Python against Unix diversity |
| L60 | Context and background, focus on the main line | 2-way | Hicks and Peng ("second-order" principle) |

## Tools built around AI agents

All added for this skill from general knowledge (no cited source); useful for agent frameworks, coding
assistants and analysis tools that run AI agents.

| ID | Goods in tension | Shape |
|----|------------------|-------|
| L61 | Human oversight and understanding, agent autonomy over long stretches | 2-way |
| L62 | Thoroughness of context and review, economy (cost), responsiveness (wall-clock time), reliability | n-way (4) |
| L63 | Candor about limits, persuasive claims that win adoption | 2-way |
| L64 | A full, auditable record, a simple output a newcomer can follow | 2-way |

## A palette of value names

When the maintainer is searching for a word, these vocabularies help. Offer them only after the maintainer has
tried their own words, and define any adopted word through step 3 of the playbook; a palette word is a label,
not a definition.

- **Cantrill's 24 platform values:** approachability, availability, compatibility, composability,
  debuggability, expressiveness, extensibility, interoperability, integrity, maintainability, measurability,
  operability, performance, portability, resiliency, rigor, robustness, safety, security, simplicity,
  stability, thoroughness, transparency, velocity.
- **Rustacean Principles:** reliable, performant, supportive, productive, transparent, versatile.
- **Tidy design principles:** human-centred, consistent, composable, inclusive.
- **Research and data analysis:** generalizability, precision, realism, reproducibility, openness,
  protection, interpretability, predictive accuracy, timeliness, skepticism, exhaustiveness, data matching.
- **Quality-attribute catalogs** (ISO/IEC 25010 and the "-ilities" lists) are vocabularies with "degree to
  which ..." definitions, useful for wording a definition. They are not interview prompts: they are long,
  neutral and have no losing sides.

## Forms a stance can take, from the same sources

These help when the maintainer has a stance but not a way to say it.

| Form | Example | Fits |
|------|---------|------|
| "A over B, while B has value" | Agile Manifesto; tidy design's "consistency over performance" | Polarity summaries |
| "A. Although B." | Zen of Python ("Errors should never pass silently. Unless explicitly silenced.") | A stance plus its flip condition in one line |
| An ordered list as tie-breaker | Rustacean Principles; Amazon tenets ("unless you know better ones") | Network `priority` |
| The same values in a different order | Gabriel's two schools | Comparing maintainers |
| Weights set by context | Hicks and Peng | Network `weights` plus flip conditions |
| Which corner is pinned, which flexes | Shape Up ("fixed time, variable scope") | Triad `pick` and `floors` |
| An observable checklist | SQLite ("Many concurrent writers? Choose client/server") | Flip conditions |
| Too little, right, too much | Rustacean Principles (from Amazon's leadership principles) | Glossary `too_little` and `too_much`; pole `overdone` |
| A mechanism that softens the tension | Rust release channels; tidy design's escape hatch to base R | `mechanisms` |
