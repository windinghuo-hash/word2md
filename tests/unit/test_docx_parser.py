import pytest
from parsers.docx_parser import DocxParser

def test_parse_heading():
    parser = DocxParser()
    nodes = parser.parse('tests/fixtures/test_basic.docx')
    assert nodes[0].type == "heading"
    assert nodes[0].attrs["level"] == 1
    assert "Main Title" in nodes[0].content

def test_parse_paragraph_with_formatting():
    parser = DocxParser()
    nodes = parser.parse('tests/fixtures/test_basic.docx')
    para_nodes = [n for n in nodes if n.type == "paragraph"]
    assert len(para_nodes) > 0
    para = para_nodes[0]
    runs = para.content
    assert any(r.get("bold") for r in runs)
    assert any(r.get("italic") for r in runs)
