# SkillMaxx Weekly skeletons (Issues #5 and #6)

`growth/scripts/newsletter_auto.py` auto-publishes `src/newsletter/issue-N.md` every
Sunday inside `testing/publish_nightly.sh` (email sends stay held in Beehiiv until the
first real non-test subscriber triggers `testing/check_first_subscriber.py`).

These skeletons give Issues #5 (Sun Nov 29, 2026) and #6 (Sun Dec 6, 2026) planned
evergreen sections, live-data spotlight hooks, tailored reader prompts, and optional
post-publish polish prompts while keeping two core guarantees:

1. **Zero placeholders on the published page.** All rendered skeleton text passes
   `newsletter_auto.py`'s `PLACEHOLDER` guard and `review/check_built_site.py`.
   `section_prompts` live in JSON metadata only for optional human/Grok polish after
   auto-publish and are never emitted into `issue-N.md`.
2. **News stays fresh at publish time.** The `👀 On our radar` section is never
   pre-filled with stale links; `publish_nightly.sh` fetches fresh Hacker News items
   each Sunday via `growth/scripts/fetch_radar_hn.py --date <SUNDAY> --radar-json ...`.
