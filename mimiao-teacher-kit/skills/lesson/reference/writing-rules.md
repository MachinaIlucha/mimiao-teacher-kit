# Writing rules for every item

These rules are binding for every lesson, homework, test and game. Apply them while writing, then run the final self-check.

## One thing per item
- One word, one form, one fact or one step per item.
- Write the answer first, then build the sentence around it.
- Exactly one correct answer, unless the type allows several accepted variants; then list all of them in `acceptedAnswers`.
- No item may be answerable in two ways. If it can be, rewrite the item.

## Distractors (wrong options)
- Real and plausible words or values of the same category and about the same length as the answer.
- Built from typical learner mistakes (wrong form, sign error, confused word).
- Never invented words, never jokes, never «all of the above» or «none of the above».

## Instructions
- One imperative sentence in the teacher's language.
- The same wording for the same type throughout a package.
- A problem that needs given data (a word problem, a physics or chemistry task) puts the data right after that sentence in the same `instruction`: «Розв'яжіть задачу. Напруга 5 В, опір 10 Ом.» Longer context (a text, a table) goes into a `rich_text` block placed just before the task.
- `title`: a short name of the task («Завдання 3», «Правда чи ні?») with `hideTitle: false`; number tasks in tests. Leave `title` empty only when the instruction alone is enough.
- Typed answers in Ukrainian or another inflected language: list every case form and spelling a correct student could type, and both Cyrillic and Latin look-alike letters for unit symbols («А» and «A»).
- Never leave an instruction blank.

## Facts
- Use only what is certain. Dates, formulas, names, quotations and rules you are not sure about are left out, not guessed.
- Never fabricate quotations or sources.
- For exam items never claim that an item comes from a real past paper.

## Level
- Nothing above the stated level or grade in vocabulary, grammar or syllabus.
- The lower the level, the shorter the sentences.

## Order and variety
- Inside a section go from easy to hard, and from recognition (choose, match, sort) to production (type, build, transform).
- No more than two blocks of the same type in a row.
- A lesson of 45+ minutes uses at least five different practice types.
- 4-8 items per block; a block takes the student 2-5 minutes.

## Content
- Neutral, age-appropriate content: no politics, religion, violence, brands or real private people.
- Use inclusive names.
- For Ukrainian teachers use Ukrainian contexts and realities by default.

## Teacher notes
- `teacher_note` holds timing, what to say, typical mistakes to watch and how to extend the task for a fast student.
- Never put answers in a `teacher_note`: the page builds the answer key itself.

## Settings
- Lessons and homework: `retryEnabled: true`, `showCorrectAnswer: true`.
- Tests: `retryEnabled: false`, `showCorrectAnswer: false`.
- Set `difficulty` on practice blocks of homework and tests; use `points` 1 unless a method pack says otherwise.

## Final self-check before building
Run this silently; fix problems, do not report them.
- Every answer was verified by actually solving the item.
- The number of `___` markers equals the number of blanks in every block.
- No duplicate items, no duplicate fronts or pairs.
- Section minutes add up to the lesson `minutes`.
- The language of the instructions is consistent and is the teacher's language.
- Every `acceptedAnswers` list contains all legitimate variants (spacing, `0.5` and `0,5`, contractions).
- Only tags allowed in `rich_text` are used, and none has attributes.
