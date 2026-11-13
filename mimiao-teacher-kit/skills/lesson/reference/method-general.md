# Method pack: any other subject

Use for history, biology, geography, literature, music theory, programming, professional courses, primary school and preschool.

## Stages of a lesson

| # | Stage | Share of time | Purpose | Block types |
|---|---|---|---|---|
| 1 | Hook question | about 10% | make students curious and show what they already know | `teacher_note` with the question, `true_false` for a quick guess |
| 2 | New material in small chunks | about 40% | teach in pieces; each chunk is followed by a 2-4 item check | `rich_text` (at most 150 words per chunk), then `true_false` or `inline_choice` |
| 3 | Structuring | about 25% | organise what was learned | `categorization`, `matching`; `dialogue_order` for processes and chronology |
| 4 | Application | about 15% | use the knowledge on a new case | `short_answer`, `word_transform`, a case question as `inline_choice` |
| 5 | Recap | about 10% | retrieve and close | `cards` with key terms, an exit `true_false` |

## Rules
- Retrieval practice over re-reading: after each chunk the student answers, not just reads.
- Concrete examples come before definitions. Show two examples, then name the concept.
- A chunk has one idea. Use `<ul>` and `<table>` in `rich_text` to keep chunks scannable.
- Use only facts you are certain about; leave out dates, numbers and quotations you would have to guess.
- Terms in `cards`: `side1` is the term, `side2` is a definition of at most 12 words.
- `word_transform` fits «fix the wrong statement» tasks: `incorrect` is a false sentence, `correct` is the corrected one.
- Programming: code goes in `<code>` inside `rich_text`; typed answers are short values or one keyword.
- Professional courses: use realistic cases from the field as `inline_choice` questions with plausible distractors.

## Ages under 10
- Sentences shorter than 10 words.
- Use only `matching`, `categorization`, `true_false` and `cards`.
- No typed answer longer than one word.
- 3-5 items per block and a lot of concrete, familiar objects.
- Instructions are one short sentence («З'єднайте.», «Розподіліть.»).

## Preschool and primary school
- One topic, three short chunks, recap with `cards`.
- Content from the child's world: family, animals, food, seasons, school things.
- The `teacher_note` of each section says what the adult reads aloud.

## Scale
A 45-minute lesson: about 9-11 practice blocks, at least five practice types where the age allows it. For ages under 10 use at most four types and shorter blocks.

## Quick checks for a lesson
- Every chunk of `rich_text` is followed by a check on that chunk only.
- The recap retrieves the key terms of the whole lesson, not new material.
