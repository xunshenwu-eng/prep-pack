# prep-pack · 家教备课包生成器

> 收到的不是「答案」，而是**能当场讲出来的教学话术 + 一张兜住追问的知识网**。

把学生/家长临时发来的题目材料，快速加工成一份自己能现学现讲的备课包：
四段式讲义 + 知识点网 + 讲授课话术，输出 Markdown 与可直接打印的 HTML。

**核心功能零依赖**（Python 3.9+ 标准库）；只有 PDF 判型是可选增强，装了 `pymupdf` 才启用。

## 为什么做这个

知识库里有一篇《家教备课包生成器》技能笔记，记录了真实痛点：
本科生去给初高中生讲题，但自己对知识已经生疏；临时发来的往往是照片或扫描 PDF，
横跨多个学科。所以要交付的**不是答案**，而是：

1. **题干重述**——先确认材料读对了吗；
2. **逐题解析**——含易错点与依据；
3. **知识点网**——从「就题论题」扩到整章体系，兜住学生追问；
4. **讲授课话术**——能当场念出来的表达，而不是书面解答。

本工具把这个流程固化成一条命令，输入用 JSON（不依赖 YAML 解析器），输出 md + html。

## 安装

```bash
git clone https://github.com/xunshenwu-eng/prep-pack.git
cd prep-pack
python -m prep_pack --help
# 可选：PDF 判型增强
pip install pymupdf
```

## 用法

```bash
# 跑通自带示例
python -m prep_pack demo

# 校验题目文件
python -m prep_pack validate examples/questions.json

# 生成备课包
python -m prep_pack build examples/questions.json -o ./out

# PDF 判型（文本型 / 扫描型，逐页字数）
python -m prep_pack inspect ./paper.pdf
```

`inspect` 未安装 `pymupdf` 时会明确提示并给出安装命令，**不会让整条流程崩掉**。

## 输入格式（JSON）

```json
{
  "subject": "数学",
  "grade": "初三",
  "topic": "一元二次方程",
  "knowledge_web": ["判别式", "韦达定理", "根的分布"],
  "questions": [
    {
      "id": 1,
      "stem": "解方程 x²-5x+6=0",
      "answer": "x=2 或 x=3",
      "analysis": "因式分解 (x-2)(x-3)=0",
      "pitfalls": ["漏根", "不验判别式"],
      "talk": "先别急着套公式，看看能不能拆成两个括号相乘"
    }
  ]
}
```

字段要求：`subject` / `grade` / `topic` / `questions` 必填；每道题至少 `stem` 与 `answer`。
缺字段会给出逐项报错，不会静默生成残缺讲义。

## 输出

| 文件 | 内容 |
| --- | --- |
| `lesson.md` | 四段式讲义：题干重述 → 逐题解析 → 知识点网 → 讲授课话术 |
| `lesson.html` | 同内容的打印友好 HTML（A4 边距、题干高亮、话术底色） |
| `outline.json` | 结构化大纲，便于二次加工 |

## 项目结构

```
prep-pack/
├── prep_pack/
│   ├── cli.py        # 命令入口
│   ├── schema.py     # 输入校验
│   ├── builder.py    # 四段式讲义生成
│   ├── render.py     # 极简 Markdown → HTML（标准库）
│   └── pdfinspect.py # 可选 PDF 判型
├── templates/lesson.md
├── examples/questions.json
└── tests/
```

## 测试

```bash
python -m unittest discover -s tests -v
```

## 边界

- **不做 OCR**。扫描件需要先转图由视觉模型读，再手工把题干录进 JSON；`inspect` 只负责判型。
- **不自动解题**。`answer` / `analysis` 由人或模型填，工具只负责组织与排版，不编造答案。
- HTML 渲染只覆盖本工具生成的 Markdown 子集（标题/列表/表格/代码块/粗体），不是通用 Markdown 解析器。
- 示例题目为项目自带原创示例，不含任何真实学生材料。

## 许可

MIT。方法思想来自个人知识库的《家教备课包生成器》技能笔记，实现为原创。
