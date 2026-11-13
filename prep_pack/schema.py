# -*- coding: utf-8 -*-
"""输入校验：宁可报错，不静默生成残缺讲义。"""
import json

ROOT_REQUIRED = ("subject", "grade", "topic", "questions")
QUESTION_REQUIRED = ("stem", "answer")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["根节点必须是对象"]
    for k in ROOT_REQUIRED:
        if k not in data or data[k] in ("", None, []):
            errors.append(f"缺必填字段: {k}")
    qs = data.get("questions")
    if qs is not None:
        if not isinstance(qs, list):
            errors.append("questions 必须是数组")
        else:
            for i, q in enumerate(qs, 1):
                if not isinstance(q, dict):
                    errors.append(f"第 {i} 题必须是对象")
                    continue
                for k in QUESTION_REQUIRED:
                    if not str(q.get(k, "")).strip():
                        errors.append(f"第 {i} 题缺字段: {k}")
    kw = data.get("knowledge_web", [])
    if kw and not isinstance(kw, list):
        errors.append("knowledge_web 必须是数组")
    return errors
