import os
import re
from .utils import get_git_blame_info

COMMENT_TYPES = {
    "TODO": {"emoji": "✅", "description": "Tasks to be done", "priority": 2},
    "FIXME": {"emoji": "🚨", "description": "Critical issues to fix", "priority": 1},
    "BUG": {"emoji": "🐛", "description": "Known bugs", "priority": 1},
    "HACK": {"emoji": "⚙️", "description": "Temporary solutions", "priority": 2},
    "NOTE": {"emoji": "📝", "description": "Important notes", "priority": 3},
    "TEMP": {"emoji": "🕒", "description": "Temporary code", "priority": 2},
    "IN PROGRESS": {"emoji": "🚧", "description": "Work in progress", "priority": 2},
    "OPTIMIZE": {"emoji": "⚡", "description": "Optimizations needed", "priority": 3},
    "REVIEW": {"emoji": "👀", "description": "Code to review", "priority": 2},
    "QUESTION": {"emoji": "❓", "description": "Questions to clarify", "priority": 2},
    "IDEA": {"emoji": "💡", "description": "Ideas to explore", "priority": 3}
}

ASSIGNEE_PATTERN = r'@(\w+)'
PRIORITY_PATTERN = r'P(\d+)'
DUE_DATE_PATTERN = r'DUE:\s*(\d{4}-\d{2}-\d{2})'
ISSUE_PATTERN = r'#(\d+)'
CREATED_PATTERN = r'CREATED:\s*(\d{4}-\d{2}-\d{2})'

def find_code_files(directory, extensions, exclude_dirs=None):
    """Find all code files in the given directory with the specified extensions."""
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', '.git', 'dist', 'build', 'venv', '__pycache__', '.next']

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                yield os.path.join(root, file)

def parse_comment_metadata(comment_text, comment_type):
    """Extract metadata from a comment text."""
    assignees = re.findall(ASSIGNEE_PATTERN, comment_text)
    priority_match = re.search(PRIORITY_PATTERN, comment_text)
    due_date_match = re.search(DUE_DATE_PATTERN, comment_text)
    issue_match = re.search(ISSUE_PATTERN, comment_text)
    created_match = re.search(CREATED_PATTERN, comment_text)

    priority = int(priority_match.group(1)) if priority_match else COMMENT_TYPES[comment_type]["priority"]

    return {
        'assignees': assignees,
        'priority': priority,
        'due_date': due_date_match.group(1) if due_date_match else None,
        'issue': issue_match.group(1) if issue_match else None,
        'created_match': created_match
    }

def clean_comment_text(comment_text):
    """Remove metadata patterns from comment text."""
    clean_text = comment_text
    for pattern in [ASSIGNEE_PATTERN, PRIORITY_PATTERN, DUE_DATE_PATTERN, ISSUE_PATTERN, CREATED_PATTERN]:
        clean_text = re.sub(pattern, '', clean_text)
    return re.sub(r'\s+', ' ', clean_text).strip()

def extract_comments(file_path, comment_types):
    """Extract comments from a single file with metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (UnicodeDecodeError, IOError):
        return []

    lines = content.split('\n')
    comments = []
    single_line_pattern = r'(?://|#|<!--|\*)\s*(' + '|'.join(comment_types) + r')\s*:?\s*(.*?)(?:-->|\*/)?$'

    for line_num, line in enumerate(lines, 1):
        matches = re.search(single_line_pattern, line.strip())
        if matches:
            comment_type = matches.group(1)
            comment_text = matches.group(2).strip()

            metadata = parse_comment_metadata(comment_text, comment_type)
            blame_info = get_git_blame_info(file_path, line_num)

            clean_text = clean_comment_text(comment_text)

            created_date = metadata['created_match'].group(1) if metadata['created_match'] else blame_info['date']

            comments.append({
                'type': comment_type,
                'text': clean_text,
                'full_text': comment_text,
                'file': file_path,
                'line': line_num,
                'assignees': metadata['assignees'],
                'priority': metadata['priority'],
                'due_date': metadata['due_date'],
                'issue': metadata['issue'],
                'created': created_date,
                'author': blame_info['author']
            })

    return comments
