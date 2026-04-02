# utils/ast_nodes.py
from typing import List, Dict, Any, Optional

class Node:
    """AST 基础节点"""
    def __init__(self, node_type: str, content: Any, attrs: Optional[Dict] = None):
        self.type = node_type
        self.content = content
        self.attrs = attrs or {}

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, content={self.content!r}, attrs={self.attrs!r})"

class HeadingNode(Node):
    """标题节点"""
    def __init__(self, level: int, content: str):
        super().__init__("heading", content, {"level": level})

    def __repr__(self):
        return f"HeadingNode(level={self.attrs['level']}, content={self.content!r})"

class ParagraphNode(Node):
    """段落节点"""
    def __init__(self, runs: List[Dict[str, Any]]):
        super().__init__("paragraph", runs, {})

    def __repr__(self):
        return f"ParagraphNode(runs={len(self.content)} runs)"

class ListNode(Node):
    """列表节点"""
    def __init__(self, items: List[str], ordered: bool = False):
        super().__init__("list", items, {"ordered": ordered})

    def __repr__(self):
        return f"ListNode(items={len(self.content)}, ordered={self.attrs['ordered']})"

class CodeBlockNode(Node):
    """代码块节点"""
    def __init__(self, code: str, language: str = ""):
        super().__init__("code_block", code, {"language": language})

    def __repr__(self):
        return f"CodeBlockNode(language={self.attrs['language']!r}, lines={len(self.content.splitlines())})"

class ImageNode(Node):
    """图片节点"""
    def __init__(self, path: str, alt: str = ""):
        super().__init__("image", path, {"alt": alt})

    def __repr__(self):
        return f"ImageNode(path={self.content!r}, alt={self.attrs.get('alt', '')!r})"

class TableNode(Node):
    """表格节点"""
    def __init__(self, rows: List[List[str]], has_header: bool = False):
        super().__init__("table", rows, {"has_header": has_header})

    def __repr__(self):
        return f"TableNode(rows={len(self.content)}, has_header={self.attrs['has_header']})"
