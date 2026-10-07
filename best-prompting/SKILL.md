---
name: best-prompting
description: Writes new prompts or improves existing ones for Claude in chat (claude.ai), Cowork, or Claude Code, for the models Claude Sonnet 5, Sonnet 5.5, Opus 5.5, and Fable 5.1 only, using the official Anthropic documents in references/ as the sole ground truth. Use whenever the user invokes /best-prompting, asks for a prompt or system prompt for Claude, or pastes a prompt to be improved. Not for image or video generation prompts (Nano Banana, Midjourney, and the like), and not for non-Claude models.
---

# /best-prompting

This skill produces one best prompt for the user's need, preceded by an analysis that explains why that prompt, model, and effort are proposed. All analysis is grounded in the official Anthropic documentation in the `references/` folder.

## 1. Supported models

This table is the only place the model list is written. When Anthropic releases a new model, update this table and the contents of `references/`.

| Name in the Final line | Model guide | Parent guide |
|---|---|---|
| `Sonnet 5` | `prompting-claude-sonnet-5.md` | none |
| `Sonnet 5.5` | `prompting-claude-sonnet-5-5.md` | `prompting-claude-sonnet-5.md` |
| `Opus 5.5` | `prompting-claude-opus-5-5.md` | `prompting-claude-opus-5.md` |
| `Fable 5.1` | `prompting-claude-fable-5-1.md` | `prompting-claude-fable-5.md` |

Parent models exist because the newer model guides only cover what differs from the previous model, and state that prompts for the parent model still apply. If the user names a model outside the table, say that this skill only serves the models in the table, then ask which model they mean.

## 2. Single ground truth

The only knowledge source for this skill is the full set of files in `references/`. They are copies of the official Anthropic documentation, with insertions labeled `[LOCAL NOTE]` from the skill maintainer.

Reading rules:

- Every time the skill is invoked, read ALL files in `references/` to the end, whatever their names, including files added later. These files are long: read them in chunks with an offset until the last line, and do not stop halfway. The only exception: code blocks that a `[LOCAL NOTE]` declares to be API code samples may be skimmed. Reading everything does not mean using everything: what goes into the prompt is governed by section 7.
- Do not summarize or paraphrase the references as the basis for analysis. Quote verbatim, in the original language, and build the analysis from the quote.
- `[LOCAL NOTE]` insertions must be obeyed. They mark sections that are outdated, specific to older models, or only applicable through the API. Never suggest prefill: the technique returns a 400 error on every model in the table.
- The `[LOCAL NOTE]` block at the top of each file only records the source and retrieval date. It is not prompting advice.
- Knowledge outside `references/` is not a source. If a suggestion is not written in the references and is Claude's own reasoning, label it **[Inference]** and explain its basis. If the references do not cover something, say so plainly.

Contents of `references/`:

| File | Role |
|---|---|
| `prompting-claude-sonnet-5.md` | Model guide: Sonnet 5, also parent of Sonnet 5.5 |
| `prompting-claude-sonnet-5-5.md` | Model guide: Sonnet 5.5 |
| `prompting-claude-opus-5-5.md` | Model guide: Opus 5.5 |
| `prompting-claude-opus-5.md` | Parent of Opus 5.5 |
| `prompting-claude-fable-5-1.md` | Model guide: Fable 5.1 |
| `prompting-claude-fable-5.md` | Parent of Fable 5.1 |
| `prompting-best-practices.md` | General foundation for all models |
| `reduce-hallucinations.md` | Thematic: accuracy, citations, permission to say "I don't know" |
| `increase-output-consistency.md` | Thematic: output format consistency |
| `mitigate-jailbreaks-and-prompt-injections.md` | Thematic: third-party content and injection |
| `reduce-prompt-leak.md` | Thematic: prompt leakage |

## 3. Priority order when references conflict

1. The target model guide.
2. Its parent guide (see the table in section 1).
3. `prompting-best-practices.md`.
4. Thematic files.

The model guide always wins for the model it targets. Sections of `prompting-best-practices.md` that a `[LOCAL NOTE]` marks as specific to previous-generation models are treated as indicative only and must be cross-checked against the target model guide.

## 4. Step 0: check the parameters before working

The skill needs three parameters: ecosystem, model, and effort.

- **Model** MUST be named by the user. If it is not, ask first (use AskUserQuestion if available) and stop until it is answered. Do not guess.
- **Ecosystem** (Chat, Cowork, or Claude Code) may be inferred when the context is unambiguous, for example when the user writes "for my Project system prompt on claude.ai" or "for CLAUDE.md". State that inference in the analysis. If the context is not unambiguous, ask together with the model question, in a single round of questions.
- **Effort** may be left unstated. Recognized levels: `low`, `medium`, `high`, `xhigh`, `max`. "Extra", "xHigh", or "extra high" mean `xhigh`.

## 5. Identify the request mode

- **Mode A, the user describes a need.** Understand the goal, materials, audience, and desired result. If two readings of the need would produce materially different prompts, ask about that one thing only. Otherwise decide yourself and state the assumptions in the analysis.
- **Mode B, the user pastes a weak prompt.** Diagnose its weaknesses one by one with reference to the documents. Weaknesses can be gaps (ambiguous instructions, missing context or reasons, unmarked pasted material, unclear output format, missing constraints, outdated techniques) or excess (rules written repeatedly, case lists that one short instruction could replace, a reason attached to every sentence, instructions for behavior the model already has by default, reference snippets for symptoms that are not present). Removing is a legitimate fix: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." (`prompting-claude-fable-5.md > Recommended scaffolding changes`). Keep the user's original intent. Fix the method, not the goal.

## 6. Map the ecosystem to the kinds of work in the references

The references are written for API developers and discuss kinds of work, rarely product names. Map as follows, and look for relevant sections in ALL files:

- **Chat**: conversations in claude.ai or the Claude apps, including Project instructions. The references name it explicitly, for example "Thinking instructions in chat system prompts" and "Mark pasted text in user messages" in the Opus 5.5 guide, "Formatting in chat" in the Fable 5.1 guide, and "Tool use in chat and knowledge work" in the Sonnet 5.5 guide.
- **Claude Code**: agentic work on files and folders, including non-coding work (research, text processing, data mining). The references mention Claude Code in `prompting-best-practices.md` (the context awareness and multiwindow workflows sections) and in `prompting-claude-opus-5.md > Controlling subagent spawning`, and cover agentic work at length in the "Agentic systems" section and in each model guide.
- **Cowork**: this name does not appear in the references. Mapping it to cross-application agentic work, unattended work, research, and processing third-party content is an **[Inference]** and must be labeled as such in the analysis. Relevant sections include "Explore context in multi-app workflows" and "Unattended agentic runs" in the Opus 5.5 guide, the research and autonomy sections of `prompting-best-practices.md`, and the indirect prompt injection section of `mitigate-jailbreaks-and-prompt-injections.md`.

API mechanics (`max_tokens`, harness code, turn-scoped system messages, caching, thinking blocks, request parameters) cannot be controlled by the user from a prompt. Do not put them in the prompt. Translate them only into what the user can control, namely model choice, effort, and prompt content. If a reference recommendation can only be applied through the API, mention briefly in the analysis that it is not available in the user's ecosystem.

Match the user's technical level. By default, do not produce prompts that require the user to write or understand code, unless they ask for it or are clearly a developer.

## 7. Be concise: every sentence must change behavior

A good prompt contains everything the task needs and nothing more. These rules apply to Mode A and Mode B:

- **Use reference snippets only when the symptom is present.** The Opus 5.5 and Fable 5.1 guides are organized by symptom: "Start with the section that matches what you observe" (`prompting-claude-opus-5-5.md > Prompting Claude Opus 5.5`, also in `prompting-claude-fable-5-1.md`). Include a snippet only if the user reports the symptom or the nature of the task clearly triggers it. When the reference offers a short version, use it, for example "If you need to limit prompt length, use only the first, which keeps most of the effect." (`prompting-claude-fable-5-1.md > Finish the whole task`).
- **One short instruction, not a list of cases.** "Instruction-following is improved enough that you can steer most behaviors with a brief instruction rather than enumerating each behavior by name." (`prompting-claude-fable-5.md > Strong instruction following`). Do not enumerate every way the model could fail. For target models other than Fable 5.1, the analysis notes that this quote comes from another model's guide.
- **Give the reason once, up front.** One paragraph on the purpose of the task and who the result is for (`prompting-claude-fable-5.md > Give the reason, not only the request`). Later rules do not each get their own "because" clause, unless the reason cannot be inferred from that paragraph.
- **Each rule is written once, in one place.** No summary section, checklist, or acceptance criteria that repeat the prompt. Examples demonstrate rules, they do not restate them.
- **Do not write behavior the target model already has by default.** For example, verification instructions for Opus: "Claude Opus 5 verifies its own work without being told to." (`prompting-claude-opus-5.md > Task scope and over-verification`). Write only what needs to change from the default behavior.
- **Coin terms sparingly.** A special term is defined once and then used consistently. Do not coin terms for things that ordinary words can name.
- **Condensing means removing, not rephrasing.** When shortening a prompt, sentences that act as criteria or limits (pass conditions, prohibitions, required formats) are copied exactly. Only second and later copies, and sentences that do not change behavior, are removed. Changing one word in a criterion can change the model's behavior.

Final test for every sentence of the prompt: if this sentence were deleted, would the model's behavior change? If not, delete it.

Rules in this section that carry no quote are the skill maintainer's inference. When used as a basis in the analysis, label them **[Inference]**.

## 8. Assess effort, always

- If effort is not stated, propose the best effort according to the references for that model, ecosystem, and task, and explain why with quotes.
- If effort is stated and the references support it, confirm briefly with the reason.
- If effort is stated but the references suggest it is a poor fit, explain why and propose a better level. The decision stays with the user.
- Defaults and the meaning of each level differ between models. Take the figures and statements directly from the effort section of each model guide, not from memory.
- For the effort used in the final prompt, apply the effort-specific adjustments the references provide when the symptom is relevant to the task (for example additions for low effort or notes on long outputs at high effort), following the rules of section 7, and state the residual risk that a prompt cannot cover. The references repeatedly describe effort as the main lever, so the prompt must never be promised as a full substitute for the right effort.
- The prompt in the first answer is written for the effort the skill PROPOSES, and the Final line carries that proposed effort. If the user then chooses a different effort, rewrite the prompt adjusted for their choice, with a Final line that reflects it, along with an explanation of the adjustments and the residual risk.

## 9. Language

- The analysis is written in the language the user used for the request. If it cannot be determined, use English.
- The generated prompt is written in the same language, unless the user asks for another.
- Quotes from the references stay in their original English, verbatim.
- If an official prompt snippet from the references is used inside a prompt written in another language, translate it faithfully, and show the original English text in the analysis so the user can compare.
- Technical terms, file names, and proper names stay in their original form.

## 10. Writing style

Applies to the analysis and to the prompt content the skill writes:

- Do not use em-dashes. Use commas, periods, or colons.
- Do not open with warm-up formulas such as "Imagine", "Have you ever", or "In today's digital age". Go straight to the substance.
- Write in full sentences and flowing paragraphs. Use bullet lists only for items that are genuinely parallel.

## 11. Output format, mandatory and in order

The output consists of four parts, in this order, with nothing after the codeblock:

**Part 1: Analysis.** Explain why this prompt is proposed: the need or the diagnosis of the old prompt, relevant behavior of the target model, ecosystem needs, and the techniques chosen. Every claim sourced from the references comes with a verbatim quote and a reference in the form `file-name > section heading`. One strongest quote per claim is enough, and focus the analysis on claims that actually change the prompt's content, usually no more than seven. Clearly separate what is quoted from the source and what is inferred. Suggestions without a basis in the references are labeled **[Inference]**. Close the analysis with the word count of the final prompt. In Mode B, compare it with the word count of the old prompt, and if the new prompt is longer, name the gaps that make it need to be longer.

**Part 2: Effort.** The proposed effort and its reasons, an assessment of the effort the user stated (if any), the prompt adjustments for that effort, and the residual risk.

**Part 3: Final line.** Immediately before the codeblock, write one line in exactly this format:

`Final: <Ecosystem>, <Model>, <effort>`

Example: `Final: Claude Code, Opus 5.5, xhigh`. Ecosystem spelling: `Chat`, `Cowork`, or `Claude Code`. Model spelling follows the first column of the table in section 1. This line is mandatory and must match the prompt below it, so the user is never unsure which ecosystem, model, and effort the prompt is for.

**Part 4: Prompt.** One codeblock of type `text` containing the final prompt, ready to copy. NO hard wraps: write each paragraph as one long line, do not break it with newlines mid-sentence. Blank lines between paragraphs are fine. Placeholders for material the user must fill in are written clearly, for example `[PASTE TEXT HERE]`, and if pasted material is wrapped in XML tags, use descriptive tags.

Do not write anything after the codeblock.

## 12. Checks before sending

- All files in `references/` have been read to the end.
- No technique marked outdated by a `[LOCAL NOTE]` is used, including prefill.
- Every sourced claim has a verbatim quote and a file > section reference. Every inference is labeled.
- The target model guide's recommendations are not overridden by the general guide.
- The Final line is immediately before the codeblock and matches the prompt.
- The prompt has no hard wraps, no em-dashes, and no API mechanics.
- The prompt passes section 7: each rule appears once, no reference snippets for absent symptoms, and every sentence changes the model's behavior.
