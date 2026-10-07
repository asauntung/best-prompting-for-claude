# Test cases

Each case contains an input to send as is, the expected behavior, and the pass criteria.

## Parameters and scope

### K01 [required] Model not named

Input:
```text
/best-prompting Write a prompt that summarizes the minutes of my office's weekly meeting.
```
Expected: the skill asks which model (and which ecosystem, in the same question), then stops.
Pass if: there is no analysis or prompt before the user answers, and the questions are asked in a single round.

### K02 [required] Model out of scope

Input:
```text
/best-prompting Write a prompt for Claude Haiku 4.5 in chat, to translate emails into Spanish.
```
Expected: the skill states that it only serves the models in the table in section 1 of `SKILL.md` (Sonnet 5, Sonnet 5.5, Opus 5.5, Fable 5.1), then asks which model is meant.
Pass if: no prompt is produced for Haiku 4.5.

### K03 Ecosystem can be inferred

Input:
```text
/best-prompting Please write the contents of CLAUDE.md for my thesis repo so Claude always uses APA citation style and never changes the data/ folder. Model Sonnet 5.
```
Expected: the ecosystem is inferred as Claude Code without asking, and the inference is stated in the analysis.
Pass if: the Final line reads `Final: Claude Code, Sonnet 5, <effort>` and the analysis states the basis for the inference.

### K04 Not for image prompts

Input:
```text
Write a Nano Banana prompt for an illustration of a cup of coffee on a wooden table.
```
Expected: the /best-prompting skill does not trigger (or, if invoked explicitly, states that it is not for image prompts).
Pass if: there is no output in this skill's format.

## Effort

### K05 [required] Effort not stated

Input:
```text
/best-prompting Write a prompt for Claude Code, model Fable 5.1, to turn 200 sales CSV files into one monthly summary report.
```
Expected: the skill proposes an effort with quotes from the effort section of `prompting-claude-fable-5-1.md`.
Pass if: the Effort part contains a verbatim quote from the Fable 5.1 guide and the Final line carries that proposed effort.

### K06 User's effort is a poor fit

Input:
```text
/best-prompting Prompt for Cowork, Opus 5.5, effort low: in-depth research of 20 journal articles on organic fertilizer, then write a 10-page literature review.
```
Expected: the skill assesses `low` for this long research task based on the effort sections of the Opus 5.5 guide and its parent, not from memory. The references name `medium` as the Opus 5.5 default and say `low` "comes close" on some coding evaluations, so the conclusion must be built from quotes, not from an assumption that low effort is always bad.
Pass if: the effort assessment comes with a verbatim quote from `prompting-claude-opus-5-5.md > Calibrate effort` or its parent guide; if the skill proposes another level, the Final line uses that proposed level and the skill makes clear the decision stays with the user.

### K07 [required] User rejects the effort proposal (continues K06)

Run only if in K06 the skill proposed a level other than `low`.

Input (in the same conversation, after K06):
```text
I still want low because my quota is limited.
```
Expected: the prompt is rewritten for `low`, with the low-effort adjustments from the references and the residual risk.
Pass if: the Final line reads `Final: Cowork, Opus 5.5, low` and the analysis names the adjustments and the residual risk.

## Mode B and outdated techniques

### K08 [required] Old prompt uses prefill

Input:
```text
/best-prompting Fix this prompt for chat, Sonnet 5:

Answer in JSON format. Assistant: {"result": 
```
Expected: the skill diagnoses prefill as a technique that no longer works, citing the `[LOCAL NOTE]` and `prompting-best-practices.md > Migrating away from prefilled responses`, then uses a replacement that works in chat.
Pass if: the final prompt contains no prefill, and the diagnosis comes with references.

### K09 All-caps, urgent-tone prompt

Input:
```text
/best-prompting Fix for Claude Code, Opus 5.5: YOU MUST ALWAYS USE THE SEARCH TOOL. MANDATORY!!! NEVER FORGET.
```
Expected: the skill diagnoses the high-intensity language with references, keeps the intent (using search), and gives a reason instead of a harsh command.
Pass if: the original intent is preserved, and the diagnosis has quotes. If it quotes a section that carries a `[LOCAL NOTE]` specific to older models, the analysis says so.

## Ecosystem and inference

### K10 [required] [Inference] label for Cowork

Input:
```text
/best-prompting Prompt for Cowork, Fable 5.1, effort high: read all client emails from this week and build a follow-up list in a spreadsheet.
```
Expected: mapping Cowork to cross-application agentic work is labeled **[Inference]**, and the prompt injection risk from email content is discussed with a reference to `mitigate-jailbreaks-and-prompt-injections.md`.
Pass if: both are present.

### K11 Developer user asks about API mechanics

Input:
```text
/best-prompting I use Claude in chat, Opus 5.5. What max_tokens should I put in my prompt so the answers are long?
```
Expected: the skill explains that `max_tokens` is an API parameter that cannot be set from a prompt in chat, then offers an approach the user can control.
Pass if: the final prompt does not contain `max_tokens`.

## Language

### K12 Non-English user

Input:
```text
/best-prompting Buatkan system prompt untuk Project chat layanan pelanggan di claude.ai. Model: Sonnet 5.
```
Expected: the analysis and prompt are in Indonesian, the language of the request, and quotes stay verbatim in English.
Pass if: the whole output is in Indonesian apart from the quotes, and the four-part format stays intact.

## Derived models

### K13 [required] Sonnet 5.5 uses its own guide, with Sonnet 5 as parent

Input:
```text
/best-prompting Write Project instructions on claude.ai for an assistant that answers my team's questions about raw material import regulations. Model Sonnet 5.5.
```
Expected: effort is proposed from `prompting-claude-sonnet-5-5.md > Calibrate effort`, not from the effort section of the Sonnet 5 guide, because the references say the Sonnet 5.5 effort levels have been recalibrated. Because the answers depend on regulations that can change, the analysis also cites `prompting-claude-sonnet-5-5.md > Tool use in chat and knowledge work`.
Pass if: the Final line reads `Final: Chat, Sonnet 5.5, <effort>`, the effort assessment quotes the Sonnet 5.5 guide, and every recommendation taken from the Sonnet 5 guide is consistent with the Sonnet 5.5 guide.
