---
name: test
description: Builds an interactive test with a pass mark, no retries and no hints, from topics, earlier lessons or an exam format, printable with an answer key. Use when the teacher asks for a test, quiz or exam practice, or types /test, «тест», «контрольна», «контрольна робота», «діагностика», «НМТ», «пробний іспит», «вхідний тест».
argument-hint: "<що перевіряємо: теми або уроки, рівень, прохідний бал>"
---

# Test

Produce ONE package of kind `test`, build it into an interactive page and hand it over.

## Behaviour
- Be fast. Do not show a plan or a preview first.
- Ask at most ONE question, and only when the subject or the topic truly cannot be inferred. Otherwise assume, build, and state the assumptions in one line afterwards.
- Talk to the teacher in the teacher's language; Ukrainian by default.
- If `~/.mimiao-teacher-kit/profile.json` exists, read it first and use it instead of asking.

## 1. Read the request, fill the gaps yourself
| Missing | Default |
|---|---|
| source | lessons or packages in this conversation, else the topics in the request, else an exam format |
| size | 15-20 scored items overall in 8-12 blocks |
| sections | 1-3, one per skill or topic |
| `passPercent` | 80 for unit tests, 60 for exam-style tests |
| level | the source's level; else A2 for languages, the grade inferred from the topic, else «7 клас» |
| `locale` | the teacher's language |

## 2. Read the references
Read `../lesson/reference/package-format.md`, `../lesson/reference/writing-rules.md`, `../lesson/reference/delivery.md` and ONE method pack by subject:
- foreign languages: `../lesson/reference/method-languages.md`
- maths, physics, chemistry, informatics: `../lesson/reference/method-maths.md`
- exam formats (НМТ, ЗНО and similar): `../lesson/reference/method-exam-nmt.md`
- everything else: `../lesson/reference/method-general.md`

## 3. Compose the test
- `kind` is `test` and the top-level `test` key is `{ "passPercent": N }`. `minutes` is optional (the time to solve).
- Set `cover` to the illustration that fits the subject (see `package-format.md`).
- Look: follow `package-format.md` → `style`. If the teacher names a style or colours («зошит», «поп», «журнал», «ніч», «дитячий», «синій»), set `style.preset` / `style.primary` / `style.accent` and remember it.
- Blocks: only `heading`, `rich_text`, `divider` and scored practice types. No `cards`, no `hint`, no `teacher_note`.
- Every practice block has `retryEnabled: false, showCorrectAnswer: false` and a `difficulty`; set `points` per the method pack.
- Items inside a section run easy first; recognition before production.
- All items are NEW: never copy items from the lessons the test is based on. Test the same words, structures and skills with fresh sentences and values.
- No hints, no translations in the items.
- A placement test spans levels in ascending order. Notes are not allowed in tests, so put the mapping of score bands to levels into the reply line, not into the package.
- Start with a short `rich_text`: time allowed and how to answer.

## 4. Build and hand over
Follow `../lesson/reference/delivery.md` exactly: save, build, show, reply. The assumptions line (a) also states the pass mark, for example «A2, 18 завдань, прохідний бал 80%».

## 5. Silent checklist before building
- `retryEnabled: false` and `showCorrectAnswer: false` in every practice block.
- No `cards`, `hint` or `teacher_note` anywhere; `test.passPercent` present.
- 15-20 scored items overall; every answer verified by solving; accepted variants listed.
- No item copied from a lesson; no duplicates; no item answerable two ways.
- Items go from easy to hard inside each section.

## Never
- Paste the page code in chat or write HTML by hand when Python works.
- Allow retries, show correct answers or give hints inside a test.
- Present exam-style items as real past-paper items.
- Invent block types or keys outside `package-format.md`.
- Add marketing beyond the line in `delivery.md`, or emojis.
