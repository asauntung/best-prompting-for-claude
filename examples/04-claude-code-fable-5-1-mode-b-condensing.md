# Example 4: Claude Code, Fable 5.1, Mode B (condensing a bloated prompt)

## User request

/best-prompting Improve this prompt for Claude Code, Fable 5.1, effort high. I'll start it and walk away.

```text
You are a highly meticulous qualitative research assistant. Your task is to read 30 farmer interview transcripts in the transcripts/ folder and build a findings table in results/findings.md. This is very important because this table will be used for my research report, and if there are any mistakes, my supervisor could reject my report.

QUOTE RULES: Every finding MUST include a direct quote from the transcript. Quotes must be copied exactly, because my supervisor will check them against the original transcripts. NEVER make up a quote. If no quote supports it, don't write the finding, because a finding without a quote is useless to me.

THEME RULES: Group the findings into themes. The themes must emerge from the data, not from your head, because this is inductive research. Don't force themes. If a finding fits two themes, pick the one it fits best, because each finding may appear only once.

FORMAT RULES: The table has the columns Theme | Finding | Quote | Respondent code | Line. Line numbers must be correct because my supervisor will check.

HOW TO WORK: Read all the transcripts one by one. Don't skip a single transcript, because every respondent matters. Call tools in parallel so it's faster. Don't rewrite the whole file for small changes. Don't report anything to me until everything is done; hold all findings for the final report.

DON'T STOP BEFORE YOU'RE DONE. I've seen you stop in these ways: (1) writing a summary and then saying "next I'll..." without doing it, (2) asking "want me to continue?", (3) giving a list of questions when none were needed, (4) stopping when you felt the conversation had gotten long. I don't want any of these. Keep working until you're done.

REMEMBER: quotes must be exact and never made up. Each finding only once. Line numbers must be correct.

DONE CRITERIA:
1. All 30 transcripts have been read.
2. Every finding has an exact quote.
3. No made-up quotes.
4. No duplicate findings.
5. Line numbers are correct.
6. The table is saved in results/findings.md.
```

## Skill output

### Analysis

All parameters are given: the Claude Code ecosystem, the Fable 5.1 model, `high` effort. This is Mode B. The original intent is kept: a findings table from 30 transcripts, exact quotes with line numbers, inductive themes, no duplicate findings, and working through to the end without supervision. The old prompt's problem is not that it lacks something but that it has too much, so the fix is mostly cutting. The references support that move: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." (`prompting-claude-fable-5.md > Recommended scaffolding changes`). The parent Fable 5 guide applies because the Fable 5.1 guide states: "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes" (`prompting-claude-fable-5-1.md > Prompting Claude Fable 5.1`).

Diagnosis of the old prompt:

**1. The same rule is written three times.** "Quotes must be exact" appears in QUOTE RULES, in REMEMBER, and in DONE CRITERIA. "Each finding only once" and "line numbers must be correct" also each appear three times. DONE CRITERIA as a whole repeats the rest of the prompt. **[Inference]** Repetition doesn't add compliance; it only makes the prompt longer. In the new prompt each rule is written once, and the criteria sentences are copied from the old prompt rather than reworded. The only thing changed is the capitalization.

**2. A reason is attached to almost every sentence.** There are seven "because" clauses, and nearly all of them come down to one thing: the supervisor will check the table against the transcripts. The references recommend giving the purpose as context, once is enough: "Claude Fable 5 tends to perform better when it understands the intent behind a request: context lets it connect the task to relevant information rather than inferring intent on its own." (`prompting-claude-fable-5.md > Give the reason, not only the request`). The new prompt opens with one paragraph of context. The only "because" kept is "because this is inductive research", since that reason can't be guessed from the opening paragraph.

**3. Four ways of stopping are spelled out one by one, in capital letters.** The references state that a short instruction is enough: "Instruction-following is improved enough that you can steer most behaviors with a brief instruction rather than enumerating each behavior by name." (`prompting-claude-fable-5.md > Strong instruction following`). Because this prompt runs unattended, the new prompt uses a short version of the official block. The references themselves provide that shortcut: "If you need to limit prompt length, use only the first, which keeps most of the effect." (`prompting-claude-fable-5-1.md > Finish the whole task`). From that first block, the opening sentence and the final-check paragraph are used. The opening sentence is kept because "The opening sentence, which tells the model the user isn't watching, carries much of the effect. Keep it as written." (same section). The original text used: "You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work." and "Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls." The rest of that block is not used. **[Inference]** The exception paragraph doesn't apply because the user is requesting work, not describing a problem; the sentence about long context is left out because this task doesn't risk exhausting the context; and the paragraph about commands that change system state is irrelevant to a task that only reads files and writes one.

**4. "Don't report anything until everything is done" has to go.** The references name lines like this specifically: "Some earlier models were eager to give updates while working, which led to system prompt lines such as "hold all findings for the final response." Remove lines like that before adding anything." (`prompting-claude-fable-5-1.md > Ask for user-facing progress updates`). That sentence is deleted, and no progress-update instruction is added in its place, because the user hasn't reported any problem with progress updates.

**5. Instructions for symptoms that aren't there.** "Call tools in parallel" and "Don't rewrite the whole file" are remedies for two symptoms in the Fable 5.1 guide's list, namely "One tool call per turn in agent loops" and "Whole files rewritten for small changes". That guide is organized by symptom: "Start with the section that matches what you observe" (`prompting-claude-fable-5-1.md > Prompting Claude Fable 5.1`). The user hasn't reported either symptom, and this task only writes one new file, so both sentences are deleted.

**6. One real check replaces three reminders.** The biggest risk in this task is a quote or line number that is off. Saying "must be exact" three times doesn't close that risk, but a separate check can: "Separate, fresh-context verifier subagents tend to outperform self-critique." (`prompting-claude-fable-5.md > Recommended scaffolding changes`). The new prompt includes one sentence asking a fresh-context subagent to check the quotes against the transcripts.

**7. The final report is given content.** The old prompt mentions a "final report" without saying what goes in it. One sentence follows the advice "Lead with the outcome." (`prompting-claude-fable-5.md > Strong instruction following`), with content specific to this task.

The role "highly meticulous qualitative research assistant" is removed. **[Inference]** The meticulousness it aims for is already expressed through the quote requirements and the subagent check, so the role doesn't change behavior.

Prompt length: the old prompt is 342 words, the new prompt is 255 words.

### Effort

The `high` effort you chose is right. It's the Fable 5.1 default and the recommended starting point: "Start at the default effort level, `high`, then test the other levels (`low`, `medium`, `xhigh`, and `max`) against your own evals." (`prompting-claude-fable-5-1.md > Consider all effort levels`). Accuracy of quotes and line numbers across 30 transcripts is the kind of work that benefits from high effort. The references provide no specific prompt addition for `high`, so nothing is added.

Remaining risk: "On routine work at higher effort, Claude Fable 5 can gather context and deliberate beyond what the task needs." (`prompting-claude-fable-5.md > Consider all effort levels`). If the result is clean but slow, try `medium` on a few transcripts and compare. No prompt guarantees zero misquoted lines, so still review the list of quotes the checker corrected in the final report.

Final: Claude Code, Fable 5.1, high

```text
I'm writing a qualitative research report on farmers' experiences, and my supervisor will check every quote in this table against the original transcripts.

Read all 30 interview transcripts in the transcripts/ folder, then build a findings table in results/findings.md with the columns Theme | Finding | Quote | Respondent code | Line.

Every finding must include a direct quote from the transcript. Quotes must be copied exactly, along with their line numbers. If no quote supports it, don't write the finding. The themes must emerge from the data, not from your head, because this is inductive research. If a finding fits two themes, pick the one it fits best; each finding may appear only once.

Before finishing, ask one fresh-context subagent to check every quote and line number against its transcript file, then fix any that don't match.

You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. Stop only when the table covers all 30 transcripts, or when something comes up that only I can decide.

When you're done, open your report with the outcome: the number of transcripts read, the number of themes and findings, then the quotes the checker corrected.
```
