import pytest
import os
from converters.docx_to_md import DocxToMarkdownConverter

def test_convert_basic_document():
    converter = DocxToMarkdownConverter()
    output_path = 'tests/fixtures/test_output.md'
    converter.convert('tests/fixtures/test_basic.docx', output_path)
    assert os.path.exists(output_path)
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '# Main Title' in content
    assert '## Subtitle' in content
    os.remove(output_path)
