#!/usr/bin/env python3
"""
Extract TODO, TEMP, BUG, etc. comments from code files and generate a Markdown report.
Enhanced version with assignees, priorities, due dates, and GitHub issue linking.
"""

import os
import re
import json
import argparse
import subprocess
from collections import defaultdict
from datetime import datetime as dt

COMMENT_TYPES = {
    "TODO": {"emoji": "✅", "description": "Tâches à accomplir", "priority": 2},
    "FIXME": {"emoji": "🚨", "description": "Problèmes critiques à résoudre", "priority": 1},
    "BUG": {"emoji": "🐛", "description": "Bugs connus", "priority": 1},
    "HACK": {"emoji": "⚙️", "description": "Solutions temporaires", "priority": 2},
    "NOTE": {"emoji": "📝", "description": "Notes importantes", "priority": 3},
    "TEMP": {"emoji": "🕒", "description": "Code temporaire", "priority": 2},
    "IN PROGRESS": {"emoji": "🚧", "description": "Travail en cours", "priority": 2},
    "OPTIMIZE": {"emoji": "⚡", "description": "Optimisations nécessaires", "priority": 3},
    "REVIEW": {"emoji": "👀", "description": "Code à revoir", "priority": 2},
    "QUESTION": {"emoji": "❓", "description": "Questions à clarifier", "priority": 2},
    "IDEA": {"emoji": "💡", "description": "Idées à explorer", "priority": 3}
}

DEFAULT_EXTENSIONS = ['.js', '.jsx', '.ts', '.tsx', '.py', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.java', '.php', '.rb', '.swift', '.kt', '.css', '.scss', '.html', '.hs']

ASSIGNEE_PATTERN = r'@(\w+)'
PRIORITY_PATTERN = r'P(\d+)'
DUE_DATE_PATTERN = r'DUE:\s*(\d{4}-\d{2}-\d{2})'
ISSUE_PATTERN = r'#(\d+)'
CREATED_PATTERN = r'CREATED:\s*(\d{4}-\d{2}-\d{2})'

def get_git_blame_info(file_path, line_number):
    """Get the author and date when a specific line was last modified."""
    try:
        blame_output = subprocess.check_output(
            ['git', 'blame', '-L', f"{line_number},{line_number}", '--porcelain', file_path],
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )

        author_match = re.search(r'author\s(.+)', blame_output)
        date_match = re.search(r'author-time\s(\d+)', blame_output)

        author = author_match.group(1) if author_match else "Unknown"
        timestamp = int(date_match.group(1)) if date_match else 0

        date = dt.fromtimestamp(timestamp).strftime('%Y-%m-%d') if timestamp else "Unknown"

        return {
            'author': author,
            'date': date
        }
    except (subprocess.SubprocessError, FileNotFoundError):
        return {
            'author': "Unknown",
            'date': "Unknown"
        }

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

def calculate_age_in_days(date_str):
    """Calculate the age of a comment in days based on its creation date."""
    if date_str == "Unknown":
        return 999

    try:
        creation_date = dt.strptime(date_str, '%Y-%m-%d')
        today = dt.now()
        return (today - creation_date).days
    except ValueError:
        return 999

def generate_priority_label(priority):
    """Generate a priority label with appropriate styling."""
    if priority == 1:
        return "🔴 **CRITIQUE**"
    elif priority == 2:
        return "🟠 **ÉLEVÉE**"
    elif priority == 3:
        return "🟡 **MOYENNE**"
    elif priority == 4:
        return "🟢 **BASSE**"
    else:
        return f"⚪ **P{priority}**"

def calculate_days_to_due(due_date):
    """Calculate days to due date."""
    return (dt.strptime(due_date, '%Y-%m-%d') - dt.now()).days

def format_due_date_text(due_date):
    """Format due date text with emojis based on status."""
    if not due_date:
        return ""

    days_to_due = calculate_days_to_due(due_date)
    if days_to_due < 0:
        return f"🚨 {-days_to_due}j de retard"
    else:
        return f"⏰ Dans {days_to_due}j"

def format_assignees_text(assignees):
    """Format assignees list to text."""
    if not assignees:
        return ""
    return f"👤 {', '.join('@' + a for a in assignees)}"

def generate_progress_bar(count, max_count, length=20):
    """Generate a visual progress bar."""
    bar_length = int((count / max_count) * length) if max_count > 0 else 0
    return "█" * bar_length + "░" * (length - bar_length)

def write_report_header(file, current_date):
    """Write report header section."""
    file.write("# 📋 Rapport d'annotations\n\n")
    file.write(f"*Généré le {current_date}*\n\n")

def write_priority_section(file, priority_counts, total, max_count):
    """Write the priority section with visual bars."""
    file.write("### ⚡ Priorités\n\n")

    priority_labels = {
        1: "🔴 Critique ",
        2: "🟠 Élevée  ",
        3: "🟡 Moyenne ",
        4: "🟢 Basse   "
    }

    for priority, count in sorted(priority_counts.items()):
        if count == 0:
            continue
        percentage = count / total * 100
        bar = generate_progress_bar(count, max_count)
        file.write(f"{priority_labels[priority]} | {bar} | {count} ({percentage:.1f}%)\n")
    file.write("\n")

def write_types_section(file, grouped_comments):
    """Write the types section with visual bars."""
    file.write("### 🏷️ Types\n\n")
    type_counts = {t: len(c) for t, c in grouped_comments.items()}
    max_type_count = max(type_counts.values()) if type_counts else 1

    for comment_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        emoji = COMMENT_TYPES[comment_type]["emoji"]
        bar = generate_progress_bar(count, max_type_count, 15)
        file.write(f"{emoji} {comment_type.ljust(12)} | {bar} | {count}\n")
    file.write("\n")

def format_comment_path(file_path, repo_root, max_length=40):
    """Format file path to display in report."""
    relative_path = os.path.relpath(file_path, repo_root)
    return relative_path if len(relative_path) < max_length else "..." + relative_path[-(max_length-3):]

def write_urgent_comments_section(file, urgent_comments, repo_root):
    """Write the urgent comments section."""
    if not urgent_comments:
        return

    file.write("## ⚠️ Urgents à traiter\n\n")
    for i, comment in enumerate(urgent_comments[:10], 1):
        priority_marker = "🔴" if comment['priority'] == 1 else "⚠️"
        type_emoji = COMMENT_TYPES[comment['type']]["emoji"]
        short_path = format_comment_path(comment['file'], repo_root)

        file.write(f"{i}. {priority_marker} {type_emoji} **{short_path}:{comment['line']}**\n")
        file.write(f"   {comment['text']}\n")

        due_text = format_due_date_text(comment['due_date'])
        assignee_text = format_assignees_text(comment['assignees'])

        meta = []
        if due_text:
            meta.append(due_text)
        if assignee_text:
            meta.append(assignee_text)

        if meta:
            file.write(f"   *{' | '.join(meta)}*\n")

        file.write("\n")

def write_report_footer(file, output_file):
    """Write report footer with link to detailed report."""
    detailed_report = os.path.splitext(output_file)[0] + "_detailed.md"
    file.write(f"\n---\n\n*Pour plus de détails, consultez le [rapport complet]({os.path.basename(detailed_report)})*\n")

def generate_simple_report(comments, output_file, repo_root, repo_url=None):
    """Génère un rapport simplifié et visuellement attrayant des annotations."""
    grouped_comments = defaultdict(list)
    for comment in comments:
        grouped_comments[comment['type']].append(comment)

    current_date = dt.now().strftime('%Y-%m-%d')

    priority_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for comment in comments:
        priority_counts[comment['priority']] += 1

    urgent_comments = [c for c in comments if c['priority'] == 1 or c['due_date']]
    urgent_comments.sort(key=lambda x: (x['priority'], x['due_date'] or '9999-12-31'))

    with open(output_file, 'w', encoding='utf-8') as f:
        write_report_header(f, current_date)

        f.write("## 🔍 En bref\n\n")
        total = len(comments)
        f.write(f"**{total}** annotations au total dans le code\n\n")

        max_count = max(priority_counts.values()) if priority_counts else 1
        write_priority_section(f, priority_counts, total, max_count)

        write_types_section(f, grouped_comments)

        write_urgent_comments_section(f, urgent_comments, repo_root)

        write_report_footer(f, output_file)

def write_md_header_toc(file, current_date, comment_types, grouped_comments):
    """Write markdown report header and table of contents."""
    file.write(f"# Rapport des annotations dans le code\n\n")
    file.write(f"*Généré le {current_date}*\n\n")
    file.write(f"Ce rapport liste toutes les annotations trouvées dans le code source.\n\n")

    file.write("## Sommaire\n\n")
    file.write("- [Résumé](#résumé)\n")
    file.write("- [Statistiques](#statistiques)\n")

    for comment_type in comment_types:
        if comment_type in grouped_comments:
            count = len(grouped_comments[comment_type])
            emoji = COMMENT_TYPES[comment_type]["emoji"]
            description = COMMENT_TYPES[comment_type]["description"]
            file.write(f"- [{emoji} {description} ({count})](#user-content-{comment_type.lower().replace(' ', '-')})\n")

    file.write("- [Par priorité](#par-priorité)\n")

def write_md_summary(file, comments, oldest_comment, newest_comment, top_assignees, due_comments):
    """Write summary section of markdown report."""
    file.write("\n## Résumé\n\n")
    total = len(comments)
    file.write(f"**Total des annotations:** {total}\n\n")

    if oldest_comment:
        oldest_age = calculate_age_in_days(oldest_comment['created'])
        file.write(f"**Annotation la plus ancienne:** {oldest_age} jours ({oldest_comment['created']})\n")
        file.write(f"- {oldest_comment['file']}:{oldest_comment['line']} - {oldest_comment['text']}\n\n")

    if newest_comment:
        newest_age = calculate_age_in_days(newest_comment['created'])
        file.write(f"**Annotation la plus récente:** {newest_age} jours ({newest_comment['created']})\n")
        file.write(f"- {newest_comment['file']}:{newest_comment['line']} - {newest_comment['text']}\n\n")

    if top_assignees:
        file.write("**Top contributeurs:**\n")
        for assignee, count in top_assignees:
            file.write(f"- @{assignee}: {count} annotations\n")
        file.write("\n")

    if due_comments:
        file.write("**Prochaines échéances:**\n")
        for comment in due_comments[:5]:
            file.write(f"- {comment['due_date']} - {comment['file']}:{comment['line']} - {comment['text']}\n")
        file.write("\n")

def write_md_statistics(file, grouped_comments, total, priority_counts, assignees_count):
    """Write statistics section of markdown report."""
    file.write("## Statistiques\n\n")

    file.write("### Par type\n\n")
    file.write("| Type | Nombre | Pourcentage |\n")
    file.write("|------|--------|-------------|\n")
    for comment_type in COMMENT_TYPES:
        if comment_type in grouped_comments:
            count = len(grouped_comments[comment_type])
            percentage = (count / total) * 100 if total > 0 else 0
            emoji = COMMENT_TYPES[comment_type]["emoji"]
            file.write(f"| {emoji} {comment_type} | {count} | {percentage:.1f}% |\n")
    file.write("\n")

    file.write("### Par priorité\n\n")
    file.write("| Priorité | Nombre | Pourcentage |\n")
    file.write("|----------|--------|-------------|\n")
    for priority in sorted(priority_counts.keys()):
        count = priority_counts[priority]
        percentage = (count / total) * 100 if total > 0 else 0
        priority_label = generate_priority_label(priority).replace("**", "")
        file.write(f"| {priority_label} | {count} | {percentage:.1f}% |\n")
    file.write("\n")

    if assignees_count:
        file.write("### Par assigné\n\n")
        file.write("| Assigné | Nombre | Pourcentage |\n")
        file.write("|---------|--------|-------------|\n")
        for assignee, count in sorted(assignees_count.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100 if total > 0 else 0
            file.write(f"| @{assignee} | {count} | {percentage:.1f}% |\n")
        file.write("\n")

def format_comment_metadata(comment, repo_url):
    """Format metadata for a comment."""
    metadata = []

    if comment['priority'] <= 2:  # Seulement pour les priorités élevées
        metadata.append(generate_priority_label(comment['priority']))

    if comment['due_date']:
        days_to_due = calculate_days_to_due(comment['due_date'])
        due_status = "🚨 **EN RETARD**" if days_to_due < 0 else f"⏰ Échéance dans {days_to_due} jours"
        metadata.append(f"{due_status} ({comment['due_date']})")

    if comment['assignees']:
        assignees_text = ", ".join([f"@{a}" for a in comment['assignees']])
        metadata.append(f"👤 {assignees_text}")

    if comment['issue']:
        issue_text = f"🔗 #{comment['issue']}"
        if repo_url:
            issue_url = f"{repo_url}/issues/{comment['issue']}"
            issue_text = f"🔗 [#{comment['issue']}]({issue_url})"
        metadata.append(issue_text)

    age = calculate_age_in_days(comment['created'])
    age_text = f"il y a {age} jours" if age < 999 else "date inconnue"
    metadata.append(f"📅 Créé {age_text} par {comment['author']}")

    return metadata

def format_file_link(file_path, line_number, repo_root, repo_url):
    """Format file link for markdown report."""
    relative_path = os.path.relpath(file_path, repo_root)

    if repo_url:
        return f"{repo_url}/blob/main/{relative_path}#L{line_number}"
    else:
        return f"file:///{file_path}#L{line_number}"

def write_md_comments_by_type(file, grouped_comments, repo_root, repo_url):
    """Write comments grouped by type."""
    for comment_type, info in COMMENT_TYPES.items():
        if comment_type not in grouped_comments:
            continue

        emoji = info["emoji"]
        description = info["description"]
        file.write(f"## {emoji} {description} <a name='{comment_type.lower().replace(' ', '-')}' />\n\n")

        for comment in grouped_comments[comment_type]:
            relative_path = os.path.relpath(comment['file'], repo_root)
            file_link = format_file_link(comment['file'], comment['line'], repo_root, repo_url)
            line = f"- [{relative_path}:{comment['line']}]({file_link}): {comment['text']}"
            metadata = format_comment_metadata(comment, repo_url)

            if metadata:
                line += "\n  " + " | ".join(metadata)

            file.write(f"{line}\n\n")

def write_md_comments_by_priority(file, comments, priority_counts, repo_root, repo_url):
    """Write comments grouped by priority."""
    file.write("## Par priorité\n\n")

    for priority in sorted(priority_counts.keys()):
        priority_label = generate_priority_label(priority)
        file.write(f"### {priority_label}\n\n")

        priority_comments = [c for c in comments if c['priority'] == priority]
        for comment in priority_comments:
            relative_path = os.path.relpath(comment['file'], repo_root)
            file_link = format_file_link(comment['file'], comment['line'], repo_root, repo_url)
            emoji = COMMENT_TYPES[comment['type']]["emoji"]
            line = f"- {emoji} **{comment['type']}**: [{relative_path}:{comment['line']}]({file_link}): {comment['text']}"
            metadata = format_comment_metadata(comment, repo_url)

            if metadata:
                line += "\n  " + " | ".join(metadata)

            file.write(f"{line}\n\n")

def generate_markdown_report(comments, output_file, repo_root, repo_url=None):
    """Generate a Markdown report from the extracted comments."""
    comments.sort(key=lambda x: (x['priority'], -calculate_age_in_days(x['created'])))
    grouped_comments = defaultdict(list)
    for comment in comments:
        grouped_comments[comment['type']].append(comment)

    oldest_comment = max(comments, key=lambda x: calculate_age_in_days(x['created']), default=None)
    newest_comment = min(comments, key=lambda x: calculate_age_in_days(x['created']), default=None)

    assignees_count = defaultdict(int)
    for comment in comments:
        for assignee in comment['assignees']:
            assignees_count[assignee] += 1

    top_assignees = sorted(assignees_count.items(), key=lambda x: x[1], reverse=True)[:5]

    priority_counts = defaultdict(int)
    for comment in comments:
        priority_counts[comment['priority']] += 1
    current_date = dt.now().strftime('%Y-%m-%d à %H:%M:%S')
    due_comments = [c for c in comments if c['due_date']]
    if due_comments:
        due_comments.sort(key=lambda x: x['due_date'])

    with open(output_file, 'w', encoding='utf-8') as f:
        write_md_header_toc(f, current_date, COMMENT_TYPES.keys(), grouped_comments)
        write_md_summary(f, comments, oldest_comment, newest_comment, top_assignees, due_comments)
        write_md_statistics(f, grouped_comments, len(comments), priority_counts, assignees_count)
        write_md_comments_by_type(f, grouped_comments, repo_root, repo_url)
        write_md_comments_by_priority(f, comments, priority_counts, repo_root, repo_url)

def generate_json_data(comments, output_file, repo_root):
    """Generate a JSON file with all comment data for potential integration with other tools."""
    json_data = []
    for comment in comments:
        json_comment = comment.copy()
        json_comment['file'] = os.path.relpath(comment['file'], repo_root)
        json_data.append(json_comment)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

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

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Scanning {args.directory} for code annotations...")
    all_comments = []

    file_count = 0
    for file_path in find_code_files(args.directory, args.extensions, args.exclude):
        file_comments = extract_comments(file_path, COMMENT_TYPES.keys())
        all_comments.extend(file_comments)
        file_count += 1
        if file_count % 100 == 0:
            print(f"Processed {file_count} files...")

    if not all_comments:
        print("Aucune annotation trouvée.")
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

if __name__ == "__main__":
    main()