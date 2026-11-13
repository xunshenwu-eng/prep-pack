# -*- coding: utf-8 -*-
import os, sys, json, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prep_pack import cli, schema, builder, render, pdfinspect

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE = os.path.join(HERE, "examples", "questions.json")


class TestSchema(unittest.TestCase):
    def test_example_valid(self):
        with open(EXAMPLE, encoding="utf-8") as f:
            self.assertEqual(schema.validate(json.load(f)), [])

    def test_missing_root(self):
        self.assertTrue(schema.validate({"subject": "数学"}))

    def test_missing_question_fields(self):
        d = {"subject": "数学", "grade": "初三", "topic": "t",
             "questions": [{"stem": "x"}]}
        self.assertTrue(any("answer" in e for e in schema.validate(d)))

    def test_not_object(self):
        self.assertTrue(schema.validate([]))


class TestBuilder(unittest.TestCase):
    def setUp(self):
        with open(EXAMPLE, encoding="utf-8") as f:
            self.data = json.load(f)

    def test_four_sections(self):
        md = builder.build_markdown(self.data)
        for s in ("题干重述", "逐题解析", "知识点网", "讲授课话术"):
            self.assertIn(s, md)

    def test_outline(self):
        o = builder.build_outline(self.data)
        self.assertEqual(o["question_count"], 2)
        self.assertTrue(o["questions"][0]["has_talk"])

    def test_write_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            paths = builder.write_outputs(self.data, d)
            self.assertEqual(len(paths), 3)
            for p in paths.values():
                self.assertTrue(os.path.getsize(p) > 0)
            with open(paths["lesson.html"], encoding="utf-8") as f:
                self.assertIn("<html", f.read())


class TestRender(unittest.TestCase):
    def test_heading_and_bold(self):
        h = render.to_html({"grade": "初三", "subject": "数学", "topic": "t"},
                           "# 标题\n\n**粗体** 与 `代码`\n")
        self.assertIn("<h1>标题</h1>", h)
        self.assertIn("<strong>粗体</strong>", h)
        self.assertIn("<code>代码</code>", h)

    def test_escapes_html(self):
        h = render.to_html({"grade": "g", "subject": "s", "topic": "t"}, "<script>x</script>")
        self.assertNotIn("<script>", h)


class TestPdfInspect(unittest.TestCase):
    def test_missing_dependency_is_graceful(self):
        ok, payload = pdfinspect.inspect("nonexistent.pdf")
        self.assertFalse(ok)
        self.assertIsInstance(payload, str)
        self.assertTrue(payload)

    def test_summarize(self):
        self.assertIn("纯扫描件", pdfinspect.summarize([0, 0]))
        self.assertIn("文本型", pdfinspect.summarize([100, 200]))
        self.assertIn("混合型", pdfinspect.summarize([0, 120]))


class TestCli(unittest.TestCase):
    def test_validate(self):
        self.assertEqual(cli.main(["validate", EXAMPLE]), 0)

    def test_demo(self):
        self.assertEqual(cli.main(["demo"]), 0)

    def test_bad_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "bad.json")
            with open(p, "w", encoding="utf-8") as f:
                f.write("{oops")
            self.assertEqual(cli.main(["validate", p]), 2)

    def test_invalid_input(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"subject": "数学"}, f)
            self.assertEqual(cli.main(["validate", p]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
