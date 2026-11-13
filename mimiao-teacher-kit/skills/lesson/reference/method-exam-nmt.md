# Method pack: exams (НМТ/ЗНО and similar)

Use for exam preparation and exam-style tests: Ukrainian language, maths, history of Ukraine, English and optional subjects. Works for lessons, homework and tests.

## Exam item formats mapped to block types

| Exam item format | Block type | How |
|---|---|---|
| Single choice of 4-5 options | `inline_choice` | one blank, 4-5 options, `points` 1; the question is the text before `___` |
| Matching, 4 to 5 pairs («встановіть відповідність») | `matching` | pairs 1:1; `points` = number of pairs |
| Sequence («встановіть послідовність») | `dialogue_order` | phrases in the correct order; `points` = number of steps |
| Several correct statements out of seven | `categorization` | two groups «Правильно» and «Неправильно» with the seven statements split between them |
| Open short numeric or word answer | `short_answer` | one blank, every accepted variant listed, `points` 1 |

The kit pairs matching items 1:1, so there is no extra distractor column. Tell the teacher about this limitation only if they ask for extra options.

## Rules
- Follow the current official programme as far as you know it, and say in the reply line that the teacher should check the items against the current year's programme.
- Never present items as real past-paper items; call them «у форматі НМТ» or «тренувальні завдання».
- One skill per item. Group blocks by topic, each topic under its own `heading`.
- Points: 1 for single choice and short answer. The format cannot give one point per pair, so for `matching` and `dialogue_order` set `points` equal to the number of pairs or steps, at most 4.
- Default `passPercent` is 60 for exam-style tests.
- Add a `rich_text` intro stating the time allowed and how answers are entered.
- Distractors follow the rules in `writing-rules.md`: typical mistakes, same category and length.

## Sizes
| Material | Blocks |
|---|---|
| 20-minute diagnostic | 12-15 blocks |
| Topic drill | 8-12 blocks |
| Full mock | up to 50 blocks in total, at most 30 per section |

## By subject
- Ukrainian language: spelling and punctuation as `inline_choice` («Позначте рядок, у якому ...» only if all options are certain), sentence analysis as `categorization`, stress and word forms as `short_answer`.
- Maths: follow `method-maths.md` for solving and verification; answers are numbers with every written variant.
- History of Ukraine: chronology as `dialogue_order`, events and dates or figures as `matching`; include only dates and facts you are certain about.
- English: reading and use of language as `inline_choice` and `fill_blanks`; follow `method-languages.md` for level rules.
- Optional subjects: use the closest format above and `method-general.md` for the content structure.

## Lessons for exam preparation
When the request is a lesson, not a test: short theory chunk in `rich_text`, then 4-6 exam-format blocks on that topic with `retryEnabled: true`, then a 3-item mini-check. Add a `teacher_note` with the typical mistakes on this topic.
