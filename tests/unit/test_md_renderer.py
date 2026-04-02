# tests/unit/test_md_renderer.py
import pytest
from utils.ast_nodes import (
    HeadingNode, ParagraphNode, ListNode, CodeBlockNode
)
from renderers.md_renderer import MarkdownRenderer

def test_render_heading():
    """测试渲染一级标题"""
    node = HeadingNode(level=1, content="Main Title")
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    assert result == "# Main Title\n\n"

def test_render_heading_level_3():
    """测试渲染三级标题"""
    node = HeadingNode(level=3, content="Subsection")
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    assert result == "### Subsection\n\n"

def test_render_paragraph_plain():
    """测试渲染纯文本段落"""
    runs = [{"text": "This is plain text.", "bold": False, "italic": False}]
    node = ParagraphNode(runs=runs)
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    assert result == "This is plain text.\n\n"

def test_render_paragraph_with_bold():
    """测试渲染包含粗体的段落"""
    runs = [
        {"text": "This is ", "bold": False, "italic": False},
        {"text": "bold", "bold": True, "italic": False},
        {"text": " text.", "bold": False, "italic": False}
    ]
    node = ParagraphNode(runs=runs)
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    assert result == "This is **bold** text.\n\n"

def test_render_paragraph_with_italic():
    """测试渲染包含斜体的段落"""
    runs = [
        {"text": "This is ", "bold": False, "italic": False},
        {"text": "italic", "bold": False, "italic": True},
        {"text": " text.", "bold": False, "italic": False}
    ]
    node = ParagraphNode(runs=runs)
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    assert result == "This is *italic* text.\n\n"

def test_render_unordered_list():
    """测试渲染无序列表"""
    items = ["First item", "Second item", "Third item"]
    node = ListNode(items=items, ordered=False)
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    expected = "- First item\n- Second item\n- Third item\n\n"
    assert result == expected

def test_render_ordered_list():
    """测试渲染有序列表"""
    items = ["First step", "Second step", "Third step"]
    node = ListNode(items=items, ordered=True)
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    expected = "1. First step\n2. Second step\n3. Third step\n\n"
    assert result == expected

def test_render_code_block():
    """测试渲染代码块"""
    code = "def hello():\n    print('world')"
    node = CodeBlockNode(code=code, language="python")
    renderer = MarkdownRenderer()
    result = renderer.render([node])
    expected = "```python\ndef hello():\n    print('world')\n```\n\n"
    assert result == expected
