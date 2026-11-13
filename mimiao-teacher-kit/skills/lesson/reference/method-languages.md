# Method pack: foreign languages (CEFR Pre-A1 to C1)

Use for English, German, Spanish, Polish and any other language lesson, at levels Pre-A1, A1, A2, B1, B2, C1.

## Stages of a balanced lesson

| # | Stage | Share of time | Purpose | Block types |
|---|---|---|---|---|
| 1 | Warm-up with personal questions | about 10% | activate the topic, get students talking | `teacher_note` with the questions (no `short_answer` needed) |
| 2 | Text or dialogue, meaning first | about 30% | understand and enjoy the text before looking at grammar | `rich_text`, then `true_false` or `inline_choice` on the CONTENT, never on grammar |
| 3 | Noticing and rule | about 15% | students discover the pattern, then see it summarised | `hint` with a guiding question, then `rich_text` with a table |
| 4 | Controlled grammar practice, at most 10 items | about 20% | automate the form | `inline_choice`, `fill_blanks`, `word_transform`, `sentence_builder` |
| 5 | Vocabulary in context | about 15% | fix the new words | `matching`, `categorization`, `cards` |
| 6 | Free production | about 10% | use the language for real | speaking or writing task described in `rich_text`, plus `teacher_note` with model answers |

The recap section of the lesson is stage 6 plus one short check (`true_false` or `short_answer`).

## Rules
- Meaning before form: students read or hear the text first, the rule comes after.
- New words appear in the text before they are practised.
- Grammar gaps give the base form in brackets: `She ___ (go) to school.` Vocabulary gaps give no hint.
- No past tenses at Pre-A1 and A1. Keep sentences short at A1-A2; B1+ may use connected texts of 80-150 words.
- Dialogues have two speakers and real-life logic. A `dialogue_order` block reuses the lesson dialogue (same lines, new order).
- Translations into the students' language appear only where the teacher wants them: put them in `cards.side2` and in `matching`. Default students' language = the teacher's language.
- Instructions are in the teacher's language, the target-language examples stay in the target language.
- Accept contractions and full forms in `acceptedAnswers` (`"don't"`, `"do not"`).

## Focus variants
| Request | Change |
|---|---|
| speaking («розмовний», «більше говоріння») | production grows to 30%, grammar practice drops to 10%; add role-play prompts in `rich_text` and `teacher_note` |
| grammar («граматика») | rule + practice grow to 50% together; more `word_transform` and `sentence_builder` |
| vocabulary («лексика») | stage 5 grows to 35%; add a second `categorization` and a `cards` set of 8-10 words |
| no grammar («без граматики») | drop stages 3 and 4 entirely; give their time to text work and vocabulary |
| exam prep | follow the exam format of the request; use `inline_choice` for multiple choice and `word_transform` for transformation tasks |

## Scale
A 45-minute lesson: about 9-11 practice blocks, 3 of them in stage 4 or 5, at least five practice types. Shorter or longer lessons keep the same shares of time.

## Quick checks for a language lesson
- The text in stage 2 is original, at the stated level, and long enough to carry the target structure at least three times.
- Every target word of stage 5 occurs in the stage 2 text.
