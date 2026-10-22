# knowledge-curator

🗡️个人 Obsidian 知识库整理 skill



# 🗡️一、功能

- 支持从 a). 历史对话、b). 聊天记录、c.) 论文 PDF、d). 代码仓库 提取知识点融入个人笔记。

- 支持笔记重构



# 🗡️ 二、安装



## 2.1 安装依赖

### 2.1.1 方式一：conda（推荐采用conda 构造虚拟环境用于agent工具调用） 

> 以下命令在本仓库根目录执行。

```powershell
conda create --name agent python=3.11 pip
conda run -n agent python -m pip install -r knowledge-curator/requirements.txt
conda run -n agent python -m pip check
conda run -n agent python -c "import sys, pymupdf; print(sys.executable); print(pymupdf.VersionBind)"
```



### 2.1.1 方式二：未安装 Conda

直接安装到当前本地 Python 环境，不要求为了本 skill 安装 Conda：

```powershell
python --version
python -m pip install -r knowledge-curator/requirements.txt
python -m pip check
python -c "import sys, pymupdf; print(sys.executable); print(pymupdf.VersionBind)"
```



## 2.2 skills安装与配置

将仓库内的 `knowledge-curator/` 整个目录放入所用 agent 的 skills 目录，保留 `references/`、`scripts/`、`requirements.txt` 与 `vendor/`。在 `knowledge-curator/SKILL.md` 中把笔记库根目录改为自己的路径；按需配置 `references/taste-memory.md` 中的记忆位置。

`knowledge-curator/requirements.txt` 是自带 Python 脚本的必需依赖清单，目前仅含 PyMuPDF。OCR 模型、draw.io、Obsidian 插件是按任务探测的可选工具，不要求全量安装。常用新增 Python 依赖优先放入 `agent`。



# 🗡️三、风格

> 笔记风格默认遵循科研表达规范。

指令示例：

![example_2](examples\example_2.png)

笔记成品样例如下：

![example_1](examples\example_1.png)
