from parsers.docx_parser import DocxParser
from renderers.md_renderer import MarkdownRenderer

class DocxToMarkdownConverter:
    def __init__(self, table_format: str = 'auto', extract_images: bool = False, images_dir: str = None):
        self.parser = DocxParser()
        self.renderer = MarkdownRenderer(table_format=table_format)
        self.extract_images = extract_images
        self.images_dir = images_dir

    def convert(self, input_path: str, output_path: str):
        nodes = self.parser.parse(
            input_path,
            extract_images=self.extract_images,
            images_dir=self.images_dir
        )
        markdown_text = self.renderer.render(nodes)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
