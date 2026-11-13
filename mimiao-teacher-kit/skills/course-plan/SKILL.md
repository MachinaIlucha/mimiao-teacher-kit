---
name: course-plan
description: Builds a week-by-week course plan (themes, lesson goals, homework and a ready /lesson request for every lesson) as one interactive page. Use when the teacher asks for a programme, a syllabus or a plan for a term, or types /course-plan, «програма», «план курсу», «календарний план», «навчальний план», «план на семестр», «підготовка до НМТ».
argument-hint: "<предмет, рівень, мета, скільки тижнів і уроків на тиждень>"
---

# Course plan

Produce ONE package of kind `course_plan`, build it into an interactive page and hand it over.

## Behaviour
- Be fast. Do not show a plan or a preview first.
- Ask at most ONE question, and only when the subject truly cannot be inferred. Otherwise assume, build, and state the assumptions in one line afterwards.
- Talk to the teacher in the teacher's language; Ukrainian by default.
- If `~/.mimiao-teacher-kit/profile.json` exists, read it first and use it instead of asking.

## 1. Read the request, fill the gaps yourself
| Missing | Default |
|---|---|
| level now | A1 for languages when unstated; for school subjects the grade inferred from the request |
| goal | the next level (languages) or the end of the school year |
| weeks | 12 |
| lessons per week | 2 |
| lesson length | 45 minutes, written into each `prompt` |
| `locale` | the teacher's language |

## 2. Read the references
Read `../lesson/reference/package-format.md`, `../lesson/reference/writing-rules.md`, `../lesson/reference/delivery.md` and ONE method pack by subject, for the progression of topics:
- foreign languages: `../lesson/reference/method-languages.md`
- maths, physics, chemistry, informatics: `../lesson/reference/method-maths.md`
- exam goals (НМТ, ЗНО and similar): `../lesson/reference/method-exam-nmt.md`
- everything else: `../lesson/reference/method-general.md`

## 3. Compose the plan
- `kind` is `course_plan`. No `sections`. The top-level `plan` key is `{ "weeks": [...] }` with 1-52 weeks numbered consecutively from 1; each week has 1-7 lessons.
- Use backward design: start from the goal and decide what must be mastered by the end, then place topics from the simplest to the most complex.
- Set `cover` to the illustration that fits the subject (see `package-format.md`).
- Look: follow `package-format.md` → `style`. If the teacher names a style or colours («зошит», «поп», «журнал», «ніч», «дитячий», «синій»), set `style.preset` / `style.primary` / `style.accent` and remember it.
- Each week has a `theme`. Each lesson has a `title`, a can-do `goal`, a one-line `homework` and a `prompt`.
- `prompt` is a ready argument line for `/lesson` in the teacher's language, with subject, level, topic and length, for example «англійська A2, подорожі, Present Perfect, 45 хв».
- Spiral review: the first lesson of each week recycles the previous week's material.
- Every 4th week ends with a revision lesson and a test lesson; the `prompt` of the test lesson is an argument line for `/test`.
- For exam goals distribute the topics by the official programme sections as far as you know them, and leave the last two weeks for mock tests (`/test` prompts in the exam format).
- No exact dates, no facts you are unsure of; keep goals and topics realistic for the stated number of weeks.

## 4. Build and hand over
Follow `../lesson/reference/delivery.md` exactly: save, build, show, reply. This skill's reply also says, in the teacher's language: «скопіюйте запит будь-якого уроку і запустіть /lesson».

## 5. Silent checklist before building
- Weeks are consecutive from 1; each has 1-7 lessons; every lesson has all four fields.
- Every `prompt` is complete enough to run with `/lesson` or `/test` without more questions.
- Every 4th week ends with revision and a `/test` prompt; the last two weeks are mock tests for exam goals.
- Difficulty rises gradually; no topic appears twice without a purpose.
- No unknown keys.

## Never
- Paste the page code in chat or write HTML by hand when Python works.
- Generate the lessons themselves; the plan holds only the prompts.
- Invent block types or keys outside `package-format.md`.
- Add marketing beyond the line in `delivery.md`, or emojis.
