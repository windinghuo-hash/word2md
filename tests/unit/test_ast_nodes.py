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
    assert node.content == "./images/pic.png"
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

def test_empty_list_node():
    node = ListNode(items=[], ordered=False)
    assert node.type == "list"
    assert len(node.content) == 0
    assert node.attrs["ordered"] is False

def test_empty_string_content():
    node = HeadingNode(level=1, content="")
    assert node.type == "heading"
    assert node.content == ""
    assert node.attrs["level"] == 1

def test_empty_paragraph():
    node = ParagraphNode(runs=[])
    assert node.type == "paragraph"
    assert len(node.content) == 0

def test_node_repr():
    node = HeadingNode(level=2, content="Test")
    repr_str = repr(node)
    assert "HeadingNode" in repr_str
    assert "level=2" in repr_str
    assert "Test" in repr_str
