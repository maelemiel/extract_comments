import argparse
import os
from src.core import find_code_files, extract_comments, COMMENT_TYPES
from src.report import generate_simple_report, generate_markdown_report, generate_json_data

DEFAULT_EXTENSIONS = ['.js', '.jsx', '.ts', '.tsx', '.py', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.java', '.php', '.rb', '.swift', '.kt', '.css', '.scss', '.html', '.hs']

def main():
    parser = argparse.ArgumentParser(description='Extract and analyze code annotations')
    parser.add_argument('--directory', '-d', type=str, default='.', help='Directory to scan')
    parser.add_argument('--output', '-o', type=str, default='docs/todos/code_annotations.md', help='Output Markdown file')
    parser.add_argument('--json-output', '-j', type=str, default='docs/todos/code_annotations.json', help='Output JSON file')
    parser.add_argument('--extensions', '-e', type=str, nargs='+', default=DEFAULT_EXTENSIONS, help='File extensions to scan')
    parser.add_argument('--repo-url', '-r', type=str, help='GitHub repository URL (e.g., https://github.com/username/repo)')
    parser.add_argument('--exclude', '-x', type=str, nargs='+', help='Directories to exclude')
    parser.add_argument('--simple', '-s', action='store_true', help='Generate a simplified, prettier report')
    args = parser.parse_args()

    extensions = args.extensions if args.extensions else [
        '.js', '.jsx', '.ts', '.tsx', '.py', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.java', '.php', '.rb', '.swift', '.kt', '.css', '.scss', '.html', '.hs'
    ]
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Scanning {args.directory} for code annotations...")
    all_comments = []
    file_count = 0
    for file_path in find_code_files(args.directory, extensions, args.exclude):
        file_comments = extract_comments(file_path, COMMENT_TYPES.keys())
        all_comments.extend(file_comments)
        file_count += 1
        if file_count % 100 == 0:
            print(f"Processed {file_count} files...")

    if not all_comments:
        print("No annotations found.")
        return

    if args.simple:
        print(f"Generating simplified report...")
        generate_simple_report(all_comments, args.output, args.directory, args.repo_url)
        detailed_output = os.path.splitext(args.output)[0] + "_detailed.md"
        print(f"Generating detailed report...")
        generate_markdown_report(all_comments, detailed_output, args.directory, args.repo_url)
    else:
        print(f"Generating detailed report...")
        generate_markdown_report(all_comments, args.output, args.directory, args.repo_url)
    print(f"Generating JSON data...")
    generate_json_data(all_comments, args.json_output, args.directory)
    print(f"Total files scanned: {file_count}")
    print(f"Total annotations found: {len(all_comments)}")
    print(f"Report generated in {args.output}")
    print(f"JSON data generated in {args.json_output}")
