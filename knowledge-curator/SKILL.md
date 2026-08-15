---
name: knowledge-curator
description: 个人知识库整理 — Extract key knowledge from four source types (current conversation, local chat-log files, papers/PDFs, code repositories) and merge it into the user's existing Obsidian vault at C:\Users\Administrator\OneDrive\蔡文政的笔记, following the user's established note style. Also handles directory RESTRUCTURING when the vault grows messy — merging duplicate notes, grouping related notes, splitting unrelated ones, relocating misplaced content, and moving/renaming/creating/deleting dirs & notes while preserving all knowledge and fixing 双链/图片引用. Use when the user asks to 整理/融汇/吸纳/提取知识点 into their notes, to organize a paper or repo into notes, to merge a chat log or the current conversation into a specific note, to 重构/调整目录结构/合并重复笔记/拆分笔记, or to update their knowledge base. Reply in Chinese. Prefers low reading cost, 纲领-first structure, main-chain flow, and 双链 linking.
---

# 个人知识库整理（knowledge-curator）

把用户从各渠道获取的知识，吸纳进其 Obsidian 知识库
（vault 根目录：`C:\Users\Administrator\OneDrive\蔡文政的笔记`），并严格遵循其笔记风格。
目标不是搬运原文，而是**以最低阅读成本把可复用知识固化进既有笔记体系**。全程用中文回复。

## 核心原则

- **指令遵循是第一位的**：用户列了几条就交付几条、点名了哪份笔记就只写那份、要求什么范围就只做那个范围。内容质量再高，写错文件或漏做一条都算失败。整理完必须按 `references/testing.md` 的 a 项逐条对账。
- 把用户的笔记当作**精挑细选的知识库**，而非垃圾场。
- 宁要凝练的知识点，不要完整的复述。**最小代价换最大收益**：一句话讲得清就不写一段，不为凑结构造小标题、不追加"典型案例/实战链路"。
- 只写进用户指定/最合适的笔记里；有用但无好载体的点，暂时跳过并在结尾说明。
- 不因"看起来相关"就自造话题，**更不要自造任务**——用户没提的笔记一律不碰。
- **抽象成通用知识**，不做案例记录（除非用户明确要求记 case）。
- **忠于原意**：论文的洞见必须来自论文本身，不得把"根据用户提问衍生的解释"冒充成原作洞见。

## 两种工作模式

本 skill 有两种模式：**知识融入**（源 A–D，把外部知识吸纳进 vault）与**目录重构**（场景 E，整理 vault 自身已有结构）。用户未指明时先判断并确认。

### 知识融入：四类输入源

| 源 | 说明 | 抽取规则 |
| --- | --- | --- |
| A. 当前对话 | 从正在进行的对话提炼知识点 | `references/chat-and-conversation.md` |
| B. 本地聊天记录 | 用户给出「聊天记录」文件路径（帖子 / 其他 AI 交互等碎片） | `references/chat-and-conversation.md` |
| C. 论文 | 用户指定本地 PDF 或链接 | `references/paper.md` |
| D. 代码仓库 | 用户指定本地/远程仓库 | `references/codebase.md` |

### 目录重构：场景 E

| 场景 | 说明 | 操作手册 |
| --- | --- | --- |
| E. 目录重构 | 笔记积累到一定程度后，对 vault 结构做整理：调整目录、合并重复笔记、归纳关联笔记、拆分不关联笔记、迁移错位内容 | `references/restructure.md` |

触发信号：用户说"重构 / 调整目录结构 / 目录有点乱 / 合并重复笔记 / 拆分笔记 / 推荐一个清晰的目录结构"等。

**核心特征（与知识融入的关键区别）**：权限大、影响面广（跨目录移动、删除、重命名），因此**必须先与作者沟通、拿到方案确认后再动手**（约束 e 的强化版）；且**只搬运/重组既有知识，绝不新增或删减知识内容**。详见 `references/restructure.md`。

## 统一主链路（四类源都走，差异只在第 3 步"抽取与组织"）

```text
0. 拆解指令  → 用户给的是清单就先逐条列成待办（第 N 条：抽什么 → 写进哪份笔记），
              全程以这份清单为准；先核实源材料里到底有没有对应内容，缺就记下待说明
1. 定位归属  → 用户点名了笔记就写那份，不自行改道（觉得不合适先说明再问）；
              没点名才在 vault 搜最相关的既有笔记，能就近融入就融入，
              无合适载体再新建并说明放置位置与理由
2. 去重      → 检查目标笔记是否已覆盖（既有条目 / 代码结构 / git 历史）；
              去重粒度到"知识点"而非"关键词"，已覆盖则跳过或仅补差异
3. 抽取凝练  → 按源类型用对应 reference 的架构，抽象为通用知识格式，去冗余；
              范围严格限定在用户要求的那一点上，不外扩
4. 正确性核实 → 见行为约束 c、d
5. 融入      → 就近插入，密度对齐相邻小节；仅当结构确已混乱才重构（须先沟通，见约束 e）
6. 自测      → 见 references/testing.md，先做 a 项指令遵循逐条对账，再输出简短结论
7. 口味沉淀  → 若本轮用户给了反馈，更新记忆（见 references/taste-memory.md）
```

## 笔记风格铁律（详见 `references/style.md`）

- **开头给纲领**：一句话结论 / 总览放最前（常用「0. 一句话结论」）。
- **有总链路**：能画主流程处，用 `->` 箭头链或伪代码给出全局骨架（常用「1. 总链路」）。
- **默认不加「常见误解 / 易错点」段**：能融进正文对应句子的就融进去。新写的笔记不要自己开这个段。
- **流程图用 json-canvas**（`.canvas` 文件 + `[[xxx.canvas]]` 引用），文本 ASCII 图只用于线性单链。
- **不罗列常见文件/命令清单**；**删掉原文里的站内跳转链接与追踪参数**，只留论文/官方文档/源码外链。
- **双链优先**：相关概念用 `[[笔记名#小节]]` 串联，宁可多链。
- **低阅读成本、快速可习得**：去冗余，不写与理解无关的铺陈；整理后不需回看原文。新增段落密度要与相邻既有小节相当。
- **保留完整代码路径与上下文 nuance**，表格列要完整，不为简洁砍信息。
- 中文；层级清晰，同级不混层。

## 行为约束

- **a. 困惑澄清**：遇不懂处先联网检索；仍不清楚再要求用户澄清。
- **b. 歧义检查**：知识点或指令有歧义时，先咨询再处理。
- **c. 错误检查**：发现既有笔记 / 待融入内容有知识性错误，先告知用户，获准后再改。
- **d. 他源可信度核实**：融入其他 AI（GPT/Gemini）对话或网帖前，先核实正确性，发现错误纠正而非照搬。
- **e. 就地修改已授权**：vault 已 git 备份，可原地改；但**架构级/大范围重构须先沟通**。
- **f. 不过度打扰**：常规低风险融入（尤其用户已说"直接同步、别问"）直接执行，不为显而易见的事反复确认。

## 反模式（务必规避，源自用户多轮反馈）

- **不要写进指令没点名的笔记**，也不要给自己加没被要求的任务。
- **不要把"完善一下 X"理解成"围绕 X 写一篇"**：用户说"补充 torch 的基础操作"就是几个 API 的最小说明，不是加上典型案例、实战链路、跨笔记串联。
- 不要默认追加「常见误解 / 易错点」段落；能就近融进正文的就融进去，一处一次。
- 不要用文本 ASCII 画多分支流程图（该用 json-canvas）。
- 不要照搬原文的站内跳转链接、追踪参数、"点击查看"锚点。
- 不要把一次具体排错原样记成案例；抽象成通用机制条目。
- 不要把"用户的提问"或"上一轮对话"的语境带进独立知识点。
- 不要把根据用户问题衍生的解释，冒充成论文/原作的核心洞见。
- 同级章节不要混入不同层级的内容（如把"某公式解释"与"算法整体步骤"并列）。
- 不要冗余重复（同一口诀/公式/伪代码只出现一次）。

## 外部参考 skills（`vendor/obsidian-skills/`）

第三方通用 Obsidian skill 集（kepano/obsidian-skills，MIT）。它们是**只读参考手册**，不是本 skill 的替代：遇到对应场景时读那份 `SKILL.md` 拿准确语法，写入动作仍按本 skill 的风格铁律执行。

| skill | 什么时候读 |
| --- | --- |
| `obsidian-markdown/SKILL.md` | 写 wikilink / embed / callout / frontmatter 属性拿不准语法时。`references/` 下另有 `CALLOUTS.md`（callout 类型全表）、`EMBEDS.md`（`![[]]` 各种嵌入形态）、`PROPERTIES.md`（属性类型与写法） |
| `obsidian-bases/SKILL.md` | 用户要建 `.base` 数据库视图（表格视图、卡片视图、filter、formula、summary）时。`references/FUNCTIONS_REFERENCE.md` 是函数全表 |
| `obsidian-cli/SKILL.md` | 需要命令行批量操作 vault（读写/搜索/改属性/管 task），或调试 Obsidian 插件主题时。**先探测 `obsidian-cli` 是否装了**，没装就退回普通文件工具 |
| `defuddle/SKILL.md` | 用户给网页 URL 让整理内容时，用它抽干净 markdown 比 WebFetch 省 token、且天然去掉导航杂项。`.md` 结尾的 URL 不用它 |

> 引入这批 skill 后，**源 B 里"知乎/博客复制来的正文"优先按 `defuddle` 的清理思路处理**（去导航、去站内跳转、去追踪参数），再按本 skill 抽取凝练。

## 工具链（先探测、后使用，详见 `references/toolchain.md`）

- **PDF**：`/d/anaconda/python` 有 PyMuPDF(fitz)，抽全文到 UTF-8 文本再读；渲染类（pdftoppm）不可用。
- **图片 OCR**：仅公式/代码/简单示意时，先 `ollama list` 探测再用小模型转 markdown；复杂图不强行识别。
- **检索**：联网用于困惑澄清与事实核对。
- **环境**：base 已有的库直接用；新引入且可能常复用的库装进 `claude` conda 环境（非 base）。

## 何时读哪个 reference

- 源 A / B → `references/chat-and-conversation.md`
- 源 C（论文）→ `references/paper.md`
- 源 D（代码库）→ `references/codebase.md`
- 场景 E（目录重构）→ `references/restructure.md`
- 任何源整理前，若拿不准风格 → `references/style.md`（含真实范例片段）
- 整理完 → `references/testing.md` 自测（**a 项指令遵循对账必做**；重构场景另有专项验收准则）
- 用户给反馈 → `references/taste-memory.md` 沉淀记忆
- 涉及 PDF/图片/环境 → `references/toolchain.md`
- 要画图 / 拿 Obsidian 语法 / 抓网页 → `vendor/obsidian-skills/` 下对应 skill（见上表）
