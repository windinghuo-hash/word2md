from typing import List
import mistune
from utils.ast_nodes import Node, HeadingNode, ParagraphNode, ListNode, CodeBlockNode

class MarkdownParser:
    def __init__(self):
        self.markdown = mistune.create_markdown(renderer=None)

    def parse(self, file_path: str) -> List[Node]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tokens = self.markdown(content)
        return self._convert_tokens(tokens)

    def _convert_tokens(self, tokens) -> List[Node]:
        nodes = []
        for token in tokens:
            node = self._convert_token(token)
            if node:
                nodes.append(node)
        return nodes

    def _convert_token(self, token) -> Node:
        t = token['type']
        if t == 'heading':
            return HeadingNode(
                level=token['attrs']['level'],
                content=self._extract_text(token.get('children', []))
            )
        elif t == 'paragraph':
            runs = self._parse_inline(token.get('children', []))
            return ParagraphNode(runs=runs)
        elif t == 'list':
            items = []
            for item in token.get('children', []):
                children = item.get('children', [])
                items.append(self._extract_text(children))
            ordered = token['attrs'].get('ordered', False)
            return ListNode(items=items, ordered=ordered)
        elif t == 'block_code':
            return CodeBlockNode(
                code=token.get('raw', ''),
                language=token['attrs'].get('info', '') or ''
            )
        return None

    def _parse_inline(self, children) -> List[dict]:
        runs = []
        for child in children:
            ct = child.get('type', '')
            if ct == 'text':
                runs.append({"text": child.get('raw', ''), "bold": False, "italic": False})
            elif ct == 'strong':
                runs.append({"text": self._extract_text(child.get('children', [])), "bold": True, "italic": False})
            elif ct == 'emphasis':
                runs.append({"text": self._extract_text(child.get('children', [])), "bold": False, "italic": True})
            elif ct == 'codespan':
                runs.append({"text": child.get('raw', ''), "bold": False, "italic": False, "code": True})
        return runs

    def _extract_text(self, children) -> str:
        if not children:
            return ""
        texts = []
        for child in children:
            if isinstance(child, dict):
                ct = child.get('type', '')
                if ct == 'text':
                    texts.append(child.get('raw', ''))
                elif 'children' in child:
                    texts.append(self._extract_text(child['children']))
        return "".join(texts)
