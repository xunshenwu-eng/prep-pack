# -*- coding: utf-8 -*-
"""可选 PDF 判型。无 pymupdf 时优雅降级，不中断主流程。"""


def available():
    try:
        import pymupdf  # noqa: F401
        return True
    except ImportError:
        try:
            import fitz  # noqa: F401
            return True
        except ImportError:
            return False


def inspect(path):
    """返回 (ok, payload)。payload 为逐页字数列表或提示文本。"""
    import os
    if not available():
        return False, ("未安装 pymupdf，跳过 PDF 判型。"
                       "安装：pip install pymupdf；扫描件仍需转图后由视觉模型读题干。")
    if not os.path.isfile(path):
        return False, f"文件不存在: {path}"
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    with pymupdf.open(path) as doc:
        pages = [len(pg.get_text().strip()) for pg in doc]
    return True, pages


def summarize(pages):
    if not pages:
        return "空文档"
    scanned = sum(1 for n in pages if n == 0)
    if scanned == len(pages):
        kind = "纯扫描件（必须转图后视觉读）"
    elif scanned:
        kind = f"混合型（{scanned} 页无文本层）"
    else:
        kind = "文本型（可直接读文本）"
    return f"{kind}；共 {len(pages)} 页，逐页字数 {pages}"
