# 工具链：探测、安装与复核

以下本机记录是点时刻验证，不能代替每次运行时的路径和能力探测。命令示例使用 PowerShell；本文件的相对路径均以 **skill 目录**（含 `SKILL.md`、`scripts/` 和 `requirements.txt`）为工作目录。

## 1. Python 环境

有 Conda 时创建或复用 `agent`，新建环境使用 Conda 默认目录，不为本 skill 修改全局目录配置；无 Conda 时直接用本地 Python。安装步骤见仓库根目录 README。最低 Python 3.10，推荐 3.11。

```powershell
conda info --envs
conda config --show envs_dirs
conda run -n agent python -c "import sys; print(sys.executable); print(sys.version)"
conda run -n agent python -m pip install -r requirements.txt
conda run -n agent python -m pip check
```

- 不存在 `agent` 时先 `conda create --name agent python=3.11 pip`，核对安装计划的位置再执行；已有环境先核对解释器，不覆盖重建。
- 本机 `agent` 位于 `D:\anaconda\envs\agent`，也可直接调用 `D:\anaconda\envs\agent\python.exe`。Conda 可能因目录不可写回退到 C 盘，必须检查实际位置；本机 D 盘目录写入需要 Windows 管理员权限。
- 无 Conda 时把 `conda run -n agent python` 换成选定的本地 `python`。不要在一个解释器安装、另一个解释器运行。
- 后续常用 Python 依赖装入 `agent`，不向 base 新增包；自带脚本使用 `requirements.txt` 中的版本。变更该清单后须重新验证。
- 基础文本或图片处理不依赖网络；需要安装时遵守当前环境权限。错误或 PATH 告警应结合退出码、实际导入和 `pip check` 判断。

## 2. PDF 全文与原图：PyMuPDF

必需依赖为 `PyMuPDF==1.26.5`，使用 `import pymupdf`，不安装同名的无关 `fitz` 包。PyMuPDF 自带 PDF 渲染器，不依赖 `pdftoppm`；系统缺少 Poppler 不阻碍这条提图链路。

### 2.1 抽取全文与页面信息

```powershell
conda run -n agent python scripts/pdf_figures.py inspect --pdf "F:\path\paper.pdf" --output "$env:TEMP\paper-inspect"
```

输出 UTF-8 `paper.txt` 和 `pages.json`，包含 1-based PDF 页码、文本块、嵌入图片数与矢量路径数。双栏阅读顺序、公式和表格仍需核看页面；文本块坐标为未旋转 PDF 坐标，不能直接当作后续显示页面的裁剪比例。

**`get_images()` 只统计嵌入位图，不表示论文有多少张图。** 坐标轴、曲线、文字等可能全部为 PDF 矢量对象；返回零不等于论文无图。对象数量也不等于图数量，页边线同样可能产生矢量路径。

### 2.2 渲染整页确定图的边界

```powershell
conda run -n agent python scripts/pdf_figures.py render --pdf "F:\path\paper.pdf" --page 2 --output "$env:TEMP\paper-page2.png"
```

默认 144 DPI。打开该页面，定位需要的图，确认子图、坐标轴、图例和图注边界。选择关键图和边界由阅读者判断，脚本不自动识别论文语义。

### 2.3 导出原图区域并保留来源

```powershell
conda run -n agent python scripts/pdf_figures.py extract --pdf "F:\path\paper.pdf" --page 2 --clip 0.10 0.15 0.90 0.55 --figure "Figure 1" --output "F:\vault\topic\images\paper-fig1.png"
```

页码和裁剪框仅作格式示例，不能不看页面直接照用。

- `--clip` 为左、上、右、下四个 0–1 比例，坐标基于**旋转后的页面显示方向**，原点在左上。左右、上下必须有序，不能越界；不要直接传像素或 PDF 点值。
- 默认 300 DPI，可用 `--dpi` 在 72–600 内调整；不改变图像内容，不重新绘制曲线或符号。图中位图部分本身分辨率低时，提高 DPI 不会恢复丢失的信息。
- 导出 PNG 与同名 JSON，记录源 PDF 路径及 SHA-256、图号、PDF 页码、裁剪框、像素尺寸、DPI、PyMuPDF 版本和图片 SHA-256。`--caption` 可记录核实过的图注，不自动生成。
- 以 `<论文标识>-fig<图号>.png` 命名，放入目标笔记同级 `images/`。脚本默认拒绝覆盖，确需替换才用 `--force`。
- 核看 PNG，再在笔记中嵌入并补来源说明。原图合格条件和无图例外见 `paper.md` 与 `testing.md`。
- 对加密 PDF 使用用户可读取的解锁副本；缺全文、读取失败或图模糊时明确报告，不能作为无图例外。
- 文本与整页预览放临时目录；最终笔记只保留必要图片及来源记录，不堆全文抽取文件。

### 2.4 选择理由与验证记录

本机验证日期：2026-10-22。环境为 `D:\anaconda\envs\agent`、Python 3.11.17、PyMuPDF 1.26.5；安装与导入完成，`pip check` 通过。

选择页面区域渲染而非只用 `extract_image()`，是因为该方法能够保留整幅图中的矢量对象、文字、位图与遮罩。仍需人工或视觉模型判断边界；这是可控的原图提取流程，不是自动选图系统。

已在该环境执行全文抽取、整页渲染、裁剪导出与 PNG 视觉核验：

| 本地样本 | 原图位置与裁剪框 | 300 DPI 输出 | 核验结果 |
| --- | --- | --- | --- |
| `F:\Store\文献\GPTQ.pdf`，16 页 | Fig. 2，PDF 第 4 页；`0.502 0.558 0.83 0.875` | 837 × 1047 PNG | 机制图、图例和完整图注保留；该 PDF 所有页的嵌入位图数均为零，验证了矢量图链路 |
| `F:\Store\文献\smoothquant.pdf`，13 页 | Fig. 2，PDF 第 2 页；`0.085 0.08 0.485 0.42` | 1021 × 1122 PNG | 两组子图、标签、曲线和完整图注保留；来源页面同时含位图与矢量对象 |

以上坐标仅适用于本机这两份 PDF，其他版本须重新定位。两张图的源文件 / 图片 SHA-256、页数和像素尺寸均与 JSON 对应。另用合成页面检查旋转 90° 后的裁剪像素与整页对应区域完全一致，及无文本层位图 PDF 的导出；共通过 23 项功能 / 异常输入检查，涵盖中文路径、拒绝隐式覆盖、显式覆盖、页码越界、非法 / NaN 裁剪框、无效 DPI、非 PDF、加密 PDF、缺失输入及保护源文件。

验证产物保存在本机临时目录 `C:\Users\Administrator\AppData\Local\Temp\knowledge-curator-review-20261022\verification\`，不作为 skill 的运行依赖。已核看 PNG；本次未在 Obsidian 中执行嵌入显示验证，不能将其算作已通过。

## 3. OCR 与视觉核验

先探测本机工具 / 模型。文本层 PDF 优先直接抽取；扫描页或图片中的公式、代码和表格，可用本地 OCR 辅助，并对照原图核实。

本机此前探测到 Ollama 的 `glm-ocr:latest`、`MedAIBase/PaddleOCR-VL:0.9b`，使用前需再次确认服务与模型可用。模型存在不代表识别准确；OCR 输出不得替代论文原图，不确定处要标注。

图太复杂时保留原图并按可核验内容解释，不强行编造识别结果。没有本地 OCR 也可先完成 PDF 原页渲染与提图；未经用户授权不上传文档到额外外部 OCR 服务。

## 4. 绘图与检索

自绘图遵循 `diagram.md`；draw.io / Graphviz / Obsidian 插件按任务探测，不能由一次 PATH 缺失推断永久不可用。事实核查优先源材料，必要时使用可用的检索工具并保留支撑结论的来源。
