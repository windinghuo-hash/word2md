# Word2Md

Word 和 Markdown 之间的高保真双向转换命令行工具。

## 功能特性

- **双向转换**：Word (.docx) ↔ Markdown (.md)
- **格式支持**：标题（1-6 级）、粗体、斜体、有序/无序列表、代码块
- **表格支持**：自动识别单列代码块，多列表格支持 GFM / HTML 两种格式
- **图片提取**：将 Word 中嵌入的图片提取为独立文件，Markdown 中自动生成引用

## 安装

**依赖环境：** Python 3.8+

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# Word → Markdown（自动以同名输出）
python word2md.py document.docx

# Markdown → Word
python word2md.py readme.md

# 指定输出文件路径
python word2md.py document.docx -o output.md
python word2md.py readme.md -o output.docx
```

### 表格格式

通过 `--table-format` 选项控制表格的输出格式：

| 选项值 | 说明 | 适用场景 |
| ------ | ---- | -------- |
| `auto` | 自动选择（默认）：单元格有多行内容时用 HTML，否则用 GFM | 通用 |
| `gfm`  | 强制使用 GFM 表格，多行内容用 `<br>` 分隔 | GitHub、标准 Markdown 渲染器 |
| `html` | 强制使用 HTML `<table>`，多行内容用 `<p>` 段落 | 需要精确换行的场景 |

```bash
python word2md.py document.docx --table-format auto   # 默认
python word2md.py document.docx --table-format gfm
python word2md.py document.docx --table-format html
```

### 图片提取

```bash
# 提取图片到默认目录（{输出文件名}_images/）
python word2md.py document.docx --extract-images

# 提取图片到指定目录
python word2md.py document.docx --extract-images --images-dir ./assets
```

提取后，Markdown 中会自动生成图片引用：

```markdown
![图片1](document_images/image_001.jpeg)
![图片2](document_images/image_002.png)
```

不启用 `--extract-images` 时，图片位置显示为占位符：

```markdown
*[图片1（未提取）]*
```

### 完整参数列表

```
python word2md.py <input_file> [选项]

参数：
  input_file              输入文件路径（.docx 或 .md）

选项：
  -o, --output            输出文件路径（默认：同名改扩展名）
  --table-format          表格格式：auto / gfm / html（默认：auto）
  --extract-images        提取图片为独立文件
  --images-dir            图片保存目录（默认：{输出文件名}_images/）
  --verbose               显示详细转换信息
  --version               显示版本号
  -h, --help              显示帮助信息
```

### 综合示例

```bash
# 提取图片，使用 HTML 表格，输出详细日志
python word2md.py 需求文档.docx \
  --extract-images \
  --images-dir ./docs/images \
  --table-format html \
  --verbose
```

## 支持的文档特性

| 特性 | Word → Markdown | Markdown → Word |
| ---- | --------------- | --------------- |
| 标题（1-6 级） | ✅ | ✅ |
| 粗体 / 斜体 | ✅ | ✅ |
| 有序 / 无序列表 | ✅ | ✅ |
| 代码块 | ✅ | ✅ |
| 表格 | ✅ | ✅ |
| 图片 | ✅（需 --extract-images） | ✅ |
| 超链接 | — | — |

> **注意：** 无标准 Heading 样式的 Word 文档（如仅通过字体大小区分层级），工具会根据字体大小自动推断标题级别。

## 开发

```bash
# 运行测试
pytest tests/ -v

# 运行测试并查看覆盖率
pytest tests/ --cov=. --cov-report=html
```
