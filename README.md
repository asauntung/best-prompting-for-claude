# Best Prompting for Claude

A `/best-prompting` skill that writes and fixes prompts **based on Anthropic's official documentation**, not guesswork or "viral tips". Every recommendation comes with a direct quote from the source document, so you can check the basis yourself.

## What the skill does

Invoke `/best-prompting`, then describe what you need or paste the prompt you want improved. The skill will:

1. Read all of the Anthropic documentation in `references/`.
2. Analyze your need, or diagnose the weaknesses of your existing prompt, with verbatim quotes and `file-name > section heading` references. Suggestions not grounded in the documents are labeled **[Inference]**.
3. Assess the right effort level (`low` to `max`) for your model and task.
4. Deliver one final, ready-to-copy prompt, preceded by a marker line such as `Final: Claude Code, Opus 5.5, high`.

| | Supported |
|---|---|
| Models | Claude Sonnet 5, Claude Sonnet 5.5, Claude Opus 5.5, Claude Fable 5.1 |
| Ecosystems | Chat (claude.ai and apps), Cowork, Claude Code |
| Language | Follows the language of your request (English if unclear) |

See the case studies in the [`examples/`](examples/) folder.

## Installation

**claude.ai and Cowork.** Download [`dist/best-prompting.zip`](dist/best-prompting.zip) (click the file, then the download button). On claude.ai, open **Customize > Skills**, click **+**, choose **+ Create skill**, then **Upload a skill** and select the zip. Do not rename the zip or the folder inside it: the folder name must match the skill name. An uploaded skill is also available in Cowork and can be turned on or off there. Official reference: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

**Claude Code.** If you sign in to Claude Code with the same Claude account, skills uploaded on claude.ai are loaded too (according to the help page above, this requires Claude Code v2.1.273 or later). To install manually, copy the `best-prompting/` folder into your personal skills folder:

```bash
git clone https://github.com/asauntung/best-prompting-for-claude.git
mkdir -p ~/.claude/skills
cp -r best-prompting-for-claude/best-prompting ~/.claude/skills/
```

Or copy it into `.claude/skills/` inside a project if you only want it in that project.

## Usage

Example requests:

```text
/best-prompting Write Project instructions on claude.ai that help me turn product notes into Instagram captions. Model Sonnet 5.
```

```text
/best-prompting Fix this prompt for Claude Code, Opus 5.5, effort high:
[paste your prompt]
```

Name the **model** (required) and the **ecosystem**. Effort is optional: the skill will propose one. If the model or ecosystem is unclear, the skill asks first.

## Limitations to know about

- The skill deliberately relies only on the documents in `references/`. If the documents don't cover something, the skill says so instead of making it up.
- Reading all the references (about 270 KB) costs a fair number of tokens on every invocation. That is the price of an analysis you can verify.
- Anthropic's documentation keeps changing. The retrieval date is in the header of every reference file and in [`CHANGELOG.md`](CHANGELOG.md).
- A good prompt does not replace the right choice of model and effort. The skill names the residual risk a prompt cannot cover.

## Repository contents

| Path | Contents |
|---|---|
| `best-prompting/` | The skill itself: `SKILL.md` and `references/` |
| `dist/best-prompting.zip` | Ready-to-upload skill |
| `examples/` | Case studies: sample outputs and demonstrations of the skill |
| `evals/` | Test cases and how to test the skill |
| `scripts/` | Reference updater, output checker, zip builder |
| `MAINTAINING.md` | Procedure for when Anthropic updates its documents or releases a new model |

## License and attribution

The original writing in this repo (SKILL.md, scripts, examples, evals, documentation) is licensed under [MIT](LICENSE). The files in `best-prompting/references/` and `evals/references/` are copies of Anthropic documentation and are **not** covered by the MIT license; see [`NOTICE.md`](NOTICE.md). This project is not affiliated with or endorsed by Anthropic.
