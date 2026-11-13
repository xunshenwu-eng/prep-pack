# 更新记录

## [1.0.0] - 2026-11-13

### 新增
- 四段式讲义生成（题干重述 / 逐题解析 / 知识点网 / 讲授课话术），输出 md + html + outline.json。
- JSON 输入逐字段校验，缺项给出明确报错。
- 极简标准库 Markdown→HTML 渲染，打印友好样式。
- 可选 `pymupdf` PDF 判型，缺失时优雅降级不中断。
- `demo` / `validate` / `build` / `inspect` 四个子命令，13 项自测。
