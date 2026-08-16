# 画图（drawio-skill）

风格铁律 12 的执行手册。**「1. 总链路」默认出图**，不再用 ASCII 文本画。

## 何时出图

| 情形 | 做法 |
| --- | --- |
| 「1. 总链路」 | **一律出图**（这是笔记的全局骨架，最该可视化） |
| 分支 / 汇聚 / 并行分支的流程 | 出图 |
| 节点 > 5 的结构、模块关系、数据流 | 出图 |
| 三四个节点的线性单链 | 保留 ASCII（`A -> B -> C`），出图反而是负担 |
| 纯对照关系（A 与 B 的差异） | 用**表格**，不出图 |

判据同「最小代价换最大收益」：图要能替代一段文字，而不是给文字配插画。

## 产出格式（本机 Obsidian 强约束）

vault 装的是 `drawio` 插件 v3.1.1（`somesanity` 版，非 `drawio-editor`）。它**只识别 `.drawio.svg`**（`main.js` 里 `endsWith(".drawio.svg")` 出现 16 次），纯 `.drawio` 不预览。

因此每张图产出**两个文件**，都放笔记同级 `images/`：

```text
<笔记同级>/images/
├── <图名>.drawio        # 源文件，便于 diff / 重生成 / validate.py 打分
└── <图名>.drawio.svg    # 嵌入用：SVG 的 content 属性内嵌完整 mxfile，可预览且双击可编辑
```

笔记里用相对短链接（同 vault 内唯一即可，不写全路径）：

```markdown
## 1. 总链路

![[<图名>.drawio.svg]]

<一句话说明图与正文章节的对应关系>
```

图名用 `<笔记名> <图的主题>`（如 `HAWQ-V2 总链路`），不要用插件默认的 `Untitled Diagram <timestamp>`。

## 生成方式

**不要手写 SVG 里的坐标**。写一个临时 Python 脚本，把节点/边/旁注定义成数据结构，同时吐出 `.drawio` 与 `.drawio.svg`——两者共用同一份布局数据，不会漂移。参考实现：`C:\Users\Administrator\AppData\Local\Temp\gen_hawq_drawio.py`（HAWQ-V2 总链路那张）。

`.drawio` XML 的写法（骨架、样式关键字、edge 必须带 `<mxGeometry relative="1">`、连接点分布、间距表）读 `~/.claude/skills/drawio-skill/references/xml-authoring.md`，不要凭记忆写。

内嵌进 SVG `content` 属性的 mxfile 要**去掉 XML 声明行、压成单行**，再用 `quoteattr` 转义。

## 本机环境限制

- **`drawio` / `draw.io` CLI 不在 PATH** → skill 的 PNG/SVG/PDF 导出功能不可用，所以 SVG 必须自己渲染（这也是上面"脚本同时吐两个文件"的原因）。
- **Graphviz `dot` 未装** → `scripts/autolayout.py` 不可用，坐标靠手算 + `validate.py --score` 验收。
- 纯 Python 的脚本可用：`validate.py`（结构 lint + 可读性打分）、`edgeports.py`、`restyle.py`、`explain.py`、`compress.py`。

## 验收

```bash
PYTHONIOENCODING=utf-8 /d/anaconda/python \
  ~/.claude/skills/drawio-skill/scripts/validate.py --strict --score "<图>.drawio"
```

要求 **0 error / 0 warning**，且 `score` 尽量为 0（`score` 由穿越顶点、边交叉、顶点重叠三项加权，越低越好）。非 0 就调坐标重生成，别凑合。

再校验 SVG 与内嵌 mxfile 都能被 XML 解析器解析（`ET.parse` + `ET.fromstring(root.get('content'))`），确保插件能读出可编辑图。

## 排版约定

- 主干竖向排列、居中对齐（`exitX=0.5;exitY=1` → `entryX=0.5;entryY=0`），主干箭头带一到两字的动作标签（如 `指标`/`估计`/`选点`）。
- 各步的**代价、反例、前提**放右侧虚线框（`dashed=1;fillColor=none`），灰色虚线横向挂在对应主干框上——主干读流程，横向读"凭什么成立/代价多少"。
- 语义配色用 `drawio-skill` 调色板：红=问题、蓝=分析、绿=决策、黄=外推、灰=结果。**3 种以上语义色必须加图例**，图例项从图里实际用到的角色机械生成。
- 上下标用 HTML 标签（`<sup>` / `<sub>`），公式不必转 LaTeX——drawio 的 `math=1` 依赖外部 MathJax，Obsidian 内嵌 SVG 时不生效。
