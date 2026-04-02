# Word2Md 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个命令行工具，实现 Word 和 Markdown 之间的高保真双向转换

**Architecture:** 分层架构，使用统一的 AST 作为中间表示，将解析和渲染分离。支持基础格式、表格、代码块和图片处理。

**Tech Stack:** Python 3.8+, python-docx, mistune, Pillow, pytest

---

## 文件结构规划

```
word2md/
├── word2md.py              # CLI 入口
├── converters/
│   ├── __init__.py
│   ├── docx_to_md.py      # Word → Markdown 转换器
│   └── md_to_docx.py      # Markdown → Word 转换器
├── parsers/
│   ├── __init__.py
│   ├── docx_parser.py     # Word 文档解析器
│   └── md_parser.py       # Markdown 解析器
├── renderers/
│   ├── __init__.py
│   ├── md_renderer.py     # Markdown 渲染器
│   └── docx_renderer.py   # Word 渲染器
├── utils/
│   ├── __init__.py
│   ├── ast_nodes.py       # AST 节点定义
│   ├── image_handler.py   # 图片处理
│   └── table_handler.py   # 表格处理
├── tests/
│   ├── unit/
│   │   ├── test_docx_parser.py
│   │   ├── test_md_parser.py
│   │   ├── test_md_renderer.py
│   │   └── test_docx_renderer.py
│   ├── integration/
│   │   ├── test_docx_to_md.py
│   │   └── test_md_to_docx.py
│   └── fixtures/
│       ├── test_basic.docx
│       └── test_basic.md
├── requirements.txt
└── README.md
```

---

## Task 1: 项目结构和依赖

**Files:**
- Create: `requirements.txt`
- Create: `README.md`
- Create: `converters/__init__.py`
- Create: `parsers/__init__.py`
- Create: `renderers/__init__.py`
- Create: `utils/__init__.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
python-docx>=0.8.11
mistune>=3.0.0
Pillow>=10.0.0
pytest>=7.0.0
```

- [ ] **Step 2: 创建 README.md**

```markdown
# Word2Md

Word 和 Markdown 之间的高保真双向转换工具。

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
# Word → Markdown
python word2md.py document.docx

# Markdown → Word
python word2md.py readme.md
```
```

- [ ] **Step 3: 创建目录结构**

```bash
mkdir -p converters parsers renderers utils tests/unit tests/integration tests/fixtures
touch converters/__init__.py parsers/__init__.py renderers/__init__.py utils/__init__.py
```

- [ ] **Step 4: 安装依赖**

```bash
pip install -r requirements.txt
```

Expected: 所有依赖成功安装

- [ ] **Step 5: 提交**

```bash
git add requirements.txt README.md converters/ parsers/ renderers/ utils/ tests/
git commit -m "chore: initialize project structure and dependencies"
```

---

## Task 2: AST 节点定义

**Files:**
- Create: `utils/ast_nodes.py`
- Create: `tests/unit/test_ast_nodes.py`

- [ ] **Step 1: 编写 AST 节点测试**

```python
# tests/unit/test_ast_nodes.py
import pytest
from utils.ast_nodes import (
    Node, HeadingNode, ParagraphNode, ListNode,
    TableNode, CodeBlockNode, ImageNode
)

def test_heading_node_creation():
    node = HeadingNode(level=1, content="Title")
    assert node.type == "heading"
    assert node.attrs["level"] == 1
    assert node.content == "Title"

def test_paragraph_node_with_runs():
    runs = [
        {"text": "Hello ", "bold": False, "italic": False},
        {"text": "world", "bold": True, "italic": False}
    ]
    node = ParagraphNode(runs=runs)
    assert node.type == "paragraph"
    assert len(node.content) == 2
    assert node.content[1]["bold"] is True

def test_list_node_ordered():
    items = ["First", "Second", "Third"]
    node = ListNode(items=items, ordered=True)
    assert node.type == "list"
    assert node.attrs["ordered"] is True
    assert len(node.content) == 3

def test_code_block_node():
    code = "def hello():\n    print('world')"
    node = CodeBlockNode(code=code, language="python")
    assert node.type == "code_block"
    assert node.attrs["language"] == "python"
    assert "def hello" in node.content

def test_image_node():
    node = ImageNode(path="./images/pic.png", alt="A picture")
    assert node.type == "image"
    assert node.attrs["path"] == "./images/pic.png"
    assert node.attrs["alt"] == "A picture"

def test_table_node():
    rows = [
        ["Header1", "Header2"],
        ["Cell1", "Cell2"]
    ]
    node = TableNode(rows=rows, has_header=True)
    assert node.type == "table"
    assert node.attrs["has_header"] is True
    assert len(node.content) == 2
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/unit/test_ast_nodes.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 3: 实现 AST 节点类**

```python
# utils/ast_nodes.py
from typing import List, Dict, Any, Optional

class Node:
    """AST 基础节点"""
    def __init__(self, node_type: str, content: Any, attrs: Optional[Dict] = None):
        self.type = node_type
        self.content = content
        self.attrs = attrs or {}

class HeadingNode(Node):
    """标题节点"""
    def __init__(self, level: int, content: str):
        super().__init__("heading", content, {"level": level})

class ParagraphNode(Node):
    """段落节点"""
    def __init__(self, runs: List[Dict[str, Any]]):
        super().__init__("paragraph", runs, {})

class ListNode(Node):
    """列表节点"""
    def __init__(self, items: List[str], ordered: bool = False):
        super().__init__("list", items, {"ordered": ordered})

class CodeBlockNode(Node):
    """代码块节点"""
    def __init__(self, code: str, language: str = ""):
        super().__init__("code_block", code, {"language": language})

class ImageNode(Node):
    """图片节点"""
    def __init__(self, path: str, alt: str = ""):
        super().__init__("image", None, {"path": path, "alt": alt})

class TableNode(Node):
    """表格节点"""
    def __init__(self, rows: List[List[str]], has_header: bool = False):
        super().__init__("table", rows, {"has_header": has_header})
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/unit/test_ast_nodes.py -v
```

Expected: 所有测试通过

- [ ] **Step 5: 提交**

```bash
git add utils/ast_nodes.py tests/unit/test_ast_nodes.py
git commit -m "feat: add AST node definitions"
```

---

## Task 3: Markdown 渲染器（基础格式）

**Files:**
- Create: `renderers/md_renderer.py`
- Create: `tests/unit/test_md_renderer.py`

- [ ] **Step 1: 编写 Markdown 渲染器测试**

```python
# tests/unit/test_md_renderer.py
import pytest
from renderers.md_renderer import MarkdownRenderer
from utils.ast_nodes import (
    HeadingNode, ParagraphNode, ListNode, CodeBlockNode
)

def test_render_heading():
    renderer = MarkdownRenderer()
    node = HeadingNode(level=1, content="Title")
    result = renderer.render_node(node)
    assert result == "# Title\n\n"

def test_render_heading_level_3():
    renderer = MarkdownRenderer()
    node = HeadingNode(level=3, content="Subtitle")
    result = renderer.render_node(node)
    assert result == "### Subtitle\n\n"

def test_render_paragraph_plain():
    renderer = MarkdownRenderer()
    runs = [{"text": "Hello world", "bold": False, "italic": False}]
    node = ParagraphNode(runs=runs)
    result = renderer.render_node(node)
    assert result == "Hello world\n\n"

def test_render_paragraph_with_bold():
    renderer = MarkdownRenderer()
    runs = [
        {"text": "Hello ", "bold": False, "italic": False},
        {"text": "world", "bold": True, "italic": False}
    ]
    node = ParagraphNode(runs=runs)
    result = renderer.render_node(node)
    assert result == "Hello **world**\n\n"

def test_render_paragraph_with_italic():
    renderer = MarkdownRenderer()
    runs = [{"text": "italic text", "bold": False, "italic": True}]
    node = ParagraphNode(runs=runs)
    result = renderer.render_node(node)
    assert result == "*italic text*\n\n"

def test_render_unordered_list():
    renderer = MarkdownRenderer()
    node = ListNode(items=["First", "Second", "Third"], ordered=False)
    result = renderer.render_node(node)
    expected = "- First\n- Second\n- Third\n\n"
    assert result == expected

def test_render_ordered_list():
    renderer = MarkdownRenderer()
    node = ListNode(items=["First", "Second"], ordered=True)
    result = renderer.render_node(node)
    expected = "1. First\n2. Second\n\n"
    assert result == expected

def test_render_code_block():
    renderer = MarkdownRenderer()
    code = "def hello():\n    print('world')"
    node = CodeBlockNode(code=code, language="python")
    result = renderer.render_node(node)
    expected = "```python\ndef hello():\n    print('world')\n```\n\n"
    assert result == expected
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/unit/test_md_renderer.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 3: 实现 Markdown 渲染器**

```python
# renderers/md_renderer.py
from typing import List
from utils.ast_nodes import Node

class MarkdownRenderer:
    """将 AST 渲染为 Markdown 文本"""
    
    def render_node(self, node: Node) -> str:
        """渲染单个节点"""
        if node.type == "heading":
            return self._render_heading(node)
        elif node.type == "paragraph":
            return self._render_paragraph(node)
        elif node.type == "list":
            return self._render_list(node)
        elif node.type == "code_block":
            return self._render_code_block(node)
        else:
            return ""
    
    def render(self, nodes: List[Node]) -> str:
        """渲染整个文档"""
        return "".join(self.render_node(node) for node in nodes)
    
    def _render_heading(self, node: Node) -> str:
        level = node.attrs["level"]
        prefix = "#" * level
        return f"{prefix} {node.content}\n\n"
    
    def _render_paragraph(self, node: Node) -> str:
        text_parts = []
        for run in node.content:
            text = run["text"]
            if run.get("bold"):
                text = f"**{text}**"
            if run.get("italic"):
                text = f"*{text}*"
            text_parts.append(text)
        return "".join(text_parts) + "\n\n"
    
    def _render_list(self, node: Node) -> str:
        lines = []
        ordered = node.attrs["ordered"]
        for i, item in enumerate(node.content, 1):
            if ordered:
                lines.append(f"{i}. {item}")
            else:
                lines.append(f"- {item}")
        return "\n".join(lines) + "\n\n"
    
    def _render_code_block(self, node: Node) -> str:
        language = node.attrs.get("language", "")
        code = node.content
        return f"```{language}\n{code}\n```\n\n"
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/unit/test_md_renderer.py -v
```

Expected: 所有测试通过

- [ ] **Step 5: 提交**

```bash
git add renderers/md_renderer.py tests/unit/test_md_renderer.py
git commit -m "feat: add Markdown renderer for basic formats"
```

---

## Task 4: Word 文档解析器（基础格式）

**Files:**
- Create: `parsers/docx_parser.py`
- Create: `tests/unit/test_docx_parser.py`
- Create: `tests/fixtures/test_basic.docx`

- [ ] **Step 1: 创建测试 Word 文档**

使用 python-docx 创建测试文档：

```python
# 临时脚本创建 test_basic.docx
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

doc = Document()

# 标题
doc.add_heading('Main Title', level=1)
doc.add_heading('Subtitle', level=2)

# 段落
p = doc.add_paragraph()
p.add_run('This is plain text. ')
p.add_run('This is bold.').bold = True
p.add_run(' ')
p.add_run('This is italic.').italic = True

# 列表
doc.add_paragraph('First item', style='List Bullet')
doc.add_paragraph('Second item', style='List Bullet')

# 代码块（使用等宽字体）
code_para = doc.add_paragraph('def hello():\n    print("world")')
code_para.runs[0].font.name = 'Courier New'

doc.save('tests/fixtures/test_basic.docx')
```

运行脚本创建文件。

- [ ] **Step 2: 编写解析器测试**

```python
# tests/unit/test_docx_parser.py
import pytest
from parsers.docx_parser import DocxParser
from utils.ast_nodes import HeadingNode, ParagraphNode, ListNode, CodeBlockNode

def test_parse_heading():
    parser = DocxParser()
    nodes = parser.parse('tests/fixtures/test_basic.docx')
    
    # 第一个节点应该是 Heading 1
    assert nodes[0].type == "heading"
    assert nodes[0].attrs["level"] == 1
    assert "Main Title" in nodes[0].content

def test_parse_paragraph_with_formatting():
    parser = DocxParser()
    nodes = parser.parse('tests/fixtures/test_basic.docx')
    
    # 找到段落节点
    para_nodes = [n for n in nodes if n.type == "paragraph"]
    assert len(para_nodes) > 0
    
    # 检查 runs
    para = para_nodes[0]
    runs = para.content
    assert any(r.get("bold") for r in runs)
    assert any(r.get("italic") for r in runs)
```

- [ ] **Step 3: 运行测试确认失败**

```bash
pytest tests/unit/test_docx_parser.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 4: 实现 Word 文档解析器**

```python
# parsers/docx_parser.py
from typing import List
from docx import Document
from utils.ast_nodes import (
    Node, HeadingNode, ParagraphNode, ListNode, CodeBlockNode
)

class DocxParser:
    """解析 Word 文档为 AST"""
    
    def parse(self, file_path: str) -> List[Node]:
        """解析 Word 文档"""
        doc = Document(file_path)
        nodes = []
        
        for para in doc.paragraphs:
            node = self._parse_paragraph(para)
            if node:
                nodes.append(node)
        
        return nodes
    
    def _parse_paragraph(self, para) -> Node:
        """解析段落"""
        style_name = para.style.name
        
        # 标题
        if style_name.startswith('Heading'):
            level = int(style_name.split()[-1])
            return HeadingNode(level=level, content=para.text)
        
        # 列表
        if 'List' in style_name:
            return ListNode(items=[para.text], ordered='Number' in style_name)
        
        # 代码块（检查字体）
        if self._is_code_block(para):
            return CodeBlockNode(code=para.text, language="")
        
        # 普通段落
        runs = []
        for run in para.runs:
            runs.append({
                "text": run.text,
                "bold": run.bold or False,
                "italic": run.italic or False
            })
        
        if runs:
            return ParagraphNode(runs=runs)
        return None
    
    def _is_code_block(self, para) -> bool:
        """检查是否为代码块"""
        if not para.runs:
            return False
        font_name = para.runs[0].font.name
        return font_name in ['Courier New', 'Consolas', 'Monaco']
```

- [ ] **Step 5: 运行测试确认通过**

```bash
pytest tests/unit/test_docx_parser.py -v
```

Expected: 所有测试通过

- [ ] **Step 6: 提交**

```bash
git add parsers/docx_parser.py tests/unit/test_docx_parser.py tests/fixtures/test_basic.docx
git commit -m "feat: add Word document parser for basic formats"
```

---

## Task 5: Word → Markdown 转换器

**Files:**
- Create: `converters/docx_to_md.py`
- Create: `tests/integration/test_docx_to_md.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/integration/test_docx_to_md.py
import pytest
import os
from converters.docx_to_md import DocxToMarkdownConverter

def test_convert_basic_document():
    converter = DocxToMarkdownConverter()
    output_path = 'tests/fixtures/test_output.md'
    
    converter.convert(
        input_path='tests/fixtures/test_basic.docx',
        output_path=output_path
    )
    
    assert os.path.exists(output_path)
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert '# Main Title' in content
    assert '## Subtitle' in content
    assert '**' in content  # Bold text
    assert '*' in content   # Italic text
    
    # 清理
    os.remove(output_path)
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/integration/test_docx_to_md.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 3: 实现转换器**

```python
# converters/docx_to_md.py
from parsers.docx_parser import DocxParser
from renderers.md_renderer import MarkdownRenderer

class DocxToMarkdownConverter:
    """Word → Markdown 转换器"""
    
    def __init__(self):
        self.parser = DocxParser()
        self.renderer = MarkdownRenderer()
    
    def convert(self, input_path: str, output_path: str):
        """转换 Word 文档为 Markdown"""
        # 解析
        nodes = self.parser.parse(input_path)
        
        # 渲染
        markdown_text = self.renderer.render(nodes)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/integration/test_docx_to_md.py -v
```

Expected: 测试通过

- [ ] **Step 5: 提交**

```bash
git add converters/docx_to_md.py tests/integration/test_docx_to_md.py
git commit -m "feat: add Word to Markdown converter"
```

---

## Task 6: Markdown 解析器

**Files:**
- Create: `parsers/md_parser.py`
- Create: `tests/unit/test_md_parser.py`
- Create: `tests/fixtures/test_basic.md`

- [ ] **Step 1: 创建测试 Markdown 文件**

```markdown
# tests/fixtures/test_basic.md
# Main Title

## Subtitle

This is plain text. **This is bold.** *This is italic.*

- First item
- Second item

```python
def hello():
    print("world")
```
```

- [ ] **Step 2: 编写解析器测试**

```python
# tests/unit/test_md_parser.py
import pytest
from parsers.md_parser import MarkdownParser

def test_parse_heading():
    parser = MarkdownParser()
    nodes = parser.parse('tests/fixtures/test_basic.md')
    
    headings = [n for n in nodes if n.type == "heading"]
    assert len(headings) >= 2
    assert headings[0].attrs["level"] == 1
    assert "Main Title" in headings[0].content

def test_parse_paragraph():
    parser = MarkdownParser()
    nodes = parser.parse('tests/fixtures/test_basic.md')
    
    paras = [n for n in nodes if n.type == "paragraph"]
    assert len(paras) > 0

def test_parse_list():
    parser = MarkdownParser()
    nodes = parser.parse('tests/fixtures/test_basic.md')
    
    lists = [n for n in nodes if n.type == "list"]
    assert len(lists) > 0
    assert lists[0].attrs["ordered"] is False

def test_parse_code_block():
    parser = MarkdownParser()
    nodes = parser.parse('tests/fixtures/test_basic.md')
    
    code_blocks = [n for n in nodes if n.type == "code_block"]
    assert len(code_blocks) > 0
    assert code_blocks[0].attrs["language"] == "python"
```

- [ ] **Step 3: 运行测试确认失败**

```bash
pytest tests/unit/test_md_parser.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 4: 实现 Markdown 解析器**

```python
# parsers/md_parser.py
from typing import List
import mistune
from utils.ast_nodes import (
    Node, HeadingNode, ParagraphNode, ListNode, CodeBlockNode
)

class MarkdownParser:
    """解析 Markdown 为 AST"""
    
    def __init__(self):
        self.markdown = mistune.create_markdown(renderer=None)
    
    def parse(self, file_path: str) -> List[Node]:
        """解析 Markdown 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tokens = self.markdown(content)
        return self._convert_tokens(tokens)
    
    def _convert_tokens(self, tokens) -> List[Node]:
        """将 mistune tokens 转换为 AST"""
        nodes = []
        
        for token in tokens:
            node = self._convert_token(token)
            if node:
                nodes.append(node)
        
        return nodes
    
    def _convert_token(self, token) -> Node:
        """转换单个 token"""
        token_type = token['type']
        
        if token_type == 'heading':
            return HeadingNode(
                level=token['attrs']['level'],
                content=self._extract_text(token['children'])
            )
        
        elif token_type == 'paragraph':
            runs = self._parse_inline(token['children'])
            return ParagraphNode(runs=runs)
        
        elif token_type == 'list':
            items = [self._extract_text(item['children']) 
                    for item in token['children']]
            ordered = token['attrs'].get('ordered', False)
            return ListNode(items=items, ordered=ordered)
        
        elif token_type == 'block_code':
            return CodeBlockNode(
                code=token['raw'],
                language=token['attrs'].get('info', '')
            )
        
        return None
    
    def _parse_inline(self, children) -> List[dict]:
        """解析行内元素"""
        runs = []
        for child in children:
            if child['type'] == 'text':
                runs.append({
                    "text": child['raw'],
                    "bold": False,
                    "italic": False
                })
            elif child['type'] == 'strong':
                runs.append({
                    "text": self._extract_text(child['children']),
                    "bold": True,
                    "italic": False
                })
            elif child['type'] == 'emphasis':
                runs.append({
                    "text": self._extract_text(child['children']),
                    "bold": False,
                    "italic": True
                })
        return runs
    
    def _extract_text(self, children) -> str:
        """提取纯文本"""
        if not children:
            return ""
        texts = []
        for child in children:
            if isinstance(child, dict):
                if child['type'] == 'text':
                    texts.append(child['raw'])
                elif 'children' in child:
                    texts.append(self._extract_text(child['children']))
        return "".join(texts)
```

- [ ] **Step 5: 运行测试确认通过**

```bash
pytest tests/unit/test_md_parser.py -v
```

Expected: 所有测试通过

- [ ] **Step 6: 提交**

```bash
git add parsers/md_parser.py tests/unit/test_md_parser.py tests/fixtures/test_basic.md
git commit -m "feat: add Markdown parser"
```

---

## Task 7: Word 渲染器

**Files:**
- Create: `renderers/docx_renderer.py`
- Create: `tests/unit/test_docx_renderer.py`

- [ ] **Step 1: 编写渲染器测试**

```python
# tests/unit/test_docx_renderer.py
import pytest
import os
from docx import Document
from renderers.docx_renderer import DocxRenderer
from utils.ast_nodes import HeadingNode, ParagraphNode, ListNode, CodeBlockNode

def test_render_heading():
    renderer = DocxRenderer()
    nodes = [HeadingNode(level=1, content="Test Title")]
    
    output_path = 'tests/fixtures/test_render.docx'
    renderer.render(nodes, output_path)
    
    doc = Document(output_path)
    assert len(doc.paragraphs) > 0
    assert doc.paragraphs[0].text == "Test Title"
    assert 'Heading 1' in doc.paragraphs[0].style.name
    
    os.remove(output_path)

def test_render_paragraph_with_bold():
    renderer = DocxRenderer()
    runs = [
        {"text": "Normal ", "bold": False, "italic": False},
        {"text": "bold", "bold": True, "italic": False}
    ]
    nodes = [ParagraphNode(runs=runs)]
    
    output_path = 'tests/fixtures/test_render.docx'
    renderer.render(nodes, output_path)
    
    doc = Document(output_path)
    para = doc.paragraphs[0]
    assert len(para.runs) == 2
    assert para.runs[1].bold is True
    
    os.remove(output_path)
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/unit/test_docx_renderer.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 3: 实现 Word 渲染器**

```python
# renderers/docx_renderer.py
from typing import List
from docx import Document
from docx.shared import Pt
from utils.ast_nodes import Node

class DocxRenderer:
    """将 AST 渲染为 Word 文档"""
    
    def render(self, nodes: List[Node], output_path: str):
        """渲染整个文档"""
        doc = Document()
        
        for node in nodes:
            self._render_node(doc, node)
        
        doc.save(output_path)
    
    def _render_node(self, doc: Document, node: Node):
        """渲染单个节点"""
        if node.type == "heading":
            self._render_heading(doc, node)
        elif node.type == "paragraph":
            self._render_paragraph(doc, node)
        elif node.type == "list":
            self._render_list(doc, node)
        elif node.type == "code_block":
            self._render_code_block(doc, node)
    
    def _render_heading(self, doc: Document, node: Node):
        level = node.attrs["level"]
        doc.add_heading(node.content, level=level)
    
    def _render_paragraph(self, doc: Document, node: Node):
        para = doc.add_paragraph()
        for run_data in node.content:
            run = para.add_run(run_data["text"])
            run.bold = run_data.get("bold", False)
            run.italic = run_data.get("italic", False)
    
    def _render_list(self, doc: Document, node: Node):
        ordered = node.attrs["ordered"]
        style = 'List Number' if ordered else 'List Bullet'
        for item in node.content:
            doc.add_paragraph(item, style=style)
    
    def _render_code_block(self, doc: Document, node: Node):
        para = doc.add_paragraph(node.content)
        para.runs[0].font.name = 'Courier New'
        para.runs[0].font.size = Pt(10)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/unit/test_docx_renderer.py -v
```

Expected: 所有测试通过

- [ ] **Step 5: 提交**

```bash
git add renderers/docx_renderer.py tests/unit/test_docx_renderer.py
git commit -m "feat: add Word document renderer"
```

---

## Task 8: Markdown → Word 转换器

**Files:**
- Create: `converters/md_to_docx.py`
- Create: `tests/integration/test_md_to_docx.py`

- [ ] **Step 1: 编写集成测试**

```python
# tests/integration/test_md_to_docx.py
import pytest
import os
from docx import Document
from converters.md_to_docx import MarkdownToDocxConverter

def test_convert_markdown_to_docx():
    converter = MarkdownToDocxConverter()
    output_path = 'tests/fixtures/test_output.docx'
    
    converter.convert(
        input_path='tests/fixtures/test_basic.md',
        output_path=output_path
    )
    
    assert os.path.exists(output_path)
    
    doc = Document(output_path)
    assert len(doc.paragraphs) > 0
    
    # 检查标题
    headings = [p for p in doc.paragraphs if 'Heading' in p.style.name]
    assert len(headings) >= 2
    
    os.remove(output_path)
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/integration/test_md_to_docx.py -v
```

Expected: FAIL - 模块不存在

- [ ] **Step 3: 实现转换器**

```python
# converters/md_to_docx.py
from parsers.md_parser import MarkdownParser
from renderers.docx_renderer import DocxRenderer

class MarkdownToDocxConverter:
    """Markdown → Word 转换器"""
    
    def __init__(self):
        self.parser = MarkdownParser()
        self.renderer = DocxRenderer()
    
    def convert(self, input_path: str, output_path: str):
        """转换 Markdown 为 Word 文档"""
        # 解析
        nodes = self.parser.parse(input_path)
        
        # 渲染
        self.renderer.render(nodes, output_path)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/integration/test_md_to_docx.py -v
```

Expected: 测试通过

- [ ] **Step 5: 提交**

```bash
git add converters/md_to_docx.py tests/integration/test_md_to_docx.py
git commit -m "feat: add Markdown to Word converter"
```

---

## Task 9: CLI 命令行接口

**Files:**
- Create: `word2md.py`
- Modify: `README.md`

- [ ] **Step 1: 编写 CLI 测试**

```python
# tests/integration/test_cli.py
import pytest
import subprocess
import os

def test_cli_docx_to_md():
    result = subprocess.run(
        ['python', 'word2md.py', 'tests/fixtures/test_basic.docx'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert os.path.exists('tests/fixtures/test_basic.md')
    
    # 清理
    if os.path.exists('tests/fixtures/test_basic.md'):
        os.remove('tests/fixtures/test_basic.md')

def test_cli_md_to_docx():
    result = subprocess.run(
        ['python', 'word2md.py', 'tests/fixtures/test_basic.md', '-o', 'tests/fixtures/output.docx'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert os.path.exists('tests/fixtures/output.docx')
    
    # 清理
    if os.path.exists('tests/fixtures/output.docx'):
        os.remove('tests/fixtures/output.docx')

def test_cli_version():
    result = subprocess.run(
        ['python', 'word2md.py', '--version'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert 'word2md' in result.stdout.lower()
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/integration/test_cli.py -v
```

Expected: FAIL - word2md.py 不存在

- [ ] **Step 3: 实现 CLI**

```python
# word2md.py
#!/usr/bin/env python3
"""
Word2Md - Word 和 Markdown 之间的双向转换工具
"""
import argparse
import sys
import os
from converters.docx_to_md import DocxToMarkdownConverter
from converters.md_to_docx import MarkdownToDocxConverter

VERSION = "0.1.0"

def main():
    parser = argparse.ArgumentParser(
        description='Word 和 Markdown 之间的双向转换工具'
    )
    parser.add_argument('input_file', help='输入文件路径 (.docx 或 .md)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--extract-images', action='store_true',
                       help='提取图片为独立文件')
    parser.add_argument('--images-dir', help='图片保存目录')
    parser.add_argument('--verbose', action='store_true',
                       help='显示详细信息')
    parser.add_argument('--version', action='version',
                       version=f'word2md {VERSION}')
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input_file):
        print(f"错误: 文件不存在: {args.input_file}", file=sys.stderr)
        return 1
    
    # 确定转换方向
    input_ext = os.path.splitext(args.input_file)[1].lower()
    
    if input_ext == '.docx':
        # Word → Markdown
        output_path = args.output or os.path.splitext(args.input_file)[0] + '.md'
        converter = DocxToMarkdownConverter()
        
        if args.verbose:
            print(f"转换 {args.input_file} → {output_path}")
        
        try:
            converter.convert(args.input_file, output_path)
            print(f"成功: {output_path}")
            return 0
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
    
    elif input_ext == '.md':
        # Markdown → Word
        output_path = args.output or os.path.splitext(args.input_file)[0] + '.docx'
        converter = MarkdownToDocxConverter()
        
        if args.verbose:
            print(f"转换 {args.input_file} → {output_path}")
        
        try:
            converter.convert(args.input_file, output_path)
            print(f"成功: {output_path}")
            return 0
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
    
    else:
        print(f"错误: 不支持的文件格式: {input_ext}", file=sys.stderr)
        print("支持的格式: .docx, .md", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/integration/test_cli.py -v
```

Expected: 所有测试通过

- [ ] **Step 5: 更新 README**

```markdown
# Word2Md

Word 和 Markdown 之间的高保真双向转换工具。

## 功能特性

- 双向转换：Word ↔ Markdown
- 支持基础格式：标题、粗体、斜体、列表
- 支持代码块
- 命令行工具，易于使用

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### Word → Markdown

```bash
python word2md.py document.docx
# 输出: document.md
```

### Markdown → Word

```bash
python word2md.py readme.md
# 输出: readme.docx
```

### 指定输出文件

```bash
python word2md.py input.docx -o output.md
```

### 显示详细信息

```bash
python word2md.py document.docx --verbose
```

## 开发

### 运行测试

```bash
pytest tests/ -v
```

### 测试覆盖率

```bash
pytest tests/ --cov=. --cov-report=html
```

## 许可证

MIT
```

- [ ] **Step 6: 手动测试**

```bash
# 测试 Word → Markdown
python word2md.py tests/fixtures/test_basic.docx -o test_output.md
cat test_output.md

# 测试 Markdown → Word
python word2md.py tests/fixtures/test_basic.md -o test_output.docx

# 清理
rm test_output.md test_output.docx
```

- [ ] **Step 7: 提交**

```bash
git add word2md.py README.md tests/integration/test_cli.py
git commit -m "feat: add CLI interface"
```

---

## 自审检查清单

- [x] **Spec 覆盖**: 所有核心需求已实现
  - ✓ 双向转换
  - ✓ 基础格式（标题、粗体、斜体、列表）
  - ✓ 代码块
  - ✓ 命令行接口
  - ✓ 单文件转换
  - ⚠ 表格和图片处理留待后续 Phase

- [x] **占位符扫描**: 无 TBD、TODO 或模糊描述

- [x] **类型一致性**: 所有节点类型、方法名在各任务中保持一致

- [x] **文件路径**: 所有路径明确且完整

- [x] **代码完整性**: 每个步骤都包含完整可运行的代码

---

## 后续扩展（Phase 2-4）

完成基础功能后，可以继续实现：

**Phase 2: 核心特性**
- 链接支持
- 图片处理（不提取模式）
- 嵌套列表

**Phase 3: 高级特性**
- 表格支持
- 图片提取模式
- 复杂表格（合并单元格）

**Phase 4: 优化和完善**
- 错误处理增强
- 性能优化
- 更多测试用例
