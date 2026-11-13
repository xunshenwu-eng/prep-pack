# -*- coding: utf-8 -*-
"""四段式讲义生成。"""
import json


def build_markdown(data):
    subject, grade, topic = data["subject"], data["grade"], data["topic"]
    qs = data["questions"]
    lines = [
        f"# {grade}{subject}备课包 · {topic}", "",
        f"> 共 {len(qs)} 题。结构：题干重述 → 逐题解析 → 知识点网 → 讲授课话术。",
        "> 题干与答案由输入提供，本工具只做组织与排版，不自动解题。", "",
        "## 一、题干重述", "",
        "> 先确认材料读对了：逐题复述，印刷模糊或截断处标明依据。", "",
    ]
    for i, q in enumerate(qs, 1):
        lines.append(f"{i}. **第 {q.get('id', i)} 题**：{str(q['stem']).strip()}")
    lines += ["", "## 二、逐题解析", ""]
    for i, q in enumerate(qs, 1):
        lines += [f"### 第 {q.get('id', i)} 题", "",
                  f"- **题干**：{str(q['stem']).strip()}",
                  f"- **答案**：{str(q['answer']).strip()}"]
        if q.get("analysis"):
            lines.append(f"- **解析**：{str(q['analysis']).strip()}")
        pits = q.get("pitfalls") or []
        if pits:
            lines.append("- **易错点**：" + "；".join(str(p) for p in pits))
        lines.append("")
    lines += ["## 三、知识点网", "",
              "> 从「就题论题」扩到整章体系，用来兜住学生的追问。", ""]
    kw = data.get("knowledge_web") or []
    if kw:
        for k in kw:
            lines.append(f"- {k}")
    else:
        lines.append("- （未填写 knowledge_web，建议补齐本章核心概念与相邻考点）")
    lines += ["", "## 四、讲授课话术", "",
              "> 能当场念出来的表达，不是书面解答。", ""]
    for i, q in enumerate(qs, 1):
        talk = q.get("talk") or f"先带学生复述第 {q.get('id', i)} 题条件，再一起找突破口。"
        lines += [f"**第 {q.get('id', i)} 题**：{talk}", ""]
    lines += ["---", "",
              "> 如与标准答案不符，请以教材为准并回查原始材料；本备课包供讲授准备使用。", ""]
    return "\n".join(lines)


def build_outline(data):
    return {
        "subject": data["subject"], "grade": data["grade"], "topic": data["topic"],
        "question_count": len(data["questions"]),
        "knowledge_points": data.get("knowledge_web", []),
        "questions": [
            {"id": q.get("id", i), "stem": q["stem"], "answer": q["answer"],
             "has_analysis": bool(q.get("analysis")), "has_talk": bool(q.get("talk")),
             "pitfall_count": len(q.get("pitfalls") or [])}
            for i, q in enumerate(data["questions"], 1)
        ],
    }


def write_outputs(data, outdir):
    import os
    from .render import to_html
    os.makedirs(outdir, exist_ok=True)
    md = build_markdown(data)
    paths = {}
    for name, content in (("lesson.md", md),
                          ("lesson.html", to_html(data, md)),
                          ("outline.json", json.dumps(build_outline(data), ensure_ascii=False, indent=1))):
        p = os.path.join(outdir, name)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        paths[name] = p
    return paths
