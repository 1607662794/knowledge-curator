# 工具链（本机已验证可用的方式，先探测后使用）

## PDF 读取（论文）

本机 `/d/anaconda/python` 装了 PyMuPDF(fitz)。抽全文到 UTF-8 文本再读，**不要依赖渲染类工具**（pdftoppm 不可用；`Read` 工具对 PDF 走 pdftoppm 会失败）。

```bash
cd /tmp && /d/anaconda/python -c "
import fitz
d=fitz.open(r'F:/path/to/paper.pdf')
out=[]
for i,p in enumerate(d):
    out.append('===== PAGE %d ====='%(i+1)); out.append(p.get_text())
open(r'C:/Users/Administrator/paper_text.txt','w',encoding='utf-8').write('\n'.join(out))
print('OK pages=',d.page_count)
"
```

然后用 `Read` 读 `C:/Users/Administrator/paper_text.txt`。

注意事项：
- Git Bash 每次调用会把 cwd 重置、Python 解析可能不稳定，**用绝对路径 `/d/anaconda/python`**，别靠 PATH 里的 `python`。
- stdout 是 gbk 容易报 UnicodeEncodeError，所以**写文件用 `encoding='utf-8'`**、不要直接 print 大段中文。
- 若 `/d/anaconda/python` 无 fitz，用 `importlib.util.find_spec` 探测：base 里已确认有 `fitz` 和 `PyPDF2`。

## 图片 OCR（仅公式/代码/简单示意）

复用 `local-ocr-first` 的探测逻辑。先探测已装的本地模型：

```bash
ollama list
```

- 仅当图片是**公式 / 代码 / 简单示意**时，用 ollama 小模型 OCR 成 markdown 融入笔记（省 token、保隐私）。
- **过于复杂的图不强行识别**，避免表意不明；必要时以 `![[图片]]` 嵌入或标注引用。

## 检索

联网搜索用于：困惑澄清（约束 a）、他源事实核对（约束 d）。

## conda 环境

- base 环境已有的库（含 fitz、PyPDF2）**直接用**。
- 本次新引入、且后续可能常复用的库：装进 `claude` conda 环境（**不是 base**）：
  ```bash
  conda run -n claude pip install <lib>    # 或 conda install -n claude <lib>
  ```
- 一次性、几乎不会再用的库，临时用即可，不必固化安装。
