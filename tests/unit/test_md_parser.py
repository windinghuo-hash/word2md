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
