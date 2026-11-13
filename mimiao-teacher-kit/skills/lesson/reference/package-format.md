# Mimiao package format (version 1)

A package is ONE JSON object saved as `<name>.mimiao.json`. The builder validates it and turns it into an interactive page. The key set is closed: any key not listed here is rejected. This format mirrors Mimiao's own task format, so a package can be imported into Mimiao without loss.

## Top-level keys

| key | rule |
|---|---|
| `mimiaoPackage` | always `1` |
| `kind` | `lesson`, `homework`, `test`, `game` or `course_plan` |
| `title` | 1..200 characters |
| `subject` | 1..80 characters, e.g. «Англійська мова» |
| `level` | optional, 0..80 characters: «A2», «7 клас», «НМТ» |
| `locale` | optional two-letter code of the teacher's language, default `uk`. The page has built-in labels for `uk` and `en`; any other locale shows Ukrainian labels unless overridden in `ui` |
| `minutes` | integer 5..240. Required for `lesson`, optional otherwise |
| `goal` | optional, up to 500 characters, one can-do sentence |
| `style` | optional `{ "primary": "#RRGGBB" }`. Only when the teacher asked for their colour |
| `ui` | optional label overrides (see below) |
| `sections` | required for `lesson`, `homework`, `test`; forbidden for `game` and `course_plan` |
| `test` | `{ "passPercent": 1..100 }`; required for kind `test` only |
| `game` | required for kind `game` only |
| `plan` | required for kind `course_plan` only |

`ui` keys (all optional, string values): `check, retry, correct, wrong, showAnswers, answerKey, printStudent, printTeacher, teacherMode, minutes, progress, finishTest, score, passed, failed, passMark, flip, next, prev, tabCards, tabPairs, tabQuiz, tabWrite, yourAnswer, week, lesson, goal, homework, copyPrompt, copied, saveInMimiao, madeWith, trueLabel, falseLabel, moveUp, moveDown, chooseGroup, theme, tasks, typeHere`.

## Sections and blocks

`sections` holds 1..20 objects `{ "title", "minutes"?, "blocks": [1..30 blocks] }`. Total blocks: lesson at most 60, homework at most 50, test at most 50. In a lesson, if every section has `minutes`, they must sum to the top-level `minutes`. Lessons, homework and tests need at least one practice block.

A block is `{ "type", "payload", "difficulty"? }`. `difficulty` (`easy`, `medium`, `hard`) is allowed only on practice blocks.

## Content blocks

| type | payload | note |
|---|---|---|
| `heading` | `{ "text" }` | |
| `rich_text` | `{ "html" }` | ONLY these tags, with NO attributes: `p br strong em u ul ol li h3 h4 blockquote table thead tbody tr th td sub sup code` |
| `hint` | `{ "text" }` | |
| `teacher_note` | `{ "text" }` | teacher-only: shown in teacher mode and in the print with answers |
| `divider` | `{}` | |

## Practice blocks

All practice blocks share this closed envelope as `payload`. Every key is required except `points`:

```json
{ "title": "", "hideTitle": false, "instruction": "Оберіть правильну відповідь.", "points": 1,
  "settings": { "retryEnabled": true, "showCorrectAnswer": true },
  "config": {} }
```

`instruction` must not be blank. `points` is 1..100 (it matters in tests). `config` depends on the type and is closed:

| type | config | rules |
|---|---|---|
| `short_answer` | `{ "text", "blanks": [{ "acceptedAnswers": [] }] }` | each blank is written `___` (three underscores) in `text`; markers == blanks, 1..15; 1..10 accepted answers per blank. Use for one-word or number answers and open short questions |
| `fill_blanks` | same as `short_answer` | gaps inside sentences or a short text |
| `inline_choice` | `{ "text", "blanks": [{ "options": [], "correctOptionIndex": 0 }] }` | `___` markers == blanks; 2..6 distinct options. This is also the multiple-choice question type: «Питання … ___» with the options in the blank |
| `true_false` | `{ "questions": [{ "text", "correct": true }] }` | 1..20 questions |
| `sentence_builder` | `{ "sentences": [] }` | 1..15 correct sentences of 3+ words; the page shuffles the words |
| `dialogue_order` | `{ "phrases": [] }` | 3..12 lines in the CORRECT order; the page shuffles them. Also use for any sequence: steps of a solution, chronology |
| `matching` | `{ "groups": ["Left title", "Right title"], "pairs": [{ "left", "right" }], "answersNewLine": false }` | 2..12 pairs; lefts distinct, rights distinct |
| `categorization` | `{ "groups": [{ "name", "elements": [] }] }` | 2..5 groups, 1..12 elements each; an element belongs to one group only |
| `word_transform` | `{ "pairs": [{ "incorrect", "correct" }] }` | 1..15 pairs; the student sees `incorrect` and types `correct`: error correction, opening brackets, word formation, rewriting |
| `cards` | `{ "cards": [{ "side1", "side2" }] }` | 1..50 flip cards; not scored; not allowed in tests |

A `test` may contain only `heading`, `rich_text`, `divider` and scored practice types (no `cards`, `hint`, `teacher_note`).

Not available in this kit, never emit: images, audio, video, embeds, accordion, tabs, columns, numeric_quantity, chess.

## How typed answers are checked

A typed answer is compared after trimming, collapsing spaces, lower-casing, unifying apostrophes and dropping one final `.`, `!` or `?`. Therefore list every legitimately correct variant in `acceptedAnswers` (`"3"`, `"x=3"`, `"x = 3"`; `"don't"`, `"do not"`). Prefer `inline_choice`, `matching` or `categorization` when many phrasings would be correct.

## Examples of every practice type

Each snippet is one complete block.

```json
{ "type": "short_answer", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Впишіть пропущене слово.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "She ___ (go) to school every day.", "blanks": [{ "acceptedAnswers": ["goes"] }] } } }
```

```json
{ "type": "fill_blanks", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Поставте дієслова у правильну форму.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "I ___ (not like) tea, but my sister ___ (like) it.", "blanks": [{ "acceptedAnswers": ["don't like", "do not like"] }, { "acceptedAnswers": ["likes"] }] } } }
```

```json
{ "type": "inline_choice", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Оберіть правильний варіант.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "Where ___ you from?", "blanks": [{ "options": ["is", "are", "am"], "correctOptionIndex": 1 }] } } }
```

```json
{ "type": "true_false", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Позначте, чи твердження правильне.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "questions": [{ "text": "Kyiv is the capital of Ukraine.", "correct": true }, { "text": "The Dnipro flows into the Baltic Sea.", "correct": false }] } } }
```

```json
{ "type": "sentence_builder", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Складіть речення зі слів.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "sentences": ["I usually walk to school", "She has lunch at noon"] } } }
```

```json
{ "type": "dialogue_order", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Розташуйте репліки в правильному порядку.", "points": 3, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "phrases": ["Hello! What would you like?", "A cup of tea, please.", "Here you are.", "Thank you."] } } }
```

```json
{ "type": "matching", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "З'єднайте слово з перекладом.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "groups": ["Слово", "Переклад"], "pairs": [{ "left": "apple", "right": "яблуко" }, { "left": "bread", "right": "хліб" }, { "left": "milk", "right": "молоко" }], "answersNewLine": false } } }
```

```json
{ "type": "categorization", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Розподіліть слова за групами.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "groups": [{ "name": "Fruit", "elements": ["apple", "banana", "plum"] }, { "name": "Vegetables", "elements": ["carrot", "potato", "onion"] }] } } }
```

```json
{ "type": "word_transform", "difficulty": "hard", "payload": { "title": "", "hideTitle": false, "instruction": "Виправте помилку в реченні.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "pairs": [{ "incorrect": "She go to school.", "correct": "She goes to school." }, { "incorrect": "He have a dog.", "correct": "He has a dog." }] } } }
```

```json
{ "type": "cards", "payload": { "title": "", "hideTitle": false, "instruction": "Переверніть картки й повторіть слова.", "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "cards": [{ "side1": "apple", "side2": "яблуко" }, { "side1": "bread", "side2": "хліб" }] } } }
```

Content blocks:

```json
{ "type": "teacher_note", "payload": { "text": "5 хв. Поставте 2-3 запитання про каву й чай, не виправляйте помилок." } }
```

```json
{ "type": "rich_text", "payload": { "html": "<h3>Present Simple</h3><p>He <strong>works</strong>, she <strong>studies</strong>.</p><table><thead><tr><th>I / you / we / they</th><th>he / she / it</th></tr></thead><tbody><tr><td>work</td><td>works</td></tr></tbody></table>" } }
```

## Complete package examples

Lesson (section minutes sum to `minutes`):

```json package
{
  "mimiaoPackage": 1,
  "kind": "lesson",
  "title": "At the café: ordering food and drink",
  "subject": "Англійська мова",
  "level": "A2",
  "locale": "uk",
  "minutes": 20,
  "goal": "I can order food and drink in a café and ask for the price.",
  "sections": [
    {
      "title": "Warm-up and dialogue",
      "minutes": 5,
      "blocks": [
        { "type": "teacher_note", "payload": { "text": "5 хв. Запитайте, що учні п'ють уранці, потім прочитайте діалог разом." } },
        { "type": "heading", "payload": { "text": "In the café" } },
        { "type": "rich_text", "payload": { "html": "<p><strong>Waiter:</strong> Hello! What would you like?</p><p><strong>Anna:</strong> A cup of tea, please.</p><p><strong>Waiter:</strong> Here you are.</p><p><strong>Anna:</strong> Thank you.</p>" } },
        { "type": "true_false", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Позначте, чи твердження правильне.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "questions": [{ "text": "The waiter asks what Anna would like.", "correct": true }, { "text": "Anna orders coffee.", "correct": false }] } } }
      ]
    },
    {
      "title": "Practice",
      "minutes": 10,
      "blocks": [
        { "type": "hint", "payload": { "text": "Подивіться на діалог: як Анна просить чай?" } },
        { "type": "inline_choice", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Оберіть правильний варіант.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "Can I ___ a cup of tea, please?", "blanks": [{ "options": ["have", "has", "having"], "correctOptionIndex": 0 }] } } },
        { "type": "divider", "payload": {} },
        { "type": "dialogue_order", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Розташуйте репліки в правильному порядку.", "points": 3, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "phrases": ["Hello! What would you like?", "A cup of tea, please.", "Here you are.", "Thank you."] } } }
      ]
    },
    {
      "title": "Recap",
      "minutes": 5,
      "blocks": [
        { "type": "short_answer", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Впишіть пропущене слово.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "Anna asks for the price: How ___ is it?", "blanks": [{ "acceptedAnswers": ["much"] }] } } }
      ]
    }
  ]
}
```

Homework:

```json package
{
  "mimiaoPackage": 1,
  "kind": "homework",
  "title": "Homework: Present Simple",
  "subject": "Англійська мова",
  "level": "A2",
  "minutes": 15,
  "goal": "I can talk about daily routines with he, she and it.",
  "sections": [
    {
      "title": "Practice",
      "blocks": [
        { "type": "rich_text", "payload": { "html": "<p>With <em>he</em>, <em>she</em>, <em>it</em> add <strong>-s</strong>: she <strong>works</strong>, he <strong>plays</strong>.</p>" } },
        { "type": "inline_choice", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Оберіть правильну форму дієслова.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "My brother ___ football on Sundays.", "blanks": [{ "options": ["play", "plays", "playing"], "correctOptionIndex": 1 }] } } },
        { "type": "fill_blanks", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Поставте дієслова у правильну форму.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "text": "Olena ___ (get up) at seven and ___ (drink) tea.", "blanks": [{ "acceptedAnswers": ["gets up"] }, { "acceptedAnswers": ["drinks"] }] } } },
        { "type": "word_transform", "difficulty": "hard", "payload": { "title": "", "hideTitle": false, "instruction": "Виправте помилку в реченні.", "points": 1, "settings": { "retryEnabled": true, "showCorrectAnswer": true }, "config": { "pairs": [{ "incorrect": "She go to school.", "correct": "She goes to school." }] } } }
      ]
    }
  ]
}
```

Test (no retries, no answers shown, no hints or notes, `test.passPercent` present):

```json package
{
  "mimiaoPackage": 1,
  "kind": "test",
  "title": "Test: Present Simple",
  "subject": "Англійська мова",
  "level": "A2",
  "minutes": 15,
  "test": { "passPercent": 80 },
  "sections": [
    {
      "title": "Grammar",
      "blocks": [
        { "type": "rich_text", "payload": { "html": "<p>Час на виконання: 15 хвилин.</p>" } },
        { "type": "inline_choice", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Оберіть правильну форму дієслова.", "points": 1, "settings": { "retryEnabled": false, "showCorrectAnswer": false }, "config": { "text": "She ___ to work by bus.", "blanks": [{ "options": ["go", "goes", "going"], "correctOptionIndex": 1 }] } } },
        { "type": "true_false", "difficulty": "easy", "payload": { "title": "", "hideTitle": false, "instruction": "Позначте, чи речення правильне.", "points": 1, "settings": { "retryEnabled": false, "showCorrectAnswer": false }, "config": { "questions": [{ "text": "He don't like fish.", "correct": false }, { "text": "They live in Lviv.", "correct": true }] } } },
        { "type": "short_answer", "difficulty": "medium", "payload": { "title": "", "hideTitle": false, "instruction": "Впишіть пропущене слово.", "points": 1, "settings": { "retryEnabled": false, "showCorrectAnswer": false }, "config": { "text": "My mother ___ (work) in a hospital.", "blanks": [{ "acceptedAnswers": ["works"] }] } } }
      ]
    }
  ]
}
```

Game (`cards`: 4..200, fronts distinct, no `sections`):

```json package
{
  "mimiaoPackage": 1,
  "kind": "game",
  "title": "Food: A1 words",
  "subject": "Англійська мова",
  "level": "A1",
  "game": {
    "preferredMode": "MATCH",
    "cards": [
      { "front": "apple", "back": "яблуко" },
      { "front": "bread", "back": "хліб" },
      { "front": "milk", "back": "молоко" },
      { "front": "cheese", "back": "сир", "alternatives": ["сирок"] }
    ]
  }
}
```

Course plan (weeks consecutive from 1, 1..7 lessons per week, `prompt` is a ready `/lesson` argument line):

```json package
{
  "mimiaoPackage": 1,
  "kind": "course_plan",
  "title": "English A2: 2 weeks (excerpt)",
  "subject": "Англійська мова",
  "level": "A2",
  "goal": "I can talk about my day, my family and my plans.",
  "plan": {
    "weeks": [
      {
        "week": 1,
        "theme": "Daily routine",
        "lessons": [
          { "title": "My day", "goal": "I can describe my daily routine.", "homework": "Напишіть 5 речень про свій ранок.", "prompt": "англійська A2, розпорядок дня, Present Simple, 45 хв" },
          { "title": "Free time", "goal": "I can say what I do in my free time.", "homework": "Вивчіть 10 слів про хобі.", "prompt": "англійська A2, вільний час і хобі, 45 хв" }
        ]
      },
      {
        "week": 2,
        "theme": "Family and friends",
        "lessons": [
          { "title": "My family", "goal": "I can describe my family members.", "homework": "Опишіть одного родича трьома реченнями.", "prompt": "англійська A2, моя родина, притяжні займенники, 45 хв" }
        ]
      }
    ]
  }
}
```
