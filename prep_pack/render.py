# -*- coding: utf-8 -*-
"""极简 Markdown → HTML（标准库，只覆盖本工具生成的子集）。"""
import html
import re

CSS = """
body{font-family:'Microsoft YaHei',system-ui,sans-serif;max-width:820px;margin:32px auto;
     padding:0 24px;line-height:1.75;color:#222}
h1{font-size:24px;border-bottom:2px solid #444;padding-bottom:8px}
h2{font-size:19px;margin-top:28px;border-left:4px solid #4a7;padding-left:10px}
h3{font-size:16px;margin-top:20px}
blockquote{background:#f4f7f4;border-left:4px solid #8aa;margin:12px 0;
           padding:8px 14px;color:#456}
li{margin:4px 0} code{background:#f2f2f2;padding:2px 5px;border-radius:3px}
pre{background:#f7f7f7;padding:12px;overflow:auto;border-radius:5px}
table{border-collapse:collapse;width:100%} td,th{border:1px solid #ccc;padding:6px 10px}
hr{border:0;border-top:1px solid #ddd;margin:24px 0}
@media print{body{margin:0;max-width:none}h2{break-after:avoid}blockquote{break-inside:avoid}}
"""


def _inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _body(md):
    out, in_code, in_ul = [], False, False
    for line in md.splitlines():
        s = line.rstrip()
        if s.startswith("```"):
            out.append("<pre><code>" if not in_code else "</code></pre>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(s))
            continue
        if not s.strip():
            if in_ul:
                out.append("</ul>")
                in_ul = False
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            n = len(m.group(1))
            out.append(f"<h{n}>{_inline(m.group(2))}</h{n}>")
            continue
        if s.startswith(">"):
            out.append("<blockquote>" + _inline(s.lstrip("> ")) + "</blockquote>")
            continue
        m = re.match(r"^\s*(?:\d+\.|-|\*)\s+(.*)$", s)
        if m:
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append("<li>" + _inline(m.group(1)) + "</li>")
            continue
        if s.startswith("---"):
            out.append("<hr>")
            continue
        out.append("<p>" + _inline(s) + "</p>")
    if in_ul:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def to_html(data, md):
    title = f"{data['grade']}{data['subject']}备课包 · {data['topic']}"
    return ("<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
            + _body(md) + "\n</body>\n</html>\n")
