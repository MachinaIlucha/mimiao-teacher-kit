# Mimiao Teacher Kit

Безкоштовний набір для вчителів і репетиторів від [Mimiao](https://mimiao.online): ви вводите одну команду, а Claude створює готовий інтерактивний матеріал. Це плагін для Claude: працює в застосунку Claude і в Claude Code.

## Команди

| Команда | Що робить | Приклад |
|---|---|---|
| `/lesson` | повний урок з вправами | `/lesson англійська A2, подорожі, Present Perfect, 45 хв` |
| `/from-material` | вправи, домашнє, тест або гра з вашого матеріалу (фото сторінки, PDF, текст) | `/from-material домашнє завдання з цієї сторінки підручника` |
| `/homework` | інтерактивне домашнє завдання | `/homework Present Perfect, A2, 8 завдань` |
| `/test` | тест із прохідним балом | `/test тема «Подорожі», A2, прохідний бал 80%` |
| `/game` | картки зі словами для ігор | `/game 20 слів на тему «Їжа», A1` |
| `/course-plan` | план курсу по тижнях | `/course-plan англійська A2, 12 тижнів, 2 уроки на тиждень` |

## Що ви отримуєте
- Інтерактивну сторінку: вправи перевіряються автоматично, учень одразу бачить результат.
- Друк для учня та друк з відповідями для вчителя.
- Будь-який предмет: мови, математика, підготовка до НМТ, історія, біологія, початкова школа та інші.
- Будь-яку правку на вимогу: «зроби складніше», «додай ще 5 речень», «без граматики».

## Встановлення

**Застосунок Claude.** Завантажте [zip-архів плагіна](https://github.com/MachinaIlucha/mimiao-teacher-kit/raw/main/download/mimiao-teacher-kit.zip), відкрийте «Customize» → «Add plugin», завантажте архів і введіть, наприклад, `/lesson англійська A2, подорожі, 45 хв`.

**Claude Code.**

```
/plugin marketplace add MachinaIlucha/mimiao-teacher-kit
/plugin install mimiao-teacher-kit@mimiao
```


## Вимоги
Python 3.9+ для створення сторінки. Якщо Python недоступний, Claude збирає сторінку вручну за готовим шаблоном.

## Збереження в Mimiao
Матеріал, який створює плагін, має той самий формат, що й завдання в Mimiao, тому його можна імпортувати в Mimiao без втрат. У Mimiao можна призначити матеріал учням, отримувати відповіді й бачити результати в журналі; набір карток там запускається у 20 ігрових режимах. Сайт: https://mimiao.online

## Ліцензія
MIT, див. [LICENSE](LICENSE).

## Для розробників
```
python -m unittest discover -s tests
python build_zip.py
```

---

# Mimiao Teacher Kit (English)

A free Claude plugin for tutors and schools by [Mimiao](https://mimiao.online). A teacher types one command, and Claude writes a lesson, homework, test, card game or course plan as an interactive page with automatic checking, print for the student and print with answers. Any subject works.

Commands: `/lesson`, `/from-material`, `/homework`, `/test`, `/game`, `/course-plan`.

Install in the Claude app: download [the zip](https://github.com/MachinaIlucha/mimiao-teacher-kit/raw/main/download/mimiao-teacher-kit.zip), open "Customize", choose "Add plugin", upload the zip, then type `/lesson ...`. Install in Claude Code: `/plugin marketplace add MachinaIlucha/mimiao-teacher-kit`, then `/plugin install mimiao-teacher-kit@mimiao`. Python 3.9+ is needed for the page builder; without it the page is assembled manually from the template.

The package format mirrors Mimiao's task format, so the material can be imported into Mimiao. Licence: MIT.
