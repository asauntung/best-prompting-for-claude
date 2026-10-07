# Testing the /best-prompting skill

Purpose of this folder: make sure the skill keeps behaving correctly after the references are updated, a new model is added, or `SKILL.md` is changed. The approach follows the Anthropic document included at [`references/develop-tests.md`](references/develop-tests.md): define specific, measurable success criteria, then test with cases that cover both normal and edge situations.

`develop-tests.md` is deliberately kept here, not in `best-prompting/references/`, so the skill does not read it on every invocation.

## How to run

1. Open a new conversation with the skill installed. One case, one conversation.
2. Send the "Input" of a case from [`test-cases.md`](test-cases.md) as is.
3. Save the skill output to `evals/results/<ID>.md` (this folder does not need to be committed).
4. For cases that produce a prompt, run the automatic checker:

   ```bash
   python3 scripts/check_output.py evals/results/*.md
   ```

5. Grade the manual criteria of each case: pass or fail, with a short note.

## Two layers of grading

**Automatic** (`scripts/check_output.py`): a valid Final line right before the codeblock, exactly one `text` codeblock, no text after it, no em-dashes, no API mechanics or prefill in the prompt, `file-name > section` references present and pointing to files that actually exist, plus warnings about possible hard wraps.

**Manual** (rubric per case): quote accuracy, relevance of the analysis, effort assessment, and adherence to the expected behavior. For quote accuracy, pick two quotes at random and search for them in their reference file. A quote that is not found exactly is a fail.

## Release threshold

All cases marked **[required]** must pass before a new version is released. For other cases, record failures in `CHANGELOG.md`.
