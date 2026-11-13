# Method pack: maths, physics, chemistry, informatics (school grades 1-11)

Use for any subject where the student solves problems with a verifiable result.

## Stages of a lesson

| # | Stage | Share of time | Purpose | Block types |
|---|---|---|---|---|
| 1 | Activate prior knowledge, 3-4 quick items | about 10% | recall what the new topic builds on | `true_false`, `short_answer` |
| 2 | Worked example | about 20% | show the full reasoning | `rich_text` with every step written out |
| 3 | Faded example | about 20% | same kind of problem, student completes part of it | `dialogue_order` for the order of steps, `fill_blanks` for the missing step |
| 4 | Guided practice, easy to medium | about 30% | build fluency | `short_answer`, `inline_choice`, `matching` |
| 5 | Independent practice with one harder or transfer problem | about 15% | apply in a new situation | `short_answer` |
| 6 | Exit check, 2 items | about 5% | see who got it | `true_false` or `short_answer` |

## Rules
- Plain-text maths only: `x^2`, `sqrt(x)`, `a/b`, `≤`, `≥`, `≠`, `·` for multiplication. `<sup>` and `<sub>` are allowed inside `rich_text`. No LaTeX, no images.
- Inside `rich_text` html never type a raw `<` or `>` as a comparison sign (it breaks the markup): write `&lt;` and `&gt;`, or use `≤` and `≥`. In every other field (instructions, task text, answers) type `<` and `>` normally.
- Every numeric answer lists its accepted variants: `"0.5"`, `"0,5"`, `"1/2"`; for equations `"3"`, `"x=3"`, `"x = 3"`.
- Answers are exact, or the instruction states the rounding («Округліть до десятих»).
- Units go in the instruction or in the sentence, not in the answer field.
- Verify every item twice: by solving it, and by substituting the answer back.
- Distractors in `inline_choice` are typical mistakes: a sign error, wrong order of operations, a forgotten step, confused formulas.
- Word problems use Ukrainian realities (hryvnias, Ukrainian cities, local distances) and the metric system.
- Set `difficulty` on every practice block (`easy` in stage 1 and the start of stage 4, `medium` in the rest of stage 4, `hard` in stage 5).
- The worked example shows ONE method clearly. Do not mix two methods in one example.
- `dialogue_order` for steps: each phrase is one complete step including the result, e.g. `2x + 3 = 11`, `2x = 8`, `x = 4`.
- Do not state a formula you are not sure about; leave it out and choose a simpler task.

## Typical lesson shape (45 min, grade 7)
1. `teacher_note`: timing and the one idea of the lesson.
2. Section «Пригадаємо»: 3-4 quick items.
3. Section «Приклад»: worked example in `rich_text`, then a faded example.
4. Section «Тренуємось»: 3-4 practice blocks, easy to medium.
5. Section «Самостійно»: 1-2 practice blocks with the transfer problem.
6. Section «Підсумок»: exit check with 2 items.

## Physics, chemistry, informatics
- Give the given data and the unknown in the problem text; the student only types the final number or term.
- Chemistry: write formulas in plain text with `<sub>`: `H<sub>2</sub>O` inside `rich_text`, `H2O` in typed answers (list both spellings).
- Informatics: code goes in `<code>` inside `rich_text`; typed answers are values or one-word results, not code.
- Keep numbers friendly in stages 2-3 so that the method, not the arithmetic, is what students see.
