# Code Modernization

Point Claude at a legacy codebase and get four things: an understanding of what it is and what it does, a plan you approve, the modernized code, and **proof that the new code behaves like the old**. It works with any language and any kind of move: a newer version of the same technology, a rewrite in another one, or a rebuild on a new architecture.

![One report page with everything found so far: a green banner when the proof passes and the old and new outputs match, the command to run next, the steps done, and the counts, with tabs for the assessment, the map, the business rules, the plan, the build notes and the proof.](assets/media/report-glance.jpg)

## Install

You need [Claude Code](https://code.claude.com). Then:

```
/plugin install code-modernization@claude-plugins-official
```

Some steps start many agents at once, so expect real usage on a large system (see *What to expect*). Start with one module or one unit as a pilot, not the whole estate.

## Start here

Open a folder for the work and type `/code-modernization:modernize`. It asks what you want to do with your code (a couple of short questions), finds the code, writes your answers down once, shows the road ahead, and gives you the exact first command. Every later command reads what you said, so nothing is asked twice. **Not sure what you want?** Choose *Understand it first*: you get the assessment, the map, the business rules and a plan, and no code is rebuilt.

To go step by step instead, point the first command at your code and follow the "next step" line each command ends with:

```
/code-modernization:modernize-preflight <name> --source <path to your code>
/code-modernization:modernize-status <name>       # where am I, and what is next: run it any time
```

`<name>` is a short label of your choice (letters, digits, `-`, `_`). `--source` makes a link at `legacy/<name>` and copies nothing, so a huge repository stays where it is. **Nothing edits your legacy source.** Commands write only to `analysis/<name>/` and `modernized/` (a build check writes build output where your build normally does), and each refreshes `analysis/<name>/REPORT.html`: one page, with everything found so far, that you can open or share. A few steps need someone who knows how the system is built and run, so bring an engineer for the first questions.

## The path

Each step stands alone, so you can stop and review after any of them.

| Step | Command | What you get |
| --- | --- | --- |
| 0 | `modernize` | Say what you want. Writes `INTENT.md`; every later command reads it. |
| 1 | `modernize-preflight <name> [target-stack] [--source <path>]` | Is the environment ready? Asks five questions only a person can answer (is this the whole system or a slice, can it build and test here, is there custom build tooling, has anyone tried before, is anything off limits), proves a build works on this code, and finds missing source. |
| 2 | `modernize-assess <name>` | What am I dealing with: inventory, complexity, debt, security, and a recommended pattern. |
| 3 | `modernize-map <name>` | The structure: dependencies, data flow, entry points and business flows, as an interactive map. |
| 4 | `modernize-extract-rules <name>` | The business rules as testable Given/When/Then cards with `file:line` citations, each re-checked by a second agent. |
| 4b | `modernize-review <name>` | A person confirms or corrects the rules that look wrong. Your answers reach the plan and the build. With the live pane on, `/modernize-review-pane` does the same one card at a time. |
| 5 | `modernize-brief <name> [target-stack]` | The phased plan a steering committee approves. **Nothing is built until you approve it.** |
| 6 | `uplift`, `transform` or `reimagine` | The build (see below). |
| 7 | `modernize-verify <name>` | **The proof.** An independent re-check with one verdict per module. |
| 8 | `modernize-harden <name>` | A security scan of the legacy system with a reviewed patch you apply yourself. |

`assess --portfolio <parent-dir>` surveys many systems and ranks them on one page. `modernize-status <name>` says where you are and gives the exact command to paste.

**A person decides at six points**, and the plugin never decides them for you: the five preflight answers, the rules that look wrong (`review`), approving the brief, accepting any difference the proof finds, signing the proof, and applying the security patch.

## How it proves the result

Modernization fails quietly: the new code passes the tests someone wrote, and differs on the inputs nobody thought of. So the proof is built from evidence a script can check, not from the model's opinion. `modernize-verify` runs after a build, ideally in a fresh session, and re-does the work instead of trusting the notes the build left behind:

- **The tests, run again from clean.** Build output is deleted, the full suite runs, and the counts come from the runner's own result files or a saved log. A run that executed no tests, or skipped them, is a failure, and a count the command merely typed in does not count.
- **Old and new on the same inputs.** Where the legacy code can run, both run on the same inputs and a script compares every byte. Only fields that must vary (timestamps, generated ids) are masked, floating-point output can be compared within a declared tolerance, and every masked field is listed in the result. A difference a person accepts is recorded with the reason.
- **Inputs nobody used.** It invents at least ten new inputs (boundaries, empty, huge, unusual order, and malformed records when you asked for exact behavior, quirks included) and compares again, so a suite that only passes on the cases the model chose is caught.
- **Tests that can fail.** A deliberate one-line break must turn tests red (the canary), and the comparison itself is checked by changing one byte of an output.
- **Every critical rule is backed by a test that ran.** Each P0 business rule must be named by a test that executed and passed. A rule named only by a skipped or pending test is listed as "named, not run", and a test folder that holds no code of its own is listed as tooling and gets no verdict.
- **The source is untouched**, checked by file times without running anything inside the analyzed tree.

Each module gets one verdict, computed by `scripts/proof_pack.py` from those files with rules written into the output: **PROVEN**, **PARTLY PROVEN** (with what is missing) or **NOT PROVEN** (nothing ran, something differs, a test fails). If the old system cannot run where you work (a mainframe program, a system that only runs in production), the old behavior can only be checked against recorded outputs, and the best verdict is PARTLY PROVEN: the page says so plainly. Anything a person must decide (open questions, exit criteria, the sign-off) is listed as waiting for a person and is never ticked for you. Every verdict is computed again from current evidence each time; none is carried over from an earlier run.

![The proof tab of the report: what passed for one rewritten module, a table of checks each with its detail, and the count of critical rules that a test names.](assets/media/report-proof.jpg)

## Choose how to build (the plan recommends one)

| If you want | Run | What happens |
| --- | --- | --- |
| The same technology on a newer version (.NET Framework to .NET 8, Java 8 to 17, Spring Boot 2 to 3) | `modernize-uplift <name> [source-version] [target-version]` | Keeps your code and fixes only what the new version breaks, driven by a catalog of the breaking changes this code actually hits. One pilot unit first with its lessons written down, then batches. The proof is the same test suite run on both versions. |
| A new technology, one module at a time, while the old system keeps running | `modernize-transform <name> [module] [target-stack]` | A plan you approve, tests that pin the old behavior, an idiomatic rewrite, and proof: old and new run on the same inputs and a script compares them. |
| A rebuild on a new architecture | `modernize-reimagine <name> [target-vision]` | A spec mined from the code, an architecture that is reviewed and approved, then services scaffolded with executable acceptance tests. |

A version move keeps your code, so it can skip `extract-rules` and `review`: `preflight`, `assess`, `uplift`, `verify` is a complete path, and `map` and `brief` add the unit order and an approved phased plan for a large system. If the delta catalog shows an "uplift" would rewrite most of the code, the command says so and points to `transform`. Rehost (move as is) and Replace (buy a product) change no code, so no build command applies; the analysis is still useful for both.

## What it has been tried on

The commands were run for real, headlessly, on public codebases while the plugin was built, and what broke was fixed. Every number below comes from the files those runs wrote. The same command can give different counts on a second run (the security scan of the osCommerce code found 48 confirmed findings and then 52), so read the numbers as typical, not exact. Wherever a person had to decide (approve a plan, accept a difference), the tester played that person. Some runs stopped early because of limits of the test machine (it refused to run any freshly compiled program, and its package index refused installs); the plugin said so and did not work around them.

| Codebase | Move | What it did and what was shown |
| --- | --- | --- |
| **AWS CardDemo** (COBOL, CICS, JCL) | Rewrite in Java, one job at a time | 35 rules (8 critical) and a five-phase plan, then the monthly interest job rewritten in Java 21 (213 tests at the end). Five independent checks in a row compared it with the real COBOL program, built locally, on inputs written after the fact. Each found something the tests had missed, and each was answered: a blank field that halted the job, a non-numeric account key, a negative zero, and differences the owner accepted as deliberate. The last check tried fifteen more inputs with malformed records and found seven more differences, so it ended NOT PROVEN. It also told two problems of the old system's test harness apart from defects in the new code. What ends a loop like this is a person deciding which inputs are in scope; the verify command now reads that from the intent you gave the front door. |
| **Eclipse Jetty** (Java 8, 2,600 files) | Java 8 to 17 | A pilot on the `jetty-util` module: the same 946 tests give the same results on both Java versions. Building and running both versions found six changes that reading the code had not predicted: a direct buffer reported as memory-mapped on 17, a bundle plugin that writes an invalid manifest and still says SUCCESS, and a build on JDK 13 to 16 that would have shipped Java 8-labelled classes that crash on Java 8, among others. 50 tests were added for the 25 of 56 critical rules that had none (996 tests run on each version, no differences). |
| **osCommerce** (PHP 5, about 44,000 lines of PHP) | PHP to Python and FastAPI | 97 rules (26 critical) and a six-phase plan. First slice, the product page: 17,957 tests pass, and 17,727 comparison cases against the real PHP files are identical. Two deliberate breaks each turned tests red. The architecture review found two high-severity problems (expired specials still shown, and a page request holding a database write lock) that were fixed with tests that failed first. An independent verification said PROVEN: its own break made 647 more tests fail, and 14 new inputs matched the real PHP. |
| **AngularJS RealWorld** (AngularJS 1.5) | AngularJS to React and TypeScript | 79 rules (5 critical). The articles service was rewritten: 166 tests, and 29 comparison cases against recorded responses of the real API (23 identical, 6 differences approved as deliberate, none unexplained). Four deliberate breaks each turned tests red, and the review's two high-severity findings were fixed. Checked by the build step itself; there was no separate verificatio