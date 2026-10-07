# Maintaining this skill

Anthropic's documentation changes several times a year, and new models keep being released. The procedure below keeps the skill up to date. All scripts need only Python 3.9 or later, with no extra libraries.

## A. Anthropic updates an existing document

1. Re-download and convert all references:

   ```bash
   python3 scripts/update_references.py
   ```

   The script fetches the Markdown version of each page (page URL + `.md`), converts site components to GitHub format, re-inserts every `[LOCAL NOTE]`, and writes a header with today's date.

2. If the script stops with a message like "heading ... found 0 times", Anthropic has renamed a section that carries a note. Open `scripts/local_notes.json`, update `heading` to the new title, and run it again. Also check whether the note's content is still correct.

3. Review the changes with `git diff`. Pay particular attention to:
   - new sections that mention older models and need a `[LOCAL NOTE]`;
   - older sections that carry a note but have since been updated by Anthropic, so the note should be removed;
   - changes to the effort recommendations in the model guides.

4. Re-test (see section D), rebuild the zip, and update `CHANGELOG.md`.

## B. Anthropic releases a new model

1. Add the new model's guide page to the `PAGES` list in `scripts/update_references.py`, then run the script.
2. Update the table in section 1 of `SKILL.md` (model name, guide, parent). That table is the only place the model list is written. The output checker also reads the model list from it.
3. Update the `references/` contents table in section 2 of `SKILL.md`, the `description` in the frontmatter, and the README.
4. If an older model is no longer supported, remove it from the table and from `PAGES`, then delete its reference file.
5. Review all `[LOCAL NOTE]` insertions again: cross-references to model guides may need to be added.

## C. Changing or adding a `[LOCAL NOTE]`

Do not edit the files in `references/` by hand, because the changes are lost the next time the script runs. Edit `scripts/local_notes.json`, then run `python3 scripts/update_references.py`. Each note consists of a file name, a section heading written exactly as in the document, and the note paragraphs.

## D. Testing and releasing

1. Run the test cases in `evals/README.md` against the new skill version, at least the cases marked required.
2. Check the outputs and examples:

   ```bash
   python3 scripts/check_output.py examples/*.md
   ```

3. If the skill's behavior changed, update the examples in `examples/` by running the skill again.
4. Build the zip, then commit:

   ```bash
   python3 scripts/build_zip.py
   ```

5. Record the changes in `CHANGELOG.md` and bump the version.
