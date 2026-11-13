# -*- coding: utf-8 -*-
import os, sys, json, argparse
from . import schema, builder, pdfinspect


def main(argv=None):
    ap = argparse.ArgumentParser(prog="prep-pack", description="家教备课包生成器（核心零依赖）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="校验题目 JSON")
    v.add_argument("path")

    b = sub.add_parser("build", help="生成备课包")
    b.add_argument("path")
    b.add_argument("-o", "--out", default="./out")

    i = sub.add_parser("inspect", help="PDF 判型（可选 pymupdf）")
    i.add_argument("path")

    sub.add_parser("demo", help="用自带示例跑通全流程")
    a = ap.parse_args(argv)

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    example = os.path.join(here, "examples", "questions.json")

    if a.cmd == "inspect":
        if not os.path.isfile(a.path):
            print("文件不存在: " + a.path, file=sys.stderr)
            return 2
        ok, payload = pdfinspect.inspect(a.path)
        print(pdfinspect.summarize(payload) if ok else "[跳过] " + payload)
        return 0

    src = example if a.cmd == "demo" else a.path
    if not os.path.isfile(src):
        print("文件不存在: " + src, file=sys.stderr)
        return 2
    try:
        data = schema.load(src)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}", file=sys.stderr)
        return 2
    errors = schema.validate(data)
    if errors:
        print("输入校验未通过：")
        for e in errors:
            print("  - " + e)
        return 1
    if a.cmd == "validate":
        print(f"✅ 校验通过：{len(data['questions'])} 题 / {len(data.get('knowledge_web', []))} 个知识点")
        return 0
    outdir = os.path.join(here, "out") if a.cmd == "demo" else a.out
    paths = builder.write_outputs(data, outdir)
    print("✅ 备课包已生成：")
    for k, p in paths.items():
        print(f"   {k:14s} {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
