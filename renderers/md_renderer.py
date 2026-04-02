# renderers/md_renderer.py
from typing import List
from utils.ast_nodes import Node, HeadingNode, ParagraphNode, ListNode, CodeBlockNode, TableNode, ImageNode

class MarkdownRenderer:
    """将 AST 节点渲染为 Markdown 文本"""

    def __init__(self, table_format: str = 'auto'):
        """
        table_format: 'gfm' | 'html' | 'auto'
          - gfm:  强制 GFM 表格（多行内容用 <br>）
          - html: 强制 HTML <table>
          - auto: 含多行单元格时用 HTML，否则用 GFM（默认）
        """
        self.table_format = table_format

    def render(self, nodes: List[Node]) -> str:
        """渲染节点列表为 Markdown 文本

        Args:
            nodes: AST 节点列表

        Returns:
            Markdown 格式的文本
        """
        result = []
        for node in nodes:
            rendered = self.render_node(node)
            if rendered:
                result.append(rendered)
        return "".join(result)

    def render_node(self, node: Node) -> str:
        """渲染单个节点

        Args:
            node: AST 节点

        Returns:
            渲染后的文本
        """
        if isinstance(node, HeadingNode):
            return self._render_heading(node)
        elif isinstance(node, ParagraphNode):
            return self._render_paragraph(node)
        elif isinstance(node, ListNode):
            return self._render_list(node)
        elif isinstance(node, CodeBlockNode):
            return self._render_code_block(node)
        elif isinstance(node, TableNode):
            return self._render_table(node)
        elif isinstance(node, ImageNode):
            return self._render_image(node)
        else:
            return ""

    def _render_heading(self, node: HeadingNode) -> str:
        """渲染标题节点

        Args:
            node: 标题节点

        Returns:
            Markdown 格式的标题
        """
        level = node.attrs.get("level", 1)
        prefix = "#" * level
        return f"{prefix} {node.content}\n\n"

    def _render_paragraph(self, node: ParagraphNode) -> str:
        """渲染段落节点

        Args:
            node: 段落节点

        Returns:
            Markdown 格式的段落
        """
        text_parts = []
        for run in node.content:
            text = run.get("text", "")
            is_bold = run.get("bold", False)
            is_italic = run.get("italic", False)

            if is_bold and is_italic:
                text = f"***{text}***"
            elif is_bold:
                text = f"**{text}**"
            elif is_italic:
                text = f"*{text}*"

            text_parts.append(text)

        return "".join(text_parts) + "\n\n"

    def _render_list(self, node: ListNode) -> str:
        """渲染列表节点

        Args:
            node: 列表节点

        Returns:
            Markdown 格式的列表
        """
        is_ordered = node.attrs.get("ordered", False)
        lines = []

        for i, item in enumerate(node.content, start=1):
            if is_ordered:
                lines.append(f"{i}. {item}")
            else:
                lines.append(f"- {item}")

        return "\n".join(lines) + "\n\n"

    def _render_image(self, node: ImageNode) -> str:
        """渲染图片节点"""
        path = node.content  # ImageNode 将 path 存在 content 中
        alt = node.attrs.get("alt", "")
        if path:
            return f"![{alt}]({path})\n\n"
        else:
            return f"*[{alt}]*\n\n"

    def _render_code_block(self, node: CodeBlockNode) -> str:
        """渲染代码块节点

        Args:
            node: 代码块节点

        Returns:
            Markdown 格式的代码块
        """
        language = node.attrs.get("language", "")
        code = node.content
        return f"```{language}\n{code}\n```\n\n"

    def _render_table(self, node: TableNode) -> str:
        """渲染表格：根据 table_format 选择 GFM 或 HTML"""
        rows = node.content
        if not rows:
            return ""

        has_header = node.attrs.get("has_header", False)
        has_multiline = any('\n' in cell for row in rows for cell in row)

        if self.table_format == 'html':
            return self._render_table_html(rows, has_header)
        elif self.table_format == 'gfm':
            return self._render_table_gfm(rows, has_header, use_br=True)
        else:  # auto
            if has_multiline:
                return self._render_table_html(rows, has_header)
            else:
                return self._render_table_gfm(rows, has_header, use_br=False)

    def _render_table_gfm(self, rows, has_header: bool, use_br: bool = False) -> str:
        """渲染为 GFM 表格"""
        col_count = max(len(row) for row in rows)
        col_widths = [3] * col_count
        for row in rows:
            for i, cell in enumerate(row):
                display = cell.replace('\n', '<br>') if use_br else cell.replace('\n', ' ')
                col_widths[i] = max(col_widths[i], len(display.strip()))

        def fmt_row(row):
            cells = []
            for i in range(col_count):
                if i < len(row):
                    if use_br:
                        cell_text = row[i].replace('\n', '<br>').strip()
                    else:
                        cell_text = row[i].replace('\n', ' ').strip()
                else:
                    cell_text = ""
                cells.append(cell_text.ljust(col_widths[i]))
            return "| " + " | ".join(cells) + " |"

        lines = [fmt_row(rows[0])]
        lines.append("| " + " | ".join("-" * col_widths[i] for i in range(col_count)) + " |")
        for row in rows[1:]:
            lines.append(fmt_row(row))
        return "\n".join(lines) + "\n\n"

    def _render_table_html(self, rows, has_header: bool) -> str:
        """渲染为 HTML table（支持单元格内换行）"""
        lines = ["<table>"]

        for row_idx, row in enumerate(rows):
            lines.append("  <tr>")
            tag = "th" if (has_header and row_idx == 0) else "td"
            for cell in row:
                # 每行作为独立段落
                paragraphs = [p.strip() for p in cell.split('\n') if p.strip()]
                if len(paragraphs) <= 1:
                    content = paragraphs[0] if paragraphs else ""
                    lines.append(f"    <{tag}>{content}</{tag}>")
                else:
                    inner = "".join(f"<p>{p}</p>" for p in paragraphs)
                    lines.append(f"    <{tag}>{inner}</{tag}>")
            lines.append("  </tr>")

        lines.append("</table>")
        return "\n".join(lines) + "\n\n"
