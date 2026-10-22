# knowledge-curator

个人 Obsidian 知识库整理 skill，支持从对话、聊天记录、论文 PDF、代码仓库提取知识，以及笔记重构、绘图。所有产出遵循统一科研表达规范，强调来源可追溯、变量定义完整、结论条件明确和低阅读成本。

## 安装

需要 Python 3.10 或更新版本，推荐 Python 3.11。以下命令在本仓库根目录执行。

### 已安装 Conda

先查看 `conda info --envs` 与 `conda config --show envs_dirs`。没有 `agent` 时，在 Conda 默认环境目录创建；已有时复用并检查 Python 版本：

```powershell
conda create --name agent python=3.11 pip
conda run -n agent python -m pip install -r knowledge-curator/requirements.txt
conda run -n agent python -m pip check
conda run -n agent python -c "import sys, pymupdf; print(sys.executable); print(pymupdf.VersionBind)"
```

创建时核对 Conda 计划中的 `environment location` 再确认。`envs_dirs` 排第一不保证该目录可写，Conda 可能回退到其他目录。本机期望位置为 `D:\anaconda\envs\agent`；该目录受 Windows 权限保护，本次通过管理员进程创建。若运行账户使默认位置回退，可在有写权限的终端使用 `conda create --prefix D:\anaconda\envs\agent python=3.11 pip`，后续对应使用 `conda run -p D:\anaconda\envs\agent ...`。其他电脑使用自己的默认目录，不照抄 D 盘路径。

### 未安装 Conda

直接安装到当前本地 Python 环境，不要求为了本 skill 安装 Conda：

```powershell
python --version
python -m pip install -r knowledge-curator/requirements.txt
python -m pip check
python -c "import sys, pymupdf; print(sys.executable); print(pymupdf.VersionBind)"
```

如果系统 Python 明确禁止直接安装，先选择可写的本地 Python 环境；不强行绕过系统保护。安装与运行始终使用同一解释器。

### 安装 skill 与配置笔记库

将仓库内的 `knowledge-curator/` 整个目录放入所用 agent 的 skills 目录，保留 `references/`、`scripts/`、`requirements.txt` 与 `vendor/`。在 `knowledge-curator/SKILL.md` 中把笔记库根目录改为自己的路径；按需配置 `references/taste-memory.md` 中的记忆位置。已有同名 skill 时先比较再更新，避免覆盖自定义内容。

`knowledge-curator/requirements.txt` 是自带 Python 脚本的必需依赖清单，目前仅含 PyMuPDF。OCR 模型、draw.io、Obsidian 插件是按任务探测的可选工具，不要求全量安装。常用新增 Python 依赖优先放入 `agent`，不改 Conda base。

## 论文原图提取

在仓库根目录执行；没有 Conda 时去掉命令前的 `conda run -n agent`：

```powershell
conda run -n agent python knowledge-curator/scripts/pdf_figures.py inspect --pdf "paper.pdf" --output "work/paper"
conda run -n agent python knowledge-curator/scripts/pdf_figures.py render --pdf "paper.pdf" --page 2 --output "work/page-2.png"
conda run -n agent python knowledge-curator/scripts/pdf_figures.py extract --pdf "paper.pdf" --page 2 --clip 0.10 0.15 0.90 0.55 --figure "Figure 1" --output "images/paper-fig1.png"
```

示例页码与裁剪框是占位示例，必须看过实际页面再确定。页码从 1 开始；裁剪框按页面显示方向，以左上角为原点，依次为左、上、右、下的归一化坐标。默认导出 300 DPI PNG 和同名 JSON 来源记录，同时保留原图中的矢量线条、文字和位图。程序不自动判定哪幅图最关键，也不自动验证图例是否裁全；必须核看输出。

论文知识提取笔记至少嵌入一张该论文原图；只有核验全文确实无图时才可例外。流程与本机验证记录见 [paper.md](knowledge-curator/references/paper.md) 和 [toolchain.md](knowledge-curator/references/toolchain.md)。

## 风格与验收

- [SKILL.md](knowledge-curator/SKILL.md)：任务范围、模式路由与授权边界。
- [style.md](knowledge-curator/references/style.md)：所有模式共用的科研风格定义，含变量、常量、下标、形状、单位及不变量。
- [diagram.md](knowledge-curator/references/diagram.md)：自绘科研图的格式、排版与可读性检查。
- [testing.md](knowledge-curator/references/testing.md)：通用验收及论文原图、重构、绘图专项验收。
