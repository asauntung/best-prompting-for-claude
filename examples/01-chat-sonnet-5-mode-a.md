# Example 1: Chat, Sonnet 5, Mode A (describing a need)

## User request

> /best-prompting I'm a high school Biology teacher. Please write instructions for a Project on claude.ai so Claude helps me create 10 multiple-choice questions from the chapter material I paste, complete with an answer key and short explanations. Model Sonnet 5.

## Skill output

### Analysis

This is a Mode A request: you are describing a need and have not brought a prompt yet. I conclude the ecosystem is **Chat**, because you mention Project instructions on claude.ai. Project instructions apply to every conversation in that Project, so their role is equivalent to a system prompt in the references. This equivalence is an **[Inference]**: the references are written for API developers and do not mention Projects. The Sonnet 5 guide also has no chat-specific section, so what applies is Sonnet 5's general behavior plus the general and topical techniques.

There are a few things you did not mention, and I decided them myself because none of them changes the prompt fundamentally. First, the questions use five options, A through E, following common practice in high school exams **[Inference]**. Second, questions 1 to 10 are shown first without the key, and the key and explanations are collected in a separate section below, so the question section can be copied straight for students **[Inference]**. Third, the cognitive level of the questions is mixed, not all recall. Grade and curriculum are left as a placeholder, `[ENTER GRADE AND CURRICULUM]`, which you fill in only once. You can change any of these assumptions directly in the prompt text.

**1. Sonnet 5 reads instructions literally, so the scope must be written explicitly.** According to `prompting-claude-sonnet-5.md > More literal instruction following`: "Claude Sonnet 5 interprets prompts literally and explicitly, particularly at lower effort levels. It does not silently generalize an instruction from one item to another, and it does not infer requests you didn't make." That is why the prompt states that the key and explanation are required for all ten questions, not just some, and that the question rules apply to every question. Things a teacher usually considers "obvious", such as exactly one correct answer and plausible distractors, are also spelled out.

**2. The reasons behind instructions help Claude aim the result.** According to `prompting-best-practices.md > Add context to improve performance`: "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses." So the prompt opens with who you are, who the questions are for, and what they are used for. Important rules also come with their reasons, for example why questions may only test the content of the material and why formulas are written without LaTeX.

**3. Questions must be grounded in the material you paste, and Claude may say the material is insufficient.** According to `reduce-hallucinations.md > Advanced techniques`, under External knowledge restriction: "Explicitly instruct Claude to only use information from provided documents and not its general knowledge." According to `reduce-hallucinations.md > Basic hallucination minimization strategies`, under Allow Claude to say "I don't know": "Explicitly give Claude permission to admit uncertainty. This simple technique can drastically reduce false information." So the prompt limits questions, key, and explanations to the content of the material, and gives an honest way out if the material is too short for 10 good questions. Distractors may still be drawn from common student misconceptions, because distractors are supposed to be wrong. This exception is my own **[Inference]**.

**4. Explanation length needs to be set with a number.** According to `prompting-claude-sonnet-5.md > Response length and verbosity`: "Claude Sonnet 5 calibrates response length to the complexity of the task rather than defaulting to a fixed verbosity." This means the word "short" alone may be interpreted differently from question to question. The prompt sets two to three sentences per explanation, along with what they contain: why the key is correct according to the material, and why the most tempting distractor is wrong.

**5. The output format is set with a template.** According to `increase-output-consistency.md > Specify the desired output format`: "Precisely define your desired output format using JSON, XML, or custom templates so that Claude follows every output formatting element you require." The prompt includes a plain-text template for the question section and the key section. JSON or XML is not used because the result is read and copied by a teacher, not processed by a program **[Inference]**.

**6. Self-check before sending.** According to `prompting-best-practices.md > Leverage thinking & interleaved thinking capabilities`, on asking Claude to check its own answer: "This catches errors reliably, especially for coding and math." That section names Claude Opus 5 as an exception that does not need this instruction, and Sonnet 5 is not mentioned. So I treat this advice as still applying to Sonnet 5 **[Inference]**. The check criteria are made concrete: the key is correct according to the material, only one option is correct, and no question's answer leaks through another question.

**7. Chemical formulas and notation are written as plain text.** According to `prompting-best-practices.md > LaTeX output`: "Claude's latest models default to LaTeX for mathematical expressions, equations, and technical explanations." Biology questions often contain formulas such as the photosynthesis equation. You will copy the questions into Word or Google Forms, where LaTeX code does not render as formulas, so the prompt asks for plain text such as C6H12O6 **[Inference]**.

One final note. The technique of marking pasted text with tags labeled with a random ID is in the Opus 5.5 guide, not the Sonnet 5 guide, and is meant for text from other parties that may contain hidden instructions. Your material is your own teaching content, so the risk is low and you do not need to type any tags **[Inference]**.

### Effort

You did not mention effort. My suggestion is **`high`**. According to `prompting-claude-sonnet-5.md > Calibrating effort and thinking depth`, `high` is "The default. This setting balances token usage and intelligence for most use cases." Writing multiple-choice questions looks simple, but quality depends on reasoning: the key must be correct, only one option may be correct, and distractors must be plausible without also being correct. According to the same section, `low` is best used for "short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive", and the guide also warns that "on moderately complex tasks running at `low` effort there is some risk of under-thinking." The `medium` level is meant for needs that prioritize savings: "Good for cost-sensitive use cases that need to reduce token usage while trading off intelligence." For one set of 10 questions per chapter, those savings are not worth the risk of a wrong key **[Inference]**. The `xhigh` level is unnecessary, because according to that guide "Extra high effort is the recommended setting for the hardest coding and agentic use cases", and this task is neither.

Prompt adjustment for `high`: the prompt contains no "think carefully" instruction. The Sonnet 5 guide recommends raising effort rather than patching through the prompt: "If you observe shallow reasoning on complex problems, raise effort to `high` or `xhigh` rather than prompting around it." An extra sentence asking for step-by-step thinking is only recommended if effort has to stay at `low`. The guide's note about `max_tokens` headroom at `high` effort is an API setting, so it is not available and does not need to be set on claude.ai.

Remaining risk: the right prompt and effort reduce errors, but they do not eliminate them. According to `reduce-hallucinations.md > Advanced techniques`: "Remember, while these techniques significantly reduce hallucinations, they don't eliminate them entirely. Always validate critical information, especially for high-stakes decisions." Check every key before the questions are used for grading. If you later choose `medium` or `low`, ask me to rewrite the prompt for that level.

Final: Chat, Sonnet 5, high

```text
You are helping me, a high school Biology teacher, write multiple-choice questions for my students. I teach [ENTER GRADE AND CURRICULUM, for example 11th grade, NGSS]. I will use the questions you write for unit quizzes and in-class practice, so every question must be factually correct, consistent with the material I teach, and clear to high school students.

In every conversation in this Project, I will paste the text of one chapter of material. Treat all the text I paste as that chapter's material. After receiving the material, write exactly 10 multiple-choice questions from it, and include an answer key and a short explanation for all ten questions, not just some of them.

The following rules apply to every question, from question 1 to question 10:

- Questions, key, and explanations rely only on information written in the material I paste, not on your general knowledge, because students learn from this material and questions outside it are unfair to them. Distractors may be drawn from common student misconceptions, as long as the correct answer is still determined by the material.
- Spread the questions across the whole material, from the beginning to the end of the chapter.
- Mix cognitive levels: about 4 questions on remembering and understanding, 4 questions on applying concepts to new situations, and 2 questions on analysis, for example reading data, a table, or a short case that you write into the question.
- Each question has five answer options, A through E, with exactly one correct answer. Distractors should be plausible to students who have not yet understood the material, and roughly the same length as the correct answer.
- Distribute the position of the correct answer randomly among A through E.
- Write in clear standard English that high school students can easily understand. Write chemical formulas and equations as plain text, for example C6H12O6 + 6O2 yields 6CO2 + 6H2O, without LaTeX, because I will copy the questions into Word or Google Forms.

Present the result in two sections using the following format. The first section contains only the questions, so I can copy it straight for students:

QUESTIONS
1. (question text)
A. (option)
B. (option)
C. (option)
D. (option)
E. (option)

Continue in the same format through question 10. The second section contains the key and explanations for all ten questions:

ANSWER KEY AND EXPLANATIONS
1. Key: (letter). Explanation: (two to three sentences explaining why that answer is correct according to the material, and why the distractor students are most likely to choose is wrong.)

Continue in the same format through number 10. Start your answer directly with the QUESTIONS heading, without an opening sentence.

Before presenting the result, check every question: its key is correct according to the material, only one option is correct, and its answer cannot be guessed from another question. Fix any question that fails this check before presenting it.

If the material I paste is too short for 10 good questions without repeating the same concept, say so at the start of your answer, state how many questions the material can support, write that many questions, and then say which parts of the material I need to add. If any part of the material seems wrong or ambiguous to you, flag it at the end of your answer in one or two sentences, and still base the questions on the material.

If my message asks for a different number of questions, number of options, or difficulty level, follow the request in that message. If I ask for a revision of a specific question, change only that question, then show that question again with its key and explanation in the same format.
```
