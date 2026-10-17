# Coursera Agent Skills

This repository contains Agent Skills for Coursera MCP-powered learning
experiences. Skills are plain Markdown instruction packages that compatible
agents can load when a user request matches the skill description.

The repository is intentionally skills-only. It does not include a Claude plugin
manifest, Cursor plugin metadata, MCP server manifest, or MCP server code. The
MCP app that consumes this repository is responsible for exposing the Coursera
tools described by each skill.

## Available Skills

### learn-with-coursera

`learn-with-coursera` turns a learner's intent into a guided Coursera experience. It
diagnoses the learner's topic, familiarity, and preferred modality, then routes
to a course, project, video, or roleplay experience and follows up with a
recommended path forward.

Skill package:

```text
skills/learn-with-coursera/
+-- SKILL.md
+-- DIAGNOSE.md
+-- SEARCH-DELIVER.md
`-- PATH-FINDER.md
```

## Install Or Consume

For local agent use, copy the skill folder into the skills directory supported
by your agent:

```bash
cp -R skills/learn-with-coursera ~/.claude/skills/learn-with-coursera
```

Other Agent Skills-compatible tools use similar layouts, usually a top-level
skills directory containing one folder per skill. The portable unit is the
folder that contains `SKILL.md` and any supporting files beside it.

For an MCP app, keep this repository as the source of truth for skill
instructions and package or sync `skills/learn-with-coursera/` into the app's skill
bundle during release. The MCP app should provide the tools listed below; the
skill only describes when and how an agent should call them.

## Skill Contract

`learn-with-coursera` expects the consuming MCP app or agent runtime to provide these
tools:

| Tool                         | Purpose                                                       |
| ---------------------------- | ------------------------------------------------------------- |
| `AskUserQuestion`            | Collect learner choices for diagnosis and roleplay refinement |
| `search_courses`             | Find Coursera courses for the learner's topic and context     |
| `search_videos`              | Find a targeted short video                                   |
| `search_hands_on_learning`   | Find guided projects or hands-on learning experiences         |
| `coursera_roleplay_practice` | Start a live roleplay practice session                        |
| `get_course_materials`       | Retrieve curriculum details for a selected course             |

Tool schemas live in the consuming MCP app. Keep the skill prose aligned with
those schemas when tool names, parameter names, or result shapes change.

## Validation

Run the repository validator before publishing changes:

```bash
node scripts/validate-skills.mjs
```

The validator checks that every direct child of `skills/` is a skill package,
that each package has a valid `SKILL.md` frontmatter block, and that any
Markdown files referenced from `SKILL.md` exist beside it.

## Contributing

See `CONTRIBUTING.md` for the editing checklist and validation expectations.
