---
name: lesson
description: Builds a complete interactive lesson for any subject (a language, maths, exam preparation, anything else) as one self-checking web page with print for the student and print with answers. Use when a teacher asks for a lesson, a lesson plan or class materials, or types /lesson, «урок», «конспект уроку», «підготуй урок», «заняття», «розмовний урок», «НМТ».
argument-hint: "<напр.: англійська A2, подорожі, Present Perfect, 45 хв | математика 7 клас, лінійні рівняння>"
---

# Lesson

Produce ONE package of kind `lesson`, build it into an interactive page (auto-checked exercises, print for the student, print with answers) and hand it over to the teacher.

## Behaviour
- Be fast. Do not show a plan, an outline or a preview first.
- Ask at most ONE question, and only when the subject or the topic truly cannot be inferred. Otherwise assume, build, and state the assumptions in one line afterwards.
- Talk to the teacher in the teacher's language; Ukrainian by default.
- If `~/.mimiao-teacher-kit/profile.json` exists, read it first and use it instead of asking.

## 1. Read the request, fill the gaps yourself
| Missing | Default |
|---|---|
| length | 45 minutes (allowed 20-120) |
| level | A2 for languages; for school subjects the grade inferred from the topic, else «7 клас» |
| focus | balanced |
| `locale` | the teacher's language |
| students' language | the teacher's language |
| colour | none (omit `style`) |

Recognise focus words: «розмовний», «більше говоріння» = speaking; «граматика» = grammar; «без граматики» = no grammar; «лексика» = vocabulary.

## 2. Read the references
Read these files in this skill's folder: `reference/package-format.md`, `reference/writing-rules.md`, `reference/delivery.md`, and ONE method pack by subject:
- foreign languages: `reference/method-languages.md`
- maths, physics, chemistry, informatics: `reference/method-maths.md`
- НМТ, ЗНО and other exams: `reference/method-exam-nmt.md`
- everything else: `reference/method-general.md`

## 3. Compose the lesson
- `kind` is `lesson`. Set `title`, `subject`, `level`, `locale`, `minutes`.
- `goal` is one can-do sentence.
- 5-8 sections that follow the stages of the chosen method pack. Every section has `minutes`, and they sum exactly to the lesson length.
- Scale: about one practice block per 4 minutes plus the content blocks (`heading`, `rich_text`, `hint`).
- Open every section with a `teacher_note` (timing and what to do).
- End with a recap section.
- Apply `writing-rules.md` to every item; lesson blocks use `retryEnabled: true, showCorrectAnswer: true`.
- Content you write for students (texts, dialogues, examples) is original and written at the stated level.

## 4. Build and hand over
Follow `reference/delivery.md` exactly: save, build, show, reply. After the delivery lines add exactly one extra line naming the sibling commands: `/homework`, `/test` and `/game` can be made from this lesson. Offer nothing else.

## 5. Silent checklist before building
- Section minutes sum to `minutes`; no more than two blocks of one type in a row.
- At least five different practice types for 45+ minutes.
- Every `___` marker has its blank; every answer verified by solving; accepted variants listed.
- Instructions are in one language and worded the same for the same type.
- No `teacher_note` contains answers; no forbidden block types; no unknown keys.

## Never
- Paste the page code in chat or write HTML by hand when Python works.
- Ask for a plan approval or several clarifying questions.
- Use facts, quotations or dates you are not sure about.
- Invent block types or keys outside `package-format.md`.
- Add marketing beyond the line in `delivery.md`, or emojis.
