# Collaborating on SkillMaxx

Two agents work on this repo side by side: **Grok Bot** (cloud box, `/workspace/skillmaxx`) and **Hermes Agent** (Brandon's Mac, `~/org/skillmaxx`, notes in `~/Knowledge`). Humans follow the same rules.

> The default branch is named **`master`**. Everywhere below, "main" means `master`.

## Before you start / when you finish
1. `git pull` and read **[STATUS.md](STATUS.md)**. Check the *In progress / claimed by* table so you don't collide with another agent.
2. Claim your task: add a row to that table (in your branch's first commit, or a quick PR).
3. When done, remove your row, update *Current state* if anything changed, and append a dated entry to the *Session log*.

## Rules
- **main is protected and always deployable.** Every push to main deploys to https://skillmaxx.gilventures.ai via GitHub Pages.
- **One short-lived branch per task**, named `<agent>/<topic>`: `grokbot/beehiiv-embed`, `hermes/fix-dkim-notes`, `brandon/copy-tweaks`.
- **Parallel tasks locally → git worktrees**, not stash juggling:
  ```bash
  git fetch origin
  git worktree add ../skillmaxx-<topic> -b <agent>/<topic> origin/master
  # ...work, commit, push...
  git worktree remove ../skillmaxx-<topic>
  ```
- **Open a PR into main.** Before merging, rebase on the latest main (`git fetch && git rebase origin/master`, then `git push --force-with-lease` *on your own branch only*).
- **Squash-merge**, then **delete the branch** (`gh pr merge --squash --delete-branch`).
- **Never force-push to main.**
- **The `PR build` CI check must pass before merging.**
- **Conventional commits**: `feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `refactor:`, `test:`, `data:` (nightly data refresh). E.g. `feat(newsletter): swap form to Beehiiv embed`.
- **Each agent commits under its own identity** (set per clone with `git config user.name/user.email`):
  | Agent | Identity |
  |---|---|
  | Grok Bot | `SkillMaxx Grok Bot <skillmaxx@mail.grokbot.com>` |
  | Hermes | `SkillMaxx Hermes <…>` (Hermes sets its own) |
  | Brandon | his GitHub identity |

## Automated runs
The nightly refresh (`testing/nightly.sh`, ~2 AM ET) commits data-only changes (`data:` commits). It may push straight to main as an admin bypass so it never gets stranded; anything that touches code goes through a PR.

## Local build & QA
```bash
npm ci
SITE_URL=https://skillmaxx.gilventures.ai PATH_PREFIX=/ npx @11ty/eleventy
(cd _site && python3 -m http.server 8080) &
node clicktest.mjs            # click tests
node review/qa.mjs <round>    # console errors, overflow, axe a11y, link crawl
```
Keep every claim on the site honest: numbers come from `data/` and `testing/results/`, never typed by hand.
