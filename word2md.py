#!/usr/bin/env python3
import argparse
import sys
import os
from converters.docx_to_md import DocxToMarkdownConverter
from converters.md_to_docx import MarkdownToDocxConverter

VERSION = "0.1.0"

def main():
    parser = argparse.ArgumentParser(description='Word 和 Markdown 之间的双向转换工具')
    parser.add_argument('input_file', help='输入文件路径 (.docx 或 .md)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--extract-images', action='store_true', help='提取图片为独立文件')
    parser.add_argument('--images-dir', help='图片保存目录（默认为 {输出文件名}_images/）')
    parser.add_argument('--table-format', choices=['gfm', 'html', 'auto'], default='auto',
                       help='表格格式：gfm=GitHub Flavored Markdown, html=HTML表格, auto=自动选择（默认）')
    parser.add_argument('--verbose', action='store_true', help='显示详细信息')
    parser.add_argument('--version', action='version', version=f'word2md {VERSION}')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"错误: 文件不存在: {args.input_file}", file=sys.stderr)
        return 1

    input_ext = os.path.splitext(args.input_file)[1].lower()

    if input_ext == '.docx':
        output_path = args.output or os.path.splitext(args.input_file)[0] + '.md'

        # 确定图片目录
        images_dir = None
        if args.extract_images:
            if args.images_dir:
                images_dir = args.images_dir
            else:
                # 默认为 {输出文件名}_images/
                base_name = os.path.splitext(output_path)[0]
                images_dir = f"{base_name}_images"

        converter = DocxToMarkdownConverter(
            table_format=args.table_format,
            extract_images=args.extract_images,
            images_dir=images_dir
        )

        if args.verbose:
            print(f"转换 {args.input_file} → {output_path}")
            if args.extract_images:
                print(f"图片目录: {images_dir}")
            print(f"表格格式: {args.table_format}")

        try:
            converter.convert(args.input_file, output_path)
            print(f"成功: {output_path}")
            return 0
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            import traceback
            if args.verbose:
                traceback.print_exc()
            return 1
    elif input_ext == '.md':
        output_path = args.output or os.path.splitext(args.input_file)[0] + '.docx'
        converter = MarkdownToDocxConverter()
        if args.verbose:
            print(f"转换 {args.input_file} → {output_path}")
        try:
            converter.convert(args.input_file, output_path)
            print(f"成功: {output_path}")
            return 0
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
    else:
        print(f"错误: 不支持的文件格式: {input_ext}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
