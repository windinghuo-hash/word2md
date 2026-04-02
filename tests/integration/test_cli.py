import pytest
import subprocess
import os

def test_cli_docx_to_md():
    result = subprocess.run(
        ['python', 'word2md.py', 'tests/fixtures/test_basic.docx', '-o', 'tests/fixtures/cli_output.md'],
        capture_output=True, text=True, cwd='D:/hahi/cc/word2md'
    )
    assert result.returncode == 0
    assert os.path.exists('tests/fixtures/cli_output.md')
    os.remove('tests/fixtures/cli_output.md')

def test_cli_md_to_docx():
    result = subprocess.run(
        ['python', 'word2md.py', 'tests/fixtures/test_basic.md', '-o', 'tests/fixtures/cli_output.docx'],
        capture_output=True, text=True, cwd='D:/hahi/cc/word2md'
    )
    assert result.returncode == 0
    assert os.path.exists('tests/fixtures/cli_output.docx')
    os.remove('tests/fixtures/cli_output.docx')

def test_cli_version():
    result = subprocess.run(
        ['python', 'word2md.py', '--version'],
        capture_output=True, text=True, cwd='D:/hahi/cc/word2md'
    )
    assert result.returncode == 0
