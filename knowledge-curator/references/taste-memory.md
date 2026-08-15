# 口味沉淀（横切能力）

当用户对某次梳理**不满意并说明原因**后，把可复用的偏好沉淀成一条记忆，让后续越来越懂用户。

## 记忆目录

`C:\Users\Administrator\.claude\projects\c--Users-Administrator-OneDrive-------\memory\`

每条记忆一个 `.md` 文件，并在同目录 `MEMORY.md` 加一行索引。

## feedback 类格式

```markdown
---
name: <简短中文名或 kebab-case-slug>
description: <一行摘要，用于召回时判断相关性>
type: feedback
---
<一句话结论：这条反馈要求我怎么做>

**Why:** <为什么——通常是用户对某次整理不满意的具体原因>

**How to apply:** <怎么落地——具体、可操作的步骤或清单>
```

在正文用 `[[其他记忆名]]` 链接相关记忆。

## 规则

- **先查重**：写前扫 `MEMORY.md` 与现有 feedback 记忆，已有同类则**更新**而非新建。
- **冲突处理**：新偏好与旧记忆冲突时，**先向用户确认以哪条为准**，再改。
- **只存可跨任务复用的偏好**，不存一次性个案细节。若用户要记的是个案，问清"这里面什么是可泛化的"，只沉淀那部分。
- 写完在 `MEMORY.md` 加索引行：`- [标题](file.md) — 一句话钩子`。

## 已有相关记忆（示例，实际以目录为准）

- `笔记整理格式偏好`（feedback_note_format.md）— 结构/代码路径/收尾风格
- `刷题自动同步`（feedback_auto_sync.md）— 直接同步别问
- `融汇前先核实他模型对话`（feedback_verify_other_model_chat.md）— 他源先核实
