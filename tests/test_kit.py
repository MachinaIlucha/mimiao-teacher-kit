"""Tests for the Mimiao Teacher Kit engine (validator, builder, template, zip)."""
import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
LESSON = PLUGIN / "mimiao-teacher-kit" / "skills" / "lesson"
SCRIPTS = LESSON / "scripts"
EXAMPLES = LESSON / "examples"
TEMPLATE = LESSON / "templates" / "player.html"
BUILD_PAGE = SCRIPTS / "build_page.py"
BUILD_ZIP = PLUGIN / "build_zip.py"
sys.path.insert(0, str(SCRIPTS))

from validate_package import PRESETS, STYLE_MODES, validate  # noqa: E402

EXAMPLE_FILES = [
    ("english-a2-travel.mimiao.json", "lesson"),
    ("maths-7-linear-equations.mimiao.json", "homework"),
    ("history-nmt-cossacks.mimiao.json", "test"),
    ("english-a2-travel-words.mimiao.json", "game"),
    ("english-a2-12-weeks.mimiao.json", "course_plan"),
]
KIT_DATA = re.compile(r'<script id="kit-data" type="application/json">(.*?)</script>', re.S)


def load(name):
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def lesson():
    return load("english-a2-travel.mimiao.json")


def find_block(pkg, block_type):
    for section in pkg["sections"]:
        for block in section["blocks"]:
            if block["type"] == block_type:
                return block
    raise AssertionError(f"no {block_type} block")


def errors_text(pkg):
    return "\n".join(validate(pkg))


def temp_dir():
    scratch = Path("F:/Mimiao/tmp/claude-kit")
    return tempfile.TemporaryDirectory(dir=str(scratch) if scratch.is_dir() else None)


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8")


class ValidatorTest(unittest.TestCase):
    def test_examples_are_valid(self):
        for name, _ in EXAMPLE_FILES:
            with self.subTest(name):
                self.assertEqual(validate(load(name)), [])

    def test_example_kinds(self):
        self.assertEqual([load(name)["kind"] for name, _ in EXAMPLE_FILES],
                         ["lesson", "homework", "test", "game", "course_plan"])

    def test_lesson_minutes_sum(self):
        pkg = lesson()
        pkg["sections"][0]["minutes"] += 1
        self.assertIn("minutes", errors_text(pkg))

    def test_blank_marker_mismatch(self):
        pkg = lesson()
        block = find_block(pkg, "short_answer")
        block["payload"]["config"]["text"] += " ___"
        text = errors_text(pkg)
        self.assertIn("config.text", text)
        self.assertIn("blank markers", text)

    def test_unknown_block_type(self):
        pkg = lesson()
        pkg["sections"][0]["blocks"].append({"type": "numeric_quantity", "payload": {}})
        self.assertIn("unsupported block type 'numeric_quantity'", errors_text(pkg))

    def test_extra_config_key(self):
        pkg = lesson()
        find_block(pkg, "cards")["payload"]["config"]["cards"][0]["image"] = "x.png"
        text = errors_text(pkg)
        self.assertIn("config.cards[0]", text)
        self.assertIn("unknown key 'image'", text)

    def test_missing_settings_key(self):
        pkg = lesson()
        del find_block(pkg, "true_false")["payload"]["settings"]["retryEnabled"]
        self.assertIn("settings", errors_text(pkg))
        self.assertIn("retryEnabled", errors_text(pkg))

    def test_blank_instruction(self):
        pkg = lesson()
        find_block(pkg, "true_false")["payload"]["instruction"] = "   "
        self.assertIn("payload.instruction", errors_text(pkg))

    def test_cards_not_allowed_in_test(self):
        pkg = load("history-nmt-cossacks.mimiao.json")
        cards = find_block(lesson(), "cards")
        pkg["sections"][0]["blocks"].append(copy.deepcopy(cards))
        pkg["sections"][0]["blocks"].append({"type": "hint", "payload": {"text": "x"}})
        pkg["sections"][0]["blocks"].append({"type": "teacher_note", "payload": {"text": "x"}})
        text = errors_text(pkg)
        for block_type in ("cards", "hint", "teacher_note"):
            self.assertIn(f"type '{block_type}' is not allowed in a test", text)

    def test_rich_text_rejects_script_and_attributes(self):
        cases = {
            "<p>x</p><script>alert(1)</script>": "script",
            '<a href="https://x.test">y</a>': "href",
            "<img src=x>": "img",
            '<p style="color:red">x</p>': "style",
            "<!-- c --><p>x</p>": "comments",
        }
        for html_text, fragment in cases.items():
            with self.subTest(html_text):
                pkg = lesson()
                find_block(pkg, "rich_text")["payload"]["html"] = html_text
                text = errors_text(pkg)
                self.assertIn("payload.html", text)
                self.assertIn(fragment, text)

    def test_bool_is_not_int(self):
        pkg = lesson()
        pkg["minutes"] = True
        self.assertIn("minutes", errors_text(pkg))
        pkg = lesson()
        pkg["mimiaoPackage"] = True
        self.assertIn("mimiaoPackage", errors_text(pkg))

    def test_cover_must_be_known(self):
        pkg = lesson()
        pkg["cover"] = "weather"
        text = errors_text(pkg)
        self.assertIn("cover", text)
        self.assertIn("must be one of", text)
        pkg["cover"] = "maths"
        self.assertEqual(validate(pkg), [])

    def test_style_preset_must_be_known(self):
        pkg = lesson()
        pkg["style"] = {"preset": "neon"}
        text = errors_text(pkg)
        self.assertIn("style.preset: must be one of", text)
        for name in PRESETS:
            self.assertIn(name, text)

    def test_style_mode_must_be_known(self):
        pkg = lesson()
        pkg["style"] = {"mode": "sepia"}
        text = errors_text(pkg)
        self.assertIn("style.mode: must be one of", text)
        for name in STYLE_MODES:
            self.assertIn(name, text)

    def test_style_accent_must_be_hex(self):
        pkg = lesson()
        for bad in ("red", "#12345", "#GGGGGG", 5):
            with self.subTest(repr(bad)):
                pkg["style"] = {"accent": bad}
                self.assertIn("style.accent: must be a #RRGGBB colour", errors_text(pkg))

    def test_style_unknown_key(self):
        pkg = lesson()
        pkg["style"] = {"preset": "pop", "font": "Comic Sans"}
        self.assertIn("style: unknown key 'font'", errors_text(pkg))

    def test_style_full_object_is_valid(self):
        pkg = lesson()
        pkg["style"] = {"preset": "notebook", "primary": "#2456C8", "accent": "#FFE66D", "mode": "dark"}
        self.assertEqual(validate(pkg), [])

    def test_unknown_top_level_key(self):
        pkg = lesson()
        pkg["extra"] = 1
        self.assertIn("unknown key 'extra'", errors_text(pkg))

    def test_game_requires_four_cards(self):
        pkg = load("english-a2-travel-words.mimiao.json")
        pkg["game"]["cards"] = pkg["game"]["cards"][:3]
        self.assertIn("game.cards", errors_text(pkg))

    def test_plan_weeks_must_be_consecutive(self):
        pkg = load("english-a2-12-weeks.mimiao.json")
        pkg["plan"]["weeks"][1]["week"] = 5
        self.assertIn("plan.weeks[1].week", errors_text(pkg))

    def test_non_object_package(self):
        for value in ([], None, "text", 5):
            with self.subTest(repr(value)):
                self.assertEqual(validate(value), ["$: package must be a JSON object"])


class BuildTest(unittest.TestCase):
    def test_build_injects_data_and_title(self):
        source = EXAMPLES / "english-a2-travel.mimiao.json"
        pkg = json.loads(source.read_text(encoding="utf-8"))
        with temp_dir() as tmp:
            out = Path(tmp) / "page.html"
            result = run(BUILD_PAGE, source, out)
            self.assertEqual(result.returncode, 0, result.stderr)
            page = out.read_text(encoding="utf-8")
        self.assertIn(f"<title>{pkg['title']}</title>", page)
        self.assertIn('<html lang="uk">', page)
        match = KIT_DATA.search(page)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match.group(1).replace("<\\/", "</")), pkg)

    def test_build_escapes_script_close(self):
        pkg = lesson()
        pkg["title"] = "A </script> B"
        with temp_dir() as tmp:
            source = Path(tmp) / "evil.mimiao.json"
            source.write_text(json.dumps(pkg, ensure_ascii=False), encoding="utf-8")
            result = run(BUILD_PAGE, source)
            self.assertEqual(result.returncode, 0, result.stderr)
            out = Path(tmp) / "evil.html"
            self.assertTrue(out.exists(), "default output path must replace .mimiao.json with .html")
            page = out.read_text(encoding="utf-8")
        # one closing tag for the data script and one for the player script, nothing from the data
        self.assertEqual(page.count("</script>"), 2)
        match = KIT_DATA.search(page)
        self.assertIsNotNone(match)
        self.assertNotIn("</", match.group(1))
        self.assertEqual(json.loads(match.group(1).replace("<\\/", "</")), pkg)
        self.assertIn("<title>A &lt;/script&gt; B</title>", page)

    def test_build_refuses_invalid_package(self):
        pkg = lesson()
        pkg["kind"] = "nonsense"
        with temp_dir() as tmp:
            source = Path(tmp) / "bad.mimiao.json"
            out = Path(tmp) / "bad.html"
            source.write_text(json.dumps(pkg, ensure_ascii=False), encoding="utf-8")
            result = run(BUILD_PAGE, source, out)
            self.assertEqual(result.returncode, 1)
            self.assertIn("kind", result.stderr)
            self.assertFalse(out.exists())

    def test_template_has_markers_and_no_external_scripts(self):
        page = TEMPLATE.read_text(encoding="utf-8")
        for marker in ('<script id="kit-data" type="application/json">{}</script>',
                       "<title>Mimiao Teacher Kit</title>", '<html lang="uk">'):
            self.assertEqual(page.count(marker), 1, marker)
        self.assertNotIn("<script src", page)
        allowed = ("https://fonts.googleapis.com", "https://fonts.gstatic.com", "https://mimiao.online")
        for url in re.findall(r"https?://[^\s\"'<>)]+", page):
            self.assertTrue(url.startswith(allowed), url)


    def test_template_defines_all_presets(self):
        page = TEMPLATE.read_text(encoding="utf-8")
        for name in PRESETS:
            with self.subTest(name):
                self.assertIn(f'[data-preset="{name}"]', page)
        self.assertEqual(len(PRESETS), 6)


class ZipTest(unittest.TestCase):
    def test_zip_builds(self):
        result = run(BUILD_ZIP)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        archive = PLUGIN / "dist" / "mimiao-teacher-kit.zip"
        self.assertTrue(archive.exists())
        with zipfile.ZipFile(archive) as bundle:
            names = bundle.namelist()
        self.assertIn("mimiao-teacher-kit/skills/lesson/templates/player.html", names)
        self.assertIn("mimiao-teacher-kit/skills/lesson/scripts/build_page.py", names)
        self.assertEqual(names, sorted(names))
        self.assertFalse([n for n in names if "__pycache__" in n or n.endswith(".pyc")])


if __name__ == "__main__":
    unittest.main()
