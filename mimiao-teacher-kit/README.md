# Mimiao Teacher Kit

A free Claude plugin for tutors and schools by [Mimiao](https://mimiao.online). A teacher types one command; Claude writes one JSON package, a bundled script validates it and builds a self-contained interactive HTML page: auto-checked exercises, print for the student, print with answers. Any subject works. The teacher is answered in their own language (Ukrainian by default).

Безкоштовний плагін Claude для вчителів і репетиторів від [Mimiao](https://mimiao.online). Одна команда: Claude створює матеріал, скрипт перевіряє його та збирає інтерактивну сторінку з автоматичною перевіркою, друком для учня та друком з відповідями. Будь-який предмет.

## Commands

| Command | Result |
|---|---|
| `/lesson` | a full lesson with exercises |
| `/from-material` | exercises, homework, a lesson, a test or a game made from the teacher's own material (photo, PDF, text) |
| `/homework` | interactive homework from a topic or a lesson |
| `/test` | a test with a pass mark |
| `/game` | a card set from a word list or a topic |
| `/course-plan` | a week-by-week course plan with a ready `/lesson` request per lesson |

## Folder map

```
mimiao-teacher-kit/
  .claude-plugin/plugin.json   plugin manifest
  skills/
    lesson/                    the lesson skill and everything shared by all skills
      SKILL.md
      reference/               package format, writing rules, method packs, delivery procedure
      scripts/                 validator and page builder
      templates/               player.html, the page template
      examples/                ready example packages
    from-material/SKILL.md
    homework/SKILL.md
    test/SKILL.md
    game/SKILL.md
    course-plan/SKILL.md
```

The five other skills read the shared reference through `../lesson/reference/`.

## Licence

MIT, see [LICENSE](LICENSE).

## Looks

Every page can be shown in six complete styles, chosen by the teacher in the request («стиль зошит», «зроби в синіх кольорах», «темна тема») or switched live with the «Вигляд» button on the page: `mimiao` (universal), `pop` (bold, for teens and adults), `editorial` (magazine, for adults and exam preparation), `notebook` (exercise book, for school subjects), `night` (dark arcade, for teens, coding and games) and `kids` (ages 6-10). Colours can be overridden on top of any style.
