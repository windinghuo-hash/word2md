from parsers.md_parser import MarkdownParser
from renderers.docx_renderer import DocxRenderer

class MarkdownToDocxConverter:
    def __init__(self):
        self.parser = MarkdownParser()
        self.renderer = DocxRenderer()

    def convert(self, input_path: str, output_path: str):
        nodes = self.parser.parse(input_path)
        self.renderer.render(nodes, output_path)
