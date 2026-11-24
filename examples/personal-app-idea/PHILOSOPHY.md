# Personal App Idea (example project): philosophy

## Bottom line

Example project: Personal App Idea is a budgeting app for people who want to know where their money goes without handing their financial life to a company. Privacy comes before convenience: you type in or import your own transactions, and nothing about your money leaves your phone or computer unless it is end-to-end encrypted first. Features that connect to the outside world, such as bank sync or backup, are welcome only when you turn them on yourself, and manual entry always stays the default. The everyday app stays simple enough for a first-time budgeter, while more powerful tools, such as forecasts, live in an Advanced view you choose to open. Where money is involved, the team finishes and checks the work before it ships; everywhere else it ships small and improves later.

Version 1.1.0 · schema `philosophical-alignment/0.1-draft` · strictness: advisory

> **Status:** EXAMPLE PROJECT. Personal App Idea is fictional, invented for the Philosophical Alignment demo on 2026-11-23. Its maintainers, releases, dates and quotes are illustrative, not a real app's record.

**Strictness:** advisory by default (the AI assistant explains and proceeds).

Advisory overall. A proposal that puts the line about money data at risk always stops and asks.

**Mission.** Example project: Personal App Idea is a simple personal budgeting app that keeps your money data on your device.

**Maintainers.** Maya (lead; designs the everyday budgeting screens (fictional)); Sam (builds import, sync and reports (fictional))

## Lines we never cross

Never traded against anything. Crossing one needs a change to the philosophy itself.

- **H1**: Unencrypted money data never leaves your device. *(Source: Example: Maya's and Sam's first interviews, and the promise on the app's download page)*

## Glossary

What each value means in this project. The priorities below link here.

<a id="value-privacy"></a>
### Privacy (`privacy@1`)

The degree to which your money data stays on your own device, readable only by you, unless you choose to send it somewhere in a form only you can unlock.

- **Looks like:** The app works fully with no account and no internet connection; Anything that leaves the device is end-to-end encrypted with a key only you hold; No analytics or crash reports that include amounts, payees or account names
- **Too little looks like:** Your transactions sit readable on someone else's server, where a breach, a sale of the company or a court order can expose them.
- **Not to be confused with:** Not security in general: a well-guarded server that can read your data is still not private. Not keeping data from you: exports and backups you control are fine. Not a ban on the internet: Convenience features may connect, as long as what they send is encrypted first.
- **In the maintainer's own words:** "Private means that if the company behind the app disappeared tomorrow, or got hacked, or got bought, nobody would learn a thing about what you spend. Your phone knows. You know. That's the whole list."
- **Done well:** Backups encrypted on your phone with your passphrase before they reach your cloud folder
- **Missing or faked:** A 'private' budgeting app that sends every transaction to its server to sort it into categories

<a id="value-convenience"></a>
### Convenience (`convenience@1`)

How little typing, setup and remembering it takes to keep your budget up to date.

- **Looks like:** Transactions arrive without retyping them; Categories suggested from your own past choices; A month's budget set up in a few minutes
- **Too little looks like:** People stop logging purchases after the second week, and the budget quietly goes stale.
- **Not to be confused with:** Not Simplicity: a simple screen can still take a lot of typing, and an automatic feature can be complicated. Not doing things without asking: here, convenience never means sending data you did not choose to send.
- **In the maintainer's own words:** "Convenient means the budget keeps itself current with almost no effort from you. Every time someone has to type the same coffee purchase by hand, that's a person deciding budgeting isn't for them."
- **Done well:** CSV import that remembers how your bank's file is laid out
- **Missing or faked:** An 'automatic' import that needs a dozen settings checked every month

<a id="value-simplicity"></a>
### Simplicity (`simplicity@1`)

How quickly a first-time budgeter can understand and use every screen they see by default, without help or a manual.

- **Looks like:** One home screen: what you have, what you've spent, what's left; Plain words for money ideas, with no finance jargon; New options start switched off
- **Too little looks like:** New users open the app, see charts and settings they don't understand, and leave.
- **Not to be confused with:** Not having few features: a feature can exist as long as it doesn't crowd the screens everyone sees. Not Convenience, which is about effort, and not Polish, which is about how finished something is.
- **In the maintainer's own words:** "Simple is my mom opening it for the first time and knowing, in ten seconds, whether she can afford dinner out this week. If she has to ask me what a screen means, it's not simple."
- **Done well:** The home screen's single 'left to spend this month' number
- **Missing or faked:** A 'simple mode' that still opens on a dashboard of six charts

<a id="value-power"></a>
### Power (`power@1`)

How much a person who wants depth can plan, analyse and customise their money in Personal App Idea without leaving it for a spreadsheet.

- **Looks like:** Forecasts of spending and balances for the months ahead; Custom rules, splits and categories; Detailed reports and exports
- **Too little looks like:** Committed users outgrow the app and go back to their spreadsheets.
- **Not to be confused with:** Not Convenience: powerful tools often take more effort, not less. Not complexity for its own sake: a feature counts here only if people actually use it to plan.
- **In the maintainer's own words:** "Power is for the person who's been budgeting for ten years. They want to ask 'if I keep this up, where am I in March?' and get the answer here, not in a spreadsheet they built themselves."
- **Done well:** Category rules that sort a year of imported transactions in one pass
- **Missing or faked:** A reports page with twenty chart types and no way to answer a real question

<a id="value-shipping-speed"></a>
### Shipping speed (`shipping-speed@1`)

How soon an improvement or fix reaches people's devices after the team decides to build it.

- **Looks like:** Small releases every week or two; A reported bug fixed and released within days
- **Too little looks like:** Requests sit for months, and people assume the app has been abandoned.
- **Not to be confused with:** Not cutting corners on money: speed here is about the size and rhythm of releases, not skipping checks. Not Power: shipping more features is different from making them deeper.
- **In the maintainer's own words:** "Speed is how long someone waits between asking and having it. There are two of us, so small and often beats big and rare."
- **Done well:** The dark-mode fix that went out two days after the first report
- **Missing or faked:** A weekly release that only bumps the version number

<a id="value-polish"></a>
### Polish (`polish@1`)

How finished and trustworthy a feature feels: correct numbers, clear wording, and no rough edges in the steps people take.

- **Looks like:** Balances that match the bank to the cent; Every empty screen and error message says what to do next; Undo for anything that changes a number
- **Too little looks like:** One wrong total, and people stop trusting every number in the app.
- **Not to be confused with:** Not Simplicity: a complicated screen can be polished, and a simple one can be rough. Not perfection: polish means finished for the people who will use it, not endlessly reworked.
- **In the maintainer's own words:** "If it touches money, it has to be right and feel right. Nobody forgives a budgeting app that's off by twelve dollars."
- **Done well:** Recurring bills that land correctly at the end of short months
- **Missing or faked:** A beautiful chart whose totals don't match the transaction list

### Other terms

Words the philosophy relies on that are not values, and what they mean here.

- <a id="term-money-data"></a>**money data** (`money-data@1`): Anything that describes your finances: accounts, balances, transactions, payees, budgets and categories, including notes you attach to them.
- <a id="term-end-to-end-encrypted"></a>**end-to-end encrypted** (`end-to-end-encrypted@1`): Encrypted on your device with a key only you hold, so any server or cloud folder it passes through, the app's own included, stores only data it cannot read.
- <a id="term-opt-in"></a>**opt-in** (`opt-in@1`): Off until you turn it on yourself, after a plain explanation of what it sends and where.
- <a id="term-advanced-view"></a>**Advanced view** (`advanced-view@1`): An optional part of the app that you switch on in Settings. It holds tools for experienced budgeters, and turning it on changes nothing on the screens everyone sees.

## Priorities

Each one names two or more good things that pull against each other, and where this project stands.

### Privacy vs. Convenience (`T01@1`)

Firm position · agreed by everyone

**Between:** [Privacy](#value-privacy) (−1) ↔ [Convenience](#value-convenience) (+1)

- **[Privacy](#value-privacy)**: `privacy@1` The degree to which your money data stays on your own device, readable only by you, unless you choose to send it somewhere in a form only you can unlock.
  - Good: Your money data stays on your device, so no breach, sale or court order somewhere else can expose it.
  - Overdone: Everything is typed by hand, people give up after two weeks, and a private budget nobody keeps helps no one.
- **[Convenience](#value-convenience)**: `convenience@1` How little typing, setup and remembering it takes to keep your budget up to date.
  - Good: Transactions arrive on their own, so the budget stays current with almost no effort.
  - Overdone: Your bank logins and every purchase sit on a company's server, readable by whoever runs it or breaks into it.

**Where we stand:** favors Privacy (-0.60).

> Privacy over convenience. Manual entry and file import are the default; anything that connects to the outside world is opt-in and end-to-end encrypted.

**Exceptions we'd accept:**
- Cloud features are welcome when they are opt-in and end-to-end encrypted, and manual entry stays the default.

**Precedents:**
- **CSV import shipped before bank sync (v1.2)**: Importing your bank's own export file gave most of the convenience of sync with nothing leaving the device. Sync through a third-party bank-data service was set aside, because that service would have read every transaction.
- **Encrypted backup to your own cloud folder (v2.0)**: Off until you turn it on. The backup is encrypted on your device with your passphrase before it is written to iCloud, Google Drive or any folder you pick; Personal App Idea never sees it, and a lost passphrase means a lost backup.

### Simple vs. Powerful (`T02@2`)

Firm position · agreed, with concerns noted

**Between:** [Simplicity](#value-simplicity) (−1) ↔ [Power](#value-power) (+1)

- **[Simplicity](#value-simplicity)**: `simplicity@1` How quickly a first-time budgeter can understand and use every screen they see by default, without help or a manual.
  - Good: A first-time budgeter understands every screen they see and keeps using the app.
  - Overdone: Experienced budgeters hit a ceiling within a month and go back to their spreadsheets.
- **[Power](#value-power)**: `power@1` How much a person who wants depth can plan, analyse and customise their money in Personal App Idea without leaving it for a spreadsheet.
  - Good: People who plan ahead can forecast, customise and analyse without leaving Personal App Idea.
  - Overdone: The home screen fills with charts and settings, and new users quit before they finish their first budget.

**Where we stand:** leans toward Simplicity (-0.40).

> Simple by default. Advanced tools are welcome in an opt-in Advanced view; the screens everyone sees stay as simple as before.

**Exceptions we'd accept:**
- An advanced tool may move from the Advanced view onto the everyday screens when most people who turn the Advanced view on use it, and first-time budgeters understand it without help in testing.

**Precedents:**
- **Split transactions kept to one simple form (v1.3)**: Splitting a purchase across categories stayed a single Split button with two amounts. Percentage rules and saved splits were left off the everyday screens.
- **Category rules live in Settings (v1.6)**: Rules such as "anything from the farmers market is Groceries" shipped as an opt-in screen under Settings; the add-transaction form did not change.

**Maintainer positions** (kept separate, never averaged):
- **Maya**: favors Simplicity (-0.60); agrees. The home screen is where people decide whether budgeting is for them; anything that makes it harder to read costs more than it adds.
- **Sam**: leans toward Power (+0.20); agrees, with a concern. Agrees to the Advanced view, but worries that tools hidden behind a switch go unnoticed by the people who would use them most. Would rather show a one-time hint once a budget has three months of history.

**Revisions:**
- T02@2 (2026-11-12): Forecast charts confused first-time budgeters on the home screen. Before: "If a beginner would need help with it, it does not ship." After: "Simple by default; advanced tools live in an opt-in Advanced view."

### Move fast vs. Polish (`T03@1`)

Working position · agreed by everyone

**Between:** [Shipping speed](#value-shipping-speed) (−1) ↔ [Polish](#value-polish) (+1)

- **[Shipping speed](#value-shipping-speed)**: `shipping-speed@1` How soon an improvement or fix reaches people's devices after the team decides to build it.
  - Good: Fixes and small improvements reach people within days, and the app visibly gets better.
  - Overdone: Half-finished features and wrong totals that make people doubt every number.
- **[Polish](#value-polish)**: `polish@1` How finished and trustworthy a feature feels: correct numbers, clear wording, and no rough edges in the steps people take.
  - Good: Every number is right and every step is clear, so people trust the app with their money.
  - Overdone: Months between releases while a team of two perfects details nobody asked about.

**Where we stand:** leans toward Polish (+0.30).

> Polish first where money is involved: anything that changes a balance or a total is finished and checked before it ships. Everything else ships small and improves later.

**Exceptions we'd accept:**
- A fix for a wrong balance or a privacy bug ships as soon as it is correct, even if the wording and layout around it are still rough.

**Precedents:**
- **Recurring transactions waited one release (v1.4)**: Held back two weeks until monthly totals were right to the cent for bills that fall on the 29th, 30th or 31st.

## Update history

- **1.0.0** (2026-08-04): First confirmed philosophy, after separate interviews with Maya and Sam.
- **1.0.1** (2026-09-22): Added the encrypted backup (v2.0) as an example of a cloud feature done our way. Nothing else changed.
- **1.1.0** (2026-11-12): Simple vs. Powerful updated to revision 2 after the spending-forecast work. Maya's and Sam's positions recorded separately; the shared position is the team's decision, not their average, and Sam agrees with a concern. Summary at the top refreshed.
