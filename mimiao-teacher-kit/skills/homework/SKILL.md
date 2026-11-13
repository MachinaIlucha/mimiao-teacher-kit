---
name: homework
description: Builds an interactive homework page of 8-10 auto-checked tasks, ordered from easy to hard and printable, from a topic or from a lesson made earlier in the conversation. Use when the teacher asks for homework or extra practice, or types /homework, «домашнє завдання», «домашка», «додаткові вправи», «закріплення».
argument-hint: "<тема або готовий урок, рівень, скільки завдань>"
---

# Homework

Produce ONE package of kind `homework`, build it into an interactive page and hand it over.

## Behaviour
- Be fast. Do not show a plan or a preview first.
- Ask at most ONE question, and only when the subject or the topic truly cannot be inferred. Otherwise assume, build, and state the assumptions in one line afterwards.
- Talk to the teacher in the teacher's language; Ukrainian by default.
- If `~/.mimiao-teacher-kit/profile.json` exists, read it first and use it instead of asking.

## 1. Read the request, fill the gaps yourself
| Missing | Default |
|---|---|
| source | the latest lesson package in this conversation, else the topic in the request |
| size | 15-20 minutes of work = 8-10 practice blocks |
| sections | 2-3, ordered easy to hard |
| level | the lesson's level; else A2 for languages, the grade inferred from the topic, else «7 клас» |
| `locale` | the teacher's language |

## 2. Read the references
Read `../lesson/reference/package-format.md`, `../lesson/reference/writing-rules.md`, `../lesson/reference/delivery.md` and ONE method pack by subject:
- foreign languages: `../lesson/reference/method-languages.md`
- maths, physics, chemistry, informatics: `../lesson/reference/method-maths.md`
- exams: `../lesson/reference/method-exam-nmt.md`
- everything else: `../lesson/reference/method-general.md`

## 3. Compose the homework
- `kind` is `homework`. `minutes` is omitted or the estimate of the work time.
- When the source is a lesson from this conversation, reuse its words and structures but write NEW items. Never copy the lesson's items.
- Set `cover` to the illustration that fits the subject (see `package-format.md`).
- Look: follow `package-format.md` → `style`. If the teacher names a style or colours («зошит», «поп», «журнал», «ніч», «дитячий», «синій»), set `style.preset` / `style.primary` / `style.accent` and remember it.
- The first block is a short `rich_text`: a reminder of the rule or a worked example.
- Then 8-10 practice blocks in 2-3 sections, easy to hard, with `difficulty` set on every practice block; recognition before production.
- The last block is one productive task (`word_transform`, `sentence_builder` or `short_answer`).
- No `teacher_note`, unless grading guidance is really needed.
- Every block uses `retryEnabled: true, showCorrectAnswer: true`.
- The instructions are written so that a student can do the task alone, without the teacher.

## 4. Build and hand over
Follow `../lesson/reference/delivery.md` exactly: save, build, show, reply. State the source («за уроком ...» or the topic) in the assumptions line.

## 5. Silent checklist before building
- 8-10 practice blocks; `difficulty` on each; no more than two blocks of one type in a row.
- No item is copied from the source lesson; every answer verified; accepted variants listed.
- The reminder block comes first; the last block is productive.
- The workload fits the minutes (2-5 minutes per block).
- No unknown keys, no forbidden block types.

## Never
- Paste the page code in chat or write HTML by hand when Python works.
- Copy items from the lesson.
- Put answers in a `teacher_note`.
- Invent block types or keys outside `package-format.md`.
- Add marketing beyond the line in `delivery.md`, or emojis.
