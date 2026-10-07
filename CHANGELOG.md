# Changelog

## v1.3.0 (2026-10-07)

- The whole repo is now in English: `SKILL.md`, README, documentation, examples, test cases, script messages, and the `[LOCAL NOTE]` insertions (previously `[CATATAN LOKAL]`). The `[Inference]` label was previously `[Inferensi]`.
- The skill now answers in the language of the user's request, with English as the fallback (previously Indonesian).
- Renamed: `evals/kasus-uji.md` is now `evals/test-cases.md`, `evals/hasil/` is now `evals/results/`, and example 4 is now `04-claude-code-fable-5-1-mode-b-condensing.md`. Examples use the heading `## Skill output`.
- Test case K12 now checks that a non-English request gets a non-English answer.
- The reference documents themselves are unchanged (same retrieval date).

## v1.2.0 (2026-09-28)

- New supported model: Claude Sonnet 5.5, with the guide `prompting-claude-sonnet-5-5.md` and Sonnet 5 as its parent.
- All references re-fetched as of 2026-09-28. `prompting-best-practices.md` now lists Sonnet 5.5 in the model guide table and the migration section.
- Three new local notes in the Sonnet 5.5 guide for sections that only apply through the API or a harness. The notes in best practices and output consistency now also point to Sonnet 5.5.
- Added test case K13 for Sonnet 5.5.

## v1.1.1 (2026-09-26)

- The skill was renamed from `prompting-claude` to `best-prompting`, invoked with `/best-prompting`. The old name was rejected on upload to claude.ai because the `name` field may not contain the words "claude" or "anthropic".
- The skill folder is now `best-prompting/` and the ready-to-upload zip is now `dist/best-prompting.zip`.

## v1.1.0 (2026-09-26)

- `SKILL.md`: new section 7 on concise prompts. Reference snippets are used only when the symptom is present, one short instruction replaces a list of cases, the reason is given once, each rule is written once, and condensing must not rephrase criteria sentences. Later sections were renumbered.
- Mode B now also diagnoses excess, and removing counts as a fix.
- The analysis closes with the prompt's word count, and in Mode B compares it with the old prompt.
- Added example 4: condensing a bloated prompt (Claude Code, Fable 5.1).

## v1.0.0 (2026-09-26)

First public release.

- The skill was named `prompting-claude` and invoked with `/prompting-claude`.
- Supported models: Claude Sonnet 5, Claude Opus 5.5, Claude Fable 5.1. The model list is now written in a single table in `SKILL.md`.
- References re-fetched from the Anthropic documentation as of 2026-09-26. The new `prompting-best-practices.md` covers Fable 5.1 and Opus 5.5.
- References converted to GitHub format (absolute links, no MDX components) with a uniform source header.
- Local notes updated for the new document structure and stored in `scripts/local_notes.json`.
- The page "Define success criteria and build evaluations" is now called `develop-tests` and was moved to `evals/references/`, so the skill no longer reads it on every invocation.
- `SKILL.md`: the ecosystem may be inferred from context, quotes are limited to one per claim, the language follows the user, the non-programmer assumption became an adjustable default, and image prompts are excluded from the triggers.
- Added: case studies, test cases, an automatic output checker, a zip builder, and a maintenance procedure.
