---
name: from-material
description: Turns the teacher's own material (a photo of a textbook page, a PDF, pasted text or a word list) into interactive exercises, homework, a lesson, a test or a card game on one self-checking page. Use when the teacher attaches or pastes material or types /from-material, «з фото», «з підручника», «зі сторінки», «з тексту», «зроби вправи з цього».
argument-hint: "<фото сторінки підручника, PDF або текст + що зробити: вправи, домашнє, тест>"
---

# From material

Turn the teacher's OWN material into ONE package, build it into an interactive page and hand it over. The material can be a photo of a textbook page, a PDF, pasted text, a word list or the pasted content of a link.

## Behaviour
- Be fast. Do not show a plan or a preview first.
- Ask at most ONE question, and only when the material or the wish truly cannot be understood. Otherwise assume, build, and state the assumptions in one line afterwards.
- Talk to the teacher in the teacher's language; Ukrainian by default.
- If `~/.mimiao-teacher-kit/profile.json` exists, read it first and use it instead of asking.

## 1. Read the request, fill the gaps yourself
| Missing | Default |
|---|---|
| kind | `homework` |
| «урок» in the request | kind `lesson` (length 45 minutes) |
| «тест» or «контрольна» | kind `test` |
| a bare word list | kind `game` |
| count | the size defaults of the chosen kind (see that skill: `../homework/SKILL.md`, `../test/SKILL.md`, `../game/SKILL.md`, `../lesson/SKILL.md`) |
| level | read from the material |
| `locale` | the teacher's language |

## 2. Read the material fully
Read every attached image and every page. Identify the subject, the topic, the level and the source (book title, page) from the material itself.

## 3. Read the references
Read `../lesson/reference/package-format.md`, `../lesson/reference/writing-rules.md`, `../lesson/reference/delivery.md` and ONE method pack by subject: `../lesson/reference/method-languages.md` (foreign languages), `../lesson/reference/method-maths.md` (maths, physics, chemistry, informatics), `../lesson/reference/method-exam-nmt.md` (exams), `../lesson/reference/method-general.md` (anything else). Then compose the chosen kind following the rules of the matching skill (`../lesson/SKILL.md`, `../homework/SKILL.md`, `../test/SKILL.md`, `../game/SKILL.md`).

## 4. Rules for working with the material
- Stay inside the material: the same vocabulary, grammar, facts and level. Introduce nothing new.
- Do not reproduce long passages of a published textbook. Quote at most a few short sentences; otherwise write new sentences and texts on the same language points.
- Refer to the source as «за матеріалами с. N» in a `hint` block.
- Exercises printed in the textbook may become interactive only by rewriting the items with new sentences that train the same point.
- If the image is unreadable in places, use only what is legible and say in the assumptions line which part was skipped.
- If the material contains the answers (a key), use them. Otherwise solve every item yourself and verify.

## 5. Build and hand over
Follow `../lesson/reference/delivery.md` exactly: save, build, show, reply. Name the detected topic, level and source in the assumptions line, for example «тема: Present Perfect, A2, за матеріалами с. 42».

## 6. Silent checklist before building
- Every item is based on content that is in the material.
- No long quotation from the source; no new vocabulary or facts.
- Markers equal blanks; every answer verified; accepted variants listed.
- The kind's own rules are met (settings for tests, section minutes for lessons, fronts distinct for games).

## Never
- Paste the page code in chat or write HTML by hand when Python works.
- Copy a textbook page word for word.
- Add content the material does not cover, or guess unreadable parts.
- Invent block types or keys outside `package-format.md`.
- Add marketing beyond the line in `delivery.md`, or emojis.
