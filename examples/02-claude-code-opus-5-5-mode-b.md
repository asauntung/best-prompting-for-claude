# Example 2: Claude Code, Opus 5.5, Mode B (fixing a prompt)

## User request

/best-prompting Fix this prompt of mine for Claude Code, model Opus 5.5, effort max:

```text
IMPORTANT!!! You are a professional editor. Tidy up ALL the markdown files in the notes/ folder, fix typos and spelling, make the heading format consistent. DON'T MISS ANYTHING. Do it as fast as possible.
```

## Skill output

### Analysis

Parameters are complete: ecosystem Claude Code, model Opus 5.5, effort `max`. This is Mode B, so the original intent is kept (tidying up all Markdown files in `notes/`, fixing typos and spelling, making the heading format consistent, with nothing missed) and what gets fixed is how it is communicated. This task is file-and-folder agentic work, so the relevant reference sections are the agentic work parts of the Opus 5.5 guide, its parent guide, and `prompting-best-practices.md`. The Opus 5 parent guide is also used because the Opus 5.5 guide itself states: "Existing Claude Opus 5 prompts should perform well without changes" (`prompting-claude-opus-5-5.md > Prompting Claude Opus 5.5`).

Diagnosis of the old prompt, point by point:

**1. Emphasis with capital letters and exclamation marks, without reasons.** "IMPORTANT!!!" and "DON'T MISS ANYTHING" add pressure but do not tell Claude why the task matters or what the notes are used for. The references recommend reasons, not volume: "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses." (`prompting-best-practices.md > Add context to improve performance`). So in the new prompt the capitals are replaced with ordinary sentences, and there is one spot (a placeholder) to explain what the notes are for. The reference's advice to soften aggressive language such as "CRITICAL: You MUST" is in a section that the `[LOCAL NOTE]` marks as specific to Claude Opus 4.5 and 4.6 (`prompting-best-practices.md > Tool usage`), so it is not used as a basis here.

**2. Ambiguous instructions.** "Tidy up" could mean anything, from fixing spelling to rewriting paragraphs. "Make the heading format consistent" does not say which format. "The notes/ folder" does not say whether subfolders are included. A test from the references: "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." (`prompting-best-practices.md > Be clear and direct`). A colleague reading the old prompt would certainly ask which heading format to use. The new prompt defines "tidy up" as two things only (spelling and heading format), asks Claude to determine the heading convention from the dominant pattern in the folder and state it before editing, and includes subfolders. The assumption that subfolders count is my reading of the word "ALL"; if not, delete that phrase in step 1.

**3. Missing scope limits.** Opus 5, the parent of Opus 5.5, tends to expand tasks: "Claude Opus 5 can also expand the scope of a task, adding steps that weren't requested or applying its own judgment about what the task should be. For narrow tasks, constrain scope explicitly" (`prompting-claude-opus-5.md > Task scope and over-verification`). Editing personal notes is a narrow task, and the words "Tidy up" combined with the "professional editor" role invite stylistic rewriting. The new prompt states explicitly what must not be touched (content, structure, code blocks, links, front matter, proper names) and includes two sentences taken word for word from the example prompt in the same reference section: "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work."

**4. "Don't miss anything" without a way to make sure.** Completeness is better guaranteed by a clear work order than by capital letters: "Provide instructions as sequential steps using numbered lists or bullet points when the order or completeness of steps matters." (`prompting-best-practices.md > Be clear and direct`). The new prompt uses numbered steps that begin by listing every file in a to-do list and then checking them off one by one. **[Inference]** This to-do list was chosen because completeness in a many-file task is a matter of record-keeping, not of thinking harder; Claude Code has a built-in to-do list, so this instruction does not require the user to set anything up.

**5. No "double-check" instruction needed.** The natural temptation with "DON'T MISS ANYTHING" is to add "check all the files again before finishing". The parent reference advises the opposite: "Claude Opus 5 verifies its own work without being told to." (`prompting-claude-opus-5.md > Task scope and over-verification`). So the new prompt contains no re-verification step; the stopping condition is simply "every file on the list is marked done".

**6. Doubtful typos.** Personal notes usually contain people's names, personal abbreviations, regional terms, or foreign terms that look like typos but are intentional. The references recommend giving permission to be unsure: "Explicitly give Claude permission to admit uncertainty. This simple technique can drastically reduce false information." (`reduce-hallucinations.md > Basic hallucination minimization strategies`). The new prompt asks Claude to leave doubtful cases as they are and note them in the report, instead of guessing.

**7. A final report that was never requested.** The old prompt does not say what should be reported, even though the user needs to know which files changed and what was left alone. The parent reference gives a report shape that goes straight to the result: "When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it." (`prompting-claude-opus-5.md > User-facing progress updates`). This sentence is adapted into the prompt's final paragraph, with report contents specific to this task added.

The "professional editor" role is kept because it is part of the original intent. **[Inference]** The references discuss roles in system prompts, whereas in Claude Code this prompt is sent as a user message; there the role is still useful as a marker of the work standard, as long as its scope is limited as in point 3. The instruction "Do it as fast as possible" is removed from the prompt; the reason is discussed in the Effort section.

### Effort

Suggested effort: `medium`. The user's chosen effort, `max`, is a poor fit for this task according to the references, for three reasons.

First, the recommended starting point for Opus 5.5 is its default: "Start at `medium`, the default on Claude Opus 5.5 (Claude Opus 5 defaults to `high`), set it explicitly, and test several levels against your own evals rather than carrying over the setting you used on Claude Opus 5." (`prompting-claude-opus-5-5.md > Calibrate effort`). The highest levels are reserved for cases that have proven to need them: "Reserve `xhigh` and `max` for work where you've measured a quality gain." (same section). Fixing spelling and making headings consistent is routine work, and at `medium` this model is already strong for that kind of work: "in Anthropic's testing, Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at `high` on coding and knowledge-work evaluations" (same section).

Second, `max` conflicts with the "Do it as fast as possible" request in your own prompt: "At a given level, Claude Opus 5.5 tends to think more per turn than Claude Opus 5, especially at `xhigh` and `max`." (same section). This means `max` makes every step slower and more expensive.

Third, speed is controlled through effort, not through a sentence in the prompt: "To get less thinking, lower the effort level first. Lowering effort reduces thinking, and with it cost and latency, more reliably than prompt instructions do." (same section). That is why "Do it as fast as possible" is removed from the prompt and its intent is moved into the choice of `medium` effort.

Prompt adjustment for `medium`: the references provide no prompt additions specific to `medium` effort for Opus 5.5, so nothing is added. **[Inference]** The completeness safeguards in this prompt (the to-do list and the stopping condition) do not depend on the amount of thinking, so they still work at lower effort.

If you still choose `max`, the prompt below can be used without content changes; just change the Final line to `Final: Claude Code, Opus 5.5, max`. Accept that turns will be longer and more expensive, and the "as fast as possible" wish will not be met. The reference's advice for high levels, "Set `max_tokens` high enough to leave room for the model's thinking tokens and the reply." (same section), is API mechanics and is not available in Claude Code. If the result at `medium` turns out to miss typos that should have been caught, raise it to `high` first before `xhigh` or `max`.

Remaining risk: at any effort, the prompt cannot guarantee zero missed typos, and the references repeatedly name effort as the main lever, not prompt sentences. **[Inference]** Typos that are valid words but wrong in context (for example "form" where "from" was meant) are the most likely to slip through. Check the list of doubtful cases in the final report, and if this folder is in a git repository, review the changes with a diff before making them permanent.

Final: Claude Code, Opus 5.5, medium

```text
Act as a professional editor. Your task is to tidy up all the Markdown files in the notes/ folder, and "tidy up" here means two things only: fixing typos and spelling, and making the heading format consistent. [WRITE HERE WHAT THESE NOTES ARE USED FOR, for example "These notes will be shared with the team as reference material, so they need to be clean and consistent." Delete this sentence if not needed.]

No file may be missed, so work in the following order:

1. List every file with the .md extension inside notes/, including those in subfolders. Record them all in a to-do list, state how many there are, and update the list each time a file is finished. Do not create new files inside notes/.
2. Read the headings across all files and determine the most dominant heading convention: the type of heading marker, the order of heading levels, capitalization, and blank lines around headings. Before you start editing, write that convention in one short paragraph along with your reasoning. If there is no dominant pattern, choose the convention that best fits the structure of the notes' content and state that choice as an assumption.
3. Work through the files one by one in list order. Fix typos and spelling following the standard rules of the language each note is written in, then apply the heading convention from step 2. Mark the file as done on the list.
4. Stop only when every file on the list is marked done.

Deliver what was asked, at the scope intended. Do not rewrite sentences for style, do not change the order or structure of the content, and do not add or remove content. Do not change the contents of code blocks, inline code, URLs, links, paths, front matter, or file names. People's names, place names, technical terms, foreign terms, and direct quotations may only be changed if the typo is beyond doubt. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work.

If you are unsure whether something is a typo or intentional, for example the spelling of a name, a personal abbreviation, a regional term, or casual language, leave it as it is and note it for the report. It is better to admit uncertainty than to guess.

When you finish, lead with the outcome: your first sentence should answer "what happened", meaning how many files were checked and how many were changed. After that, state the heading convention you used, then list the things you were unsure about and left as they are, with the file name and line for each.
```
