#!/usr/bin/env python3
"""Validate a Mimiao Teacher Kit package (format v1).

Usage: python validate_package.py <package.json>

The practice-block payloads mirror the CRM class HomeworkTaskPayloadContract
(closed envelope + closed per-type config) with stricter kit limits, so a valid
package can be imported into the CRM Homework canvas unchanged.
Standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from typing import Any

KINDS = ("lesson", "homework", "test", "game", "course_plan")
CONTENT_TYPES = ("heading", "rich_text", "hint", "teacher_note", "divider")
PRACTICE_TYPES = (
    "short_answer", "true_false", "inline_choice", "fill_blanks", "sentence_builder",
    "dialogue_order", "matching", "categorization", "word_transform", "cards",
)
GAME_MODES = (
    "FLASHCARDS", "LEARN", "WRITE", "SPELL", "TEST", "MATCH", "LIVE", "TEAMS", "BLAST", "BLOCKS",
    "MEMORY", "BINGO", "QUIZ", "QUEST", "BOSS", "HANGMAN", "ANAGRAM", "OPEN_BOX", "WHEEL", "SPEAKING",
)
UI_KEYS = (
    "check", "retry", "correct", "wrong", "showAnswers", "answerKey", "printStudent", "printTeacher",
    "teacherMode", "minutes", "progress", "finishTest", "score", "passed", "failed", "passMark", "flip",
    "next", "prev", "tabCards", "tabPairs", "tabQuiz", "tabWrite", "yourAnswer", "week", "lesson", "goal",
    "homework", "copyPrompt", "copied", "saveInMimiao", "madeWith", "trueLabel", "falseLabel", "moveUp",
    "moveDown", "chooseGroup", "theme", "tasks", "typeHere",
)

TOP_LEVEL_KEYS = (
    "mimiaoPackage", "kind", "title", "subject", "level", "locale", "minutes", "goal", "style", "ui",
    "sections", "test", "game", "plan",
)
RICH_TEXT_TAGS = frozenset(
    "p br strong em u ul ol li h3 h4 blockquote table thead tbody tr th td sub sup code".split()
)
DIFFICULTIES = ("easy", "medium", "hard")
TEST_FORBIDDEN_TYPES = ("hint", "teacher_note", "cards")

_BLANK = re.compile(r"_{3,}")
_LOCALE = re.compile(r"[a-z]{2}")
_HEX = re.compile(r"#[0-9A-Fa-f]{6}")
_ITEM_MAX = 4000
_TEXT_MAX = 12000


def _add(errs: list[str], path: str, msg: str) -> None:
    errs.append(f"{path}: {msg}")


def _is_int(value: Any) -> bool:
    return type(value) is int  # bool is a subclass of int; it must not pass


def _obj(value: Any, path: str, errs: list[str], required: tuple = (), optional: tuple = ()) -> dict | None:
    if not isinstance(value, dict):
        _add(errs, path, "must be an object")
        return None
    allowed = set(required) | set(optional)
    for key in value:
        if key not in allowed:
            _add(errs, path, f"unknown key '{key}'")
    for key in required:
        if key not in value:
            _add(errs, path, f"missing required key '{key}'")
    return value


def _str(value: Any, path: str, errs: list[str], lo: int = 0, hi: int = _ITEM_MAX) -> bool:
    if not isinstance(value, str):
        _add(errs, path, "must be a string")
        return False
    ok = True
    if lo >= 1 and not value.strip():
        _add(errs, path, "must not be blank")
        ok = False
    if len(value) > hi:
        _add(errs, path, f"is too long (max {hi} characters)")
        ok = False
    return ok


def _int(value: Any, path: str, errs: list[str], lo: int, hi: int) -> bool:
    if not _is_int(value):
        _add(errs, path, "must be an integer")
        return False
    if value < lo or value > hi:
        _add(errs, path, f"must be between {lo} and {hi}")
        return False
    return True


def _bool(value: Any, path: str, errs: list[str]) -> bool:
    if type(value) is not bool:
        _add(errs, path, "must be true or false")
        return False
    return True


def _list(value: Any, path: str, errs: list[str], lo: int, hi: int) -> list | None:
    if not isinstance(value, list):
        _add(errs, path, "must be an array")
        return None
    if len(value) < lo or len(value) > hi:
        _add(errs, path, f"must have {lo}..{hi} items (has {len(value)})")
    return value


def _str_list(value: Any, path: str, errs: list[str], lo: int, hi: int, distinct: bool = False,
              item_hi: int = _ITEM_MAX) -> list | None:
    items = _list(value, path, errs, lo, hi)
    if items is None:
        return None
    seen: set[str] = set()
    for i, item in enumerate(items):
        if _str(item, f"{path}[{i}]", errs, 1, item_hi) and distinct:
            key = item.strip()
            if key in seen:
                _add(errs, f"{path}[{i}]", f"duplicate value '{item}'")
            seen.add(key)
    return items


# --------------------------------------------------------------------------- rich text

class _RichTextChecker(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.problems: list[str] = []

    def _problem(self, msg: str) -> None:
        if msg not in self.problems:
            self.problems.append(msg)

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag not in RICH_TEXT_TAGS:
            self._problem(f"tag <{tag}> is not allowed")
        for name, _ in attrs:
            self._problem(f"attribute '{name}' is not allowed (tags carry no attributes)")

    def handle_endtag(self, tag: str) -> None:
        if tag not in RICH_TEXT_TAGS:
            self._problem(f"tag </{tag}> is not allowed")

    def handle_comment(self, data: str) -> None:
        self._problem("comments are not allowed")

    def handle_decl(self, decl: str) -> None:
        self._problem("declarations are not allowed")

    def handle_pi(self, data: str) -> None:
        self._problem("processing instructions are not allowed")

    def unknown_decl(self, data: str) -> None:
        self._problem("declarations are not allowed")


def _check_rich_html(html_text: str, path: str, errs: list[str]) -> None:
    checker = _RichTextChecker()
    try:
        checker.feed(html_text)
        checker.close()
    except Exception as exc:  # malformed markup must never crash the validator
        _add(errs, path, f"html could not be parsed ({exc})")
        return
    for problem in checker.problems:
        _add(errs, path, problem)


# --------------------------------------------------------------------------- practice configs

def _check_text_markers(text: Any, blanks: Any, path: str, errs: list[str]) -> None:
    if not isinstance(text, str) or not isinstance(blanks, list):
        return
    count = len(_BLANK.findall(text))
    if count != len(blanks):
        _add(errs, f"{path}.text", f"has {count} blank markers (___) but {len(blanks)} blanks")


def _cfg_answer_blanks(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("text", "blanks"))
    if c is None:
        return
    if "text" in c:
        _str(c["text"], f"{path}.text", errs, 1, _TEXT_MAX)
    if "blanks" in c:
        blanks = _list(c["blanks"], f"{path}.blanks", errs, 1, 15)
        for i, blank in enumerate(blanks or []):
            bp = f"{path}.blanks[{i}]"
            b = _obj(blank, bp, errs, required=("acceptedAnswers",))
            if b is not None and "acceptedAnswers" in b:
                _str_list(b["acceptedAnswers"], f"{bp}.acceptedAnswers", errs, 1, 10)
        _check_text_markers(c.get("text"), c["blanks"], path, errs)


def _cfg_inline_choice(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("text", "blanks"))
    if c is None:
        return
    if "text" in c:
        _str(c["text"], f"{path}.text", errs, 1, _TEXT_MAX)
    if "blanks" in c:
        blanks = _list(c["blanks"], f"{path}.blanks", errs, 1, 15)
        for i, blank in enumerate(blanks or []):
            bp = f"{path}.blanks[{i}]"
            b = _obj(blank, bp, errs, required=("options", "correctOptionIndex"))
            if b is None:
                continue
            options = None
            if "options" in b:
                options = _str_list(b["options"], f"{bp}.options", errs, 2, 6, distinct=True)
            if "correctOptionIndex" in b:
                idx = b["correctOptionIndex"]
                if not _is_int(idx):
                    _add(errs, f"{bp}.correctOptionIndex", "must be an integer")
                elif options is not None and not 0 <= idx < len(options):
                    _add(errs, f"{bp}.correctOptionIndex", f"must be between 0 and {len(options) - 1}")
        _check_text_markers(c.get("text"), c["blanks"], path, errs)


def _cfg_true_false(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("questions",))
    if c is None or "questions" not in c:
        return
    questions = _list(c["questions"], f"{path}.questions", errs, 1, 20)
    for i, q in enumerate(questions or []):
        qp = f"{path}.questions[{i}]"
        qo = _obj(q, qp, errs, required=("text", "correct"))
        if qo is None:
            continue
        if "text" in qo:
            _str(qo["text"], f"{qp}.text", errs, 1)
        if "correct" in qo:
            _bool(qo["correct"], f"{qp}.correct", errs)


def _cfg_sentence_builder(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("sentences",))
    if c is None or "sentences" not in c:
        return
    sentences = _str_list(c["sentences"], f"{path}.sentences", errs, 1, 15)
    for i, s in enumerate(sentences or []):
        if isinstance(s, str) and s.strip() and len(s.split()) < 3:
            _add(errs, f"{path}.sentences[{i}]", "must have at least 3 words")


def _cfg_dialogue_order(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("phrases",))
    if c is not None and "phrases" in c:
        _str_list(c["phrases"], f"{path}.phrases", errs, 3, 12)


def _cfg_matching(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("groups", "pairs", "answersNewLine"))
    if c is None:
        return
    if "groups" in c:
        _str_list(c["groups"], f"{path}.groups", errs, 2, 2)
    if "answersNewLine" in c:
        _bool(c["answersNewLine"], f"{path}.answersNewLine", errs)
    if "pairs" not in c:
        return
    pairs = _list(c["pairs"], f"{path}.pairs", errs, 2, 12)
    seen = {"left": set(), "right": set()}
    for i, pair in enumerate(pairs or []):
        pp = f"{path}.pairs[{i}]"
        po = _obj(pair, pp, errs, required=("left", "right"))
        if po is None:
            continue
        for side in ("left", "right"):
            if side in po and _str(po[side], f"{pp}.{side}", errs, 1):
                key = po[side].strip()
                if key in seen[side]:
                    _add(errs, f"{pp}.{side}", f"duplicate {side} value '{po[side]}'")
                seen[side].add(key)


def _cfg_categorization(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("groups",))
    if c is None or "groups" not in c:
        return
    groups = _list(c["groups"], f"{path}.groups", errs, 2, 5)
    owner: dict[str, int] = {}
    for i, group in enumerate(groups or []):
        gp = f"{path}.groups[{i}]"
        go = _obj(group, gp, errs, required=("name", "elements"))
        if go is None:
            continue
        if "name" in go:
            _str(go["name"], f"{gp}.name", errs, 1)
        if "elements" in go:
            elements = _str_list(go["elements"], f"{gp}.elements", errs, 1, 12)
            for j, el in enumerate(elements or []):
                if not isinstance(el, str) or not el.strip():
                    continue
                key = el.strip()
                if key in owner and owner[key] != i:
                    _add(errs, f"{gp}.elements[{j}]", f"element '{el}' also appears in groups[{owner[key]}]")
                owner.setdefault(key, i)


def _cfg_word_transform(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("pairs",))
    if c is None or "pairs" not in c:
        return
    pairs = _list(c["pairs"], f"{path}.pairs", errs, 1, 15)
    for i, pair in enumerate(pairs or []):
        pp = f"{path}.pairs[{i}]"
        po = _obj(pair, pp, errs, required=("incorrect", "correct"))
        if po is None:
            continue
        ok = True
        for key in ("incorrect", "correct"):
            if key in po:
                ok = _str(po[key], f"{pp}.{key}", errs, 1) and ok
            else:
                ok = False
        if ok and po["incorrect"].strip() == po["correct"].strip():
            _add(errs, pp, "incorrect and correct must differ")


def _cfg_cards(cfg: Any, path: str, errs: list[str]) -> None:
    c = _obj(cfg, path, errs, required=("cards",))
    if c is None or "cards" not in c:
        return
    cards = _list(c["cards"], f"{path}.cards", errs, 1, 50)
    for i, card in enumerate(cards or []):
        cp = f"{path}.cards[{i}]"
        co = _obj(card, cp, errs, required=("side1", "side2"))
        if co is None:
            continue
        for key in ("side1", "side2"):
            if key in co:
                _str(co[key], f"{cp}.{key}", errs, 1)


_CONFIG_CHECKS = {
    "short_answer": _cfg_answer_blanks,
    "fill_blanks": _cfg_answer_blanks,
    "inline_choice": _cfg_inline_choice,
    "true_false": _cfg_true_false,
    "sentence_builder": _cfg_sentence_builder,
    "dialogue_order": _cfg_dialogue_order,
    "matching": _cfg_matching,
    "categorization": _cfg_categorization,
    "word_transform": _cfg_word_transform,
    "cards": _cfg_cards,
}


def _practice_payload(btype: str, payload: Any, path: str, errs: list[str]) -> None:
    p = _obj(payload, path, errs,
             required=("title", "hideTitle", "instruction", "settings", "config"), optional=("points",))
    if p is None:
        return
    if "title" in p:
        _str(p["title"], f"{path}.title", errs, 0, 240)
    if "hideTitle" in p:
        _bool(p["hideTitle"], f"{path}.hideTitle", errs)
    if "instruction" in p:
        _str(p["instruction"], f"{path}.instruction", errs, 1, 12000)
    if "points" in p:
        _int(p["points"], f"{path}.points", errs, 1, 100)
    if "settings" in p:
        s = _obj(p["settings"], f"{path}.settings", errs, required=("retryEnabled", "showCorrectAnswer"))
        if s is not None:
            for key in ("retryEnabled", "showCorrectAnswer"):
                if key in s:
                    _bool(s[key], f"{path}.settings.{key}", errs)
    if "config" in p:
        _CONFIG_CHECKS[btype](p["config"], f"{path}.config", errs)


def _content_payload(btype: str, payload: Any, path: str, errs: list[str]) -> None:
    if btype == "divider":
        _obj(payload, path, errs)
        return
    limits = {"heading": 200, "rich_text": 20000, "hint": 2000, "teacher_note": 4000}
    field = "html" if btype == "rich_text" else "text"
    p = _obj(payload, path, errs, required=(field,))
    if p is None or field not in p:
        return
    if _str(p[field], f"{path}.{field}", errs, 1, limits[btype]) and btype == "rich_text":
        _check_rich_html(p[field], f"{path}.html", errs)


# --------------------------------------------------------------------------- structure

def _block(block: Any, path: str, kind: str, errs: list[str]) -> str | None:
    """Validate one block; returns its type when it is a known, allowed type."""
    b = _obj(block, path, errs, required=("type", "payload"), optional=("difficulty",))
    if b is None:
        return None
    btype = b.get("type")
    known = isinstance(btype, str) and (btype in CONTENT_TYPES or btype in PRACTICE_TYPES)
    allowed = known
    if "type" in b:
        if not isinstance(btype, str):
            _add(errs, f"{path}.type", "must be a string")
        elif not known:
            _add(errs, f"{path}.type", f"unsupported block type '{btype}'")
        elif kind == "test" and (btype in TEST_FORBIDDEN_TYPES):
            _add(errs, f"{path}.type", f"type '{btype}' is not allowed in a test")
            allowed = False
    if "difficulty" in b:
        if b["difficulty"] not in DIFFICULTIES or not isinstance(b["difficulty"], str):
            _add(errs, f"{path}.difficulty", "must be one of easy, medium, hard")
        elif known and btype not in PRACTICE_TYPES:
            _add(errs, f"{path}.difficulty", "is allowed only on practice blocks")
    if known and "payload" in b:
        if btype in PRACTICE_TYPES:
            _practice_payload(btype, b["payload"], f"{path}.payload", errs)
        else:
            _content_payload(btype, b["payload"], f"{path}.payload", errs)
    return btype if allowed else None


def _sections(pkg: dict, kind: str, errs: list[str]) -> None:
    sections = _list(pkg["sections"], "sections", errs, 1, 20)
    if sections is None:
        return
    total = 0
    practice = 0
    minutes_all = True
    minutes_sum = 0
    for i, section in enumerate(sections):
        sp = f"sections[{i}]"
        s = _obj(section, sp, errs, required=("title", "blocks"), optional=("minutes",))
        if s is None:
            minutes_all = False
            continue
        if "title" in s:
            _str(s["title"], f"{sp}.title", errs, 1, 120)
        if "minutes" in s:
            if _int(s["minutes"], f"{sp}.minutes", errs, 1, 240):
                minutes_sum += s["minutes"]
            else:
                minutes_all = False
        else:
            minutes_all = False
        if "blocks" in s:
            blocks = _list(s["blocks"], f"{sp}.blocks", errs, 1, 30)
            for j, block in enumerate(blocks or []):
                total += 1
                btype = _block(block, f"{sp}.blocks[{j}]", kind, errs)
                if btype in PRACTICE_TYPES:
                    practice += 1
    limit = 60 if kind == "lesson" else 50
    if kind in ("lesson", "homework", "test") and total > limit:
        _add(errs, "sections", f"has {total} blocks in total (max {limit} for a {kind})")
    if practice == 0:
        _add(errs, "sections", "needs at least one practice block")
    if kind == "lesson" and minutes_all and _is_int(pkg.get("minutes")) and minutes_sum != pkg["minutes"]:
        _add(errs, "sections", f"section minutes sum to {minutes_sum} but top-level minutes is {pkg['minutes']}")


def _game(game: Any, errs: list[str]) -> None:
    g = _obj(game, "game", errs, required=("preferredMode", "cards"))
    if g is None:
        return
    if "preferredMode" in g and g["preferredMode"] not in GAME_MODES:
        _add(errs, "game.preferredMode", "must be one of " + ", ".join(GAME_MODES))
    if "cards" not in g:
        return
    cards = _list(g["cards"], "game.cards", errs, 4, 200)
    seen: set[str] = set()
    for i, card in enumerate(cards or []):
        cp = f"game.cards[{i}]"
        c = _obj(card, cp, errs, required=("front", "back"), optional=("alternatives",))
        if c is None:
            continue
        if "front" in c and _str(c["front"], f"{cp}.front", errs, 1, 300):
            key = c["front"].strip()
            if key in seen:
                _add(errs, f"{cp}.front", f"duplicate front '{c['front']}'")
            seen.add(key)
        if "back" in c:
            _str(c["back"], f"{cp}.back", errs, 1, 300)
        if "alternatives" in c:
            _str_list(c["alternatives"], f"{cp}.alternatives", errs, 0, 5, item_hi=300)


def _plan(plan: Any, errs: list[str]) -> None:
    p = _obj(plan, "plan", errs, required=("weeks",))
    if p is None or "weeks" not in p:
        return
    weeks = _list(p["weeks"], "plan.weeks", errs, 1, 52)
    for i, week in enumerate(weeks or []):
        wp = f"plan.weeks[{i}]"
        w = _obj(week, wp, errs, required=("week", "theme", "lessons"))
        if w is None:
            continue
        if "week" in w and _int(w["week"], f"{wp}.week", errs, 1, 52) and w["week"] != i + 1:
            _add(errs, f"{wp}.week", f"must be {i + 1} (weeks are numbered consecutively from 1)")
        if "theme" in w:
            _str(w["theme"], f"{wp}.theme", errs, 1, 200)
        if "lessons" in w:
            lessons = _list(w["lessons"], f"{wp}.lessons", errs, 1, 7)
            for j, lesson in enumerate(lessons or []):
                lp = f"{wp}.lessons[{j}]"
                lo = _obj(lesson, lp, errs, required=("title", "goal"), optional=("homework", "prompt"))
                if lo is None:
                    continue
                if "title" in lo:
                    _str(lo["title"], f"{lp}.title", errs, 1, 200)
                if "goal" in lo:
                    _str(lo["goal"], f"{lp}.goal", errs, 1, 500)
                for key in ("homework", "prompt"):
                    if key in lo:
                        _str(lo[key], f"{lp}.{key}", errs, 0, 500)


def _validate(pkg: Any, errs: list[str]) -> None:
    if not isinstance(pkg, dict):
        _add(errs, "$", "package must be a JSON object")
        return
    _obj(pkg, "$", errs, required=("mimiaoPackage", "kind", "title", "subject"), optional=TOP_LEVEL_KEYS[4:])
    if "mimiaoPackage" in pkg and not (_is_int(pkg["mimiaoPackage"]) and pkg["mimiaoPackage"] == 1):
        _add(errs, "mimiaoPackage", "must be the integer 1")
    kind = pkg.get("kind")
    kind_ok = isinstance(kind, str) and kind in KINDS
    if "kind" in pkg and not kind_ok:
        _add(errs, "kind", "must be one of " + ", ".join(KINDS))
    if "title" in pkg:
        _str(pkg["title"], "title", errs, 1, 200)
    if "subject" in pkg:
        _str(pkg["subject"], "subject", errs, 1, 80)
    if "level" in pkg:
        _str(pkg["level"], "level", errs, 0, 80)
    if "goal" in pkg:
        _str(pkg["goal"], "goal", errs, 0, 500)
    if "locale" in pkg:
        if not isinstance(pkg["locale"], str) or not _LOCALE.fullmatch(pkg["locale"]):
            _add(errs, "locale", "must be a two-letter lower-case language code")
    if "minutes" in pkg:
        _int(pkg["minutes"], "minutes", errs, 5, 240)
    elif kind == "lesson":
        _add(errs, "minutes", "is required for a lesson")
    if "style" in pkg:
        s = _obj(pkg["style"], "style", errs, optional=("primary",))
        if s is not None and "primary" in s:
            if not isinstance(s["primary"], str) or not _HEX.fullmatch(s["primary"]):
                _add(errs, "style.primary", "must be a #RRGGBB color")
    if "ui" in pkg:
        ui = pkg["ui"]
        if not isinstance(ui, dict):
            _add(errs, "ui", "must be an object")
        else:
            for key, value in ui.items():
                if key not in UI_KEYS:
                    _add(errs, "ui", f"unknown key '{key}'")
                else:
                    _str(value, f"ui.{key}", errs, 1, 80)
    if not kind_ok:
        return
    needs_sections = kind in ("lesson", "homework", "test")
    for key, needed in (("sections", needs_sections), ("test", kind == "test"),
                        ("game", kind == "game"), ("plan", kind == "course_plan")):
        if needed and key not in pkg:
            _add(errs, key, f"is required for kind {kind}")
        elif not needed and key in pkg:
            _add(errs, key, f"is not allowed for kind {kind}")
    if needs_sections and "sections" in pkg:
        _sections(pkg, kind, errs)
    if kind == "test" and "test" in pkg:
        t = _obj(pkg["test"], "test", errs, required=("passPercent",))
        if t is not None and "passPercent" in t:
            _int(t["passPercent"], "test.passPercent", errs, 1, 100)
    if kind == "game" and "game" in pkg:
        _game(pkg["game"], errs)
    if kind == "course_plan" and "plan" in pkg:
        _plan(pkg["plan"], errs)


def validate(package: Any) -> list[str]:
    """Return a list of `<json path>: <message>` errors; empty when the package is valid."""
    errs: list[str] = []
    try:
        _validate(package, errs)
    except Exception as exc:  # the validator must never raise on malformed input
        errs.append(f"$: internal validator error ({type(exc).__name__}: {exc})")
    return errs


def summary(package: dict) -> str:
    kind = package["kind"]
    if kind == "game":
        return f"OK: game, {len(package['game']['cards'])} cards"
    if kind == "course_plan":
        return f"OK: course_plan, {len(package['plan']['weeks'])} weeks"
    blocks = sum(len(section["blocks"]) for section in package["sections"])
    return f"OK: {kind}, {blocks} blocks"


def _reject_constant(name: str) -> Any:
    raise ValueError(f"invalid number {name}")


def load_package(path: str) -> Any:
    """Read UTF-8 JSON; raises ValueError (including JSONDecodeError) on bad syntax."""
    with open(path, encoding="utf-8") as handle:
        return json.loads(handle.read(), parse_constant=_reject_constant)


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page
        except (AttributeError, ValueError):
            pass
    if len(argv) != 2:
        print("usage: python validate_package.py <package.json>", file=sys.stderr)
        return 2
    try:
        package = load_package(argv[1])
    except (ValueError, UnicodeDecodeError) as exc:
        print(f"JSON error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"cannot read {argv[1]}: {exc}", file=sys.stderr)
        return 2
    errors = validate(package)
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    print(summary(package))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
