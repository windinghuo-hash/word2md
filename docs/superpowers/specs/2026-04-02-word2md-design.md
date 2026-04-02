# Word2Md 设计文档

## 项目概述

Word2Md 是一个命令行工具，用于在 Microsoft Word（.docx）和 Markdown（.md）格式之间进行高保真双向转换。

## 目标用户

技术文档编写者、开发者，需要在 Word 和 Markdown 之间转换文档的用户。

## 核心需求

1. **双向转换**：支持 Word → Markdown 和 Markdown → Word
2. **格式支持**：
   - 基础格式：标题、粗体、斜体、列表、链接、图片
   - 表格：包括复杂表格（合并单元格）
   - 代码块：行内代码和代码块，带语法高亮标记
3. **图片处理**：支持提取为独立文件，或不提取图片
4. **单文件转换**：每次转换一个文件
5. **高保真**：尽可能保留所有细节，正确处理复杂特性
6. **技术栈**：Python

## 技术方案选择

**选定方案：纯 Python 实现**

核心库：
- `python-docx`：读写 Word 文档
- `mistune` 或 `markdown-it-py`：解析和渲染 Markdown

理由：
- 完全控制转换过程，满足高保真要求
- 无外部依赖，部署简单
- 易于调试和定制
- Python 生态成熟，库支持完善

## 整体架构

采用分层架构，将解析和渲染分离，使用统一的抽象语法树（AST）表示文档结构：

```
CLI 层 (word2md.py)
    ↓
转换器层 (converters/)
    ├── docx_to_md.py    # Word → Markdown
    └── md_to_docx.py    # Markdown → Word
    ↓
解析器层 (parsers/)
    ├── docx_parser.py   # 解析 Word 文档结构
    └── md_parser.py     # 解析 Markdown 语法树
    ↓
渲染器层 (renderers/)
    ├── md_renderer.py   # 生成 Markdown 文本
    └── docx_renderer.py # 生成 Word 文档
    ↓
工具层 (utils/)
    ├── image_handler.py # 图片提取/嵌入
    └── table_handler.py # 表格转换
```

核心思想：解析和渲染分离，中间用统一的 AST 表示文档结构，两个转换方向复用解析和渲染逻辑。

## 核心组件

### 1. DocxParser（Word 文档解析器）

**职责**：将 Word 文档解析为统一的 AST

**输入**：`.docx` 文件路径

**输出**：文档 AST

**实现细节**：
- 使用 `python-docx` 打开文档
- 遍历 `document.paragraphs` 和 `document.tables`
- 识别段落类型：
  - 标题：通过 `paragraph.style.name`（如 'Heading 1'）
  - 列表：通过 `paragraph.style.name`（如 'List Bullet'）
  - 代码块：通过字体族（`Courier New` 或 `Consolas`）或自定义样式
- 提取行内样式：遍历 `paragraph.runs`，检查 `run.bold`、`run.italic`
- 处理图片：从 `document.inline_shapes` 提取

### 2. MarkdownParser（Markdown 解析器）

**职责**：将 Markdown 文本解析为统一的 AST

**输入**：`.md` 文件内容

**输出**：文档 AST

**实现细节**：
- 使用 `mistune` 或 `markdown-it-py` 解析 Markdown
- 转换为统一的 AST 格式
- 识别 GFM 表格、代码块、图片等扩展语法

### 3. 统一 AST 结构

```python
Node = {
    'type': 'heading' | 'paragraph' | 'list' | 'table' | 'code_block' | 'image',
    'content': ...,
    'attrs': {'level': 1, 'bold': True, ...}
}
```

**节点类型**：
- `heading`：标题，attrs 包含 `level`（1-6）
- `paragraph`：段落，content 为 runs 列表
- `list`：列表，attrs 包含 `ordered`（布尔值）
- `table`：表格，content 为二维数组
- `code_block`：代码块，attrs 包含 `language`
- `image`：图片，attrs 包含 `path`、`alt`

### 4. MarkdownRenderer（Markdown 渲染器）

**职责**：将 AST 转换为 Markdown 文本

**输入**：文档 AST

**输出**：Markdown 文本

**实现细节**：
- 遍历 AST，生成符合 CommonMark 规范的 Markdown
- 表格使用 GFM 格式
- 代码块使用三个反引号，保留语言标记

### 5. DocxRenderer（Word 渲染器）

**职责**：将 AST 转换为 Word 文档

**输入**：文档 AST

**输出**：`.docx` 文件

**实现细节**：
- 使用 `python-docx` 创建文档
- 应用内置样式（Heading 1-6）
- 设置字体和段落格式
- 插入表格和图片

## Word → Markdown 转换流程

### 1. 解析阶段

- 使用 `python-docx` 打开 `.docx` 文件
- 遍历 `document.paragraphs` 和 `document.tables`
- 识别段落类型（标题、列表、代码块）
- 提取行内样式（粗体、斜体）
- 处理图片

### 2. 图片处理

**提取模式（--extract-images）**：
- 创建 `{输出文件名}_images/` 目录
- 保存图片为 `image_001.png`、`image_002.jpg` 等
- AST 中记录相对路径

**不提取模式**：
- AST 中标记图片位置但不输出到 Markdown

### 3. 表格处理

- 遍历 `table.rows` 和 `row.cells`
- 检测表头（第一行是否加粗）
- 处理合并单元格：
  - 记录 `cell.merge` 信息
  - 在 Markdown 中用空单元格或注释标记
  - 添加警告注释：`<!-- 注意：此表格包含合并单元格 -->`

### 4. 渲染阶段

- 将 AST 转换为 Markdown 语法
- 表格使用 GFM 格式
- 代码块使用三个反引号，保留语言标记（如果有）

## Markdown → Word 转换流程

### 1. 解析阶段

- 使用 `mistune` 或 `markdown-it-py` 解析 Markdown
- 构建 AST，识别标题、列表、代码块、表格、图片

### 2. 图片处理

- 解析图片路径（相对路径或绝对路径）
- 读取图片文件，使用 `document.add_picture()` 嵌入
- 如果图片不存在，插入占位符文本：`[图片缺失: path/to/image.png]`

### 3. 表格处理

- 解析 Markdown 表格为二维数组
- 使用 `document.add_table()` 创建 Word 表格
- 第一行设置为表头样式（加粗）
- 应用对齐方式（如果 Markdown 中有 `:---:` 等标记）

### 4. 渲染阶段

- 使用 `python-docx` 创建新文档
- 遍历 AST，逐个添加段落、表格、图片
- 应用样式：
  - 标题使用内置样式 `Heading 1-6`
  - 代码块使用等宽字体（`Courier New`）
  - 粗体/斜体通过 `run.bold`/`run.italic` 设置

## 命令行接口

### 命令格式

```bash
word2md <input_file> [options]
```

### 参数

- `input_file`：输入文件路径（`.docx` 或 `.md`）
- `-o, --output`：输出文件路径（可选，默认为输入文件名改扩展名）
- `--extract-images`：提取图片为独立文件（默认关闭）
- `--images-dir`：图片保存目录（默认为 `{输出文件名}_images/`）
- `--verbose`：显示详细转换信息
- `--version`：显示版本号

### 使用示例

```bash
# Word → Markdown（不提取图片）
word2md document.docx

# Word → Markdown（提取图片）
word2md document.docx --extract-images

# Markdown → Word
word2md readme.md -o output.docx

# 指定图片目录
word2md doc.docx --extract-images --images-dir ./assets
```

### 自动检测转换方向

根据输入文件扩展名自动判断：
- `.docx` → 转换为 `.md`
- `.md` → 转换为 `.docx`

## 错误处理

### 1. 文件错误

- **文件不存在**：显示清晰错误信息，退出码 1
- **文件格式错误**（损坏的 `.docx`）：捕获 `python-docx` 异常，提示用户
- **权限错误**：提示无法读取/写入文件

### 2. 转换错误

**不支持的特性**（如数学公式、文本框）：
- 记录警告信息到 stderr
- 在输出中插入注释标记：`<!-- 不支持的特性：文本框 -->`
- 继续转换其他内容

**复杂表格**（合并单元格）：
- 尽力转换，在 Markdown 中用注释说明限制
- 例如：`<!-- 注意：此表格包含合并单元格，可能显示不完整 -->`

### 3. 图片错误

- **图片文件不存在**（Markdown → Word）：
  - 插入占位符文本：`[图片缺失: path/to/image.png]`
  - 记录警告但继续转换
- **图片格式不支持**：尝试转换或跳过

### 4. 日志和调试

- **默认模式**：只显示错误和警告
- **--verbose 模式**：显示每个元素的转换过程
- 所有错误和警告输出到 stderr，正常信息输出到 stdout

### 退出码

- `0`：成功
- `1`：文件错误或致命错误
- `2`：转换完成但有警告

## 测试策略

### 1. 单元测试

- 测试每个解析器和渲染器的独立功能
- 测试 AST 节点的创建和转换
- 测试图片处理、表格处理等工具函数
- 使用 `pytest`，覆盖率目标 80%+

### 2. 集成测试

**测试文档集**：
- `test_basic.docx`：基础格式（标题、粗体、斜体、列表）
- `test_table.docx`：各种表格（简单表格、表头、对齐）
- `test_code.docx`：代码块和行内代码
- `test_images.docx`：包含图片的文档
- `test_complex.docx`：混合所有特性

**测试方法**：
- 对应的 `.md` 文件作为预期输出
- 测试双向转换：Word → Markdown → Word，检查信息损失

### 3. 边界测试

- 空文档
- 超大文档（1000+ 段落）
- 特殊字符（中文、emoji、特殊符号）
- 嵌套列表（3 层以上）
- 复杂表格（合并单元格、嵌套表格）

### 4. 回归测试

- 保存用户报告的问题文档作为测试用例
- 每次修复 bug 后添加对应测试

### 测试文件结构

```
tests/
├── unit/
│   ├── test_docx_parser.py
│   ├── test_md_parser.py
│   └── test_renderers.py
├── integration/
│   ├── test_docx_to_md.py
│   └── test_md_to_docx.py
└── fixtures/
    ├── test_basic.docx
    ├── test_basic.md
    └── ...
```

## 项目结构

```
word2md/
├── word2md.py              # CLI 入口
├── converters/
│   ├── __init__.py
│   ├── docx_to_md.py
│   └── md_to_docx.py
├── parsers/
│   ├── __init__.py
│   ├── docx_parser.py
│   └── md_parser.py
├── renderers/
│   ├── __init__.py
│   ├── md_renderer.py
│   └── docx_renderer.py
├── utils/
│   ├── __init__.py
│   ├── image_handler.py
│   └── table_handler.py
├── tests/
│   └── ...
├── requirements.txt
└── README.md
```

## 依赖库

```
python-docx>=0.8.11
mistune>=3.0.0
Pillow>=10.0.0
pytest>=7.0.0
```

## 实现优先级

### Phase 1：基础功能
1. 项目结构搭建
2. CLI 框架（参数解析）
3. 基础格式转换（标题、段落、粗体、斜体）
4. 单元测试框架

### Phase 2：核心特性
1. 列表支持（有序、无序、嵌套）
2. 链接和图片（不提取模式）
3. 代码块（行内和块级）
4. 集成测试

### Phase 3：高级特性
1. 表格支持（简单表格）
2. 图片提取模式
3. 复杂表格（合并单元格）
4. 错误处理和日志

### Phase 4：优化和完善
1. 边界测试
2. 性能优化
3. 文档和示例
4. 发布准备

## 未来扩展

- 支持更多 Markdown 方言（如 MultiMarkdown）
- 批量转换模式
- 配置文件支持
- 样式映射自定义
- GUI 界面
