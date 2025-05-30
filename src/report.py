import os
from collections import defaultdict
from datetime import datetime as dt
from .core import COMMENT_TYPES
from .utils import (
    generate_priority_label, calculate_age_in_days, calculate_days_to_due,
    format_due_date_text, format_assignees_text, generate_progress_bar
)

def write_report_header(file, current_date):
    """Write report header section."""
    file.write("# 📋 Annotations Report\n\n")
    file.write(f"*Generated on {current_date}*\n\n")

def write_priority_section(file, priority_counts, total, max_count):
    """Write the priority section with visual bars."""
    file.write("### ⚡ Priorities\n\n")

    priority_labels = {
        1: "🔴 Critical ",
        2: "🟠 High  ",
        3: "🟡 Medium ",
        4: "🟢 Low   "
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

    file.write("## ⚠️ Urgent items to address\n\n")
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
    file.write(f"\n---\n\n*For more details, see the [full report]({os.path.basename(detailed_report)})*\n")

def generate_simple_report(comments, output_file, repo_root, repo_url=None):
    """Generate a simplified and visually appealing annotation report."""
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

        f.write("## 🔍 At a glance\n\n")
        total = len(comments)
        f.write(f"**{total}** annotations found in the code\n\n")

        max_count = max(priority_counts.values()) if priority_counts else 1
        write_priority_section(f, priority_counts, total, max_count)

        write_types_section(f, grouped_comments)

        write_urgent_comments_section(f, urgent_comments, repo_root)

        write_report_footer(f, output_file)

def generate_markdown_report(comments, output_file, repo_root, repo_url=None):
    """Generate a detailed Markdown report from the extracted comments."""
    grouped_comments = defaultdict(list)
    for comment in comments:
        grouped_comments[comment['type']].append(comment)

    current_date = dt.now().strftime('%Y-%m-%d')

    priority_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for comment in comments:
        priority_counts[comment['priority']] += 1

    total_comments = len(comments)
    total_urgent = sum(1 for c in comments if c['priority'] == 1 or c['due_date'])
    urgent_comments = [c for c in comments if c['priority'] == 1 or c['due_date']]
    urgent_comments.sort(key=lambda x: (x['priority'], x['due_date'] or '9999-12-31'))

    oldest_comment = min(comments, key=lambda x: x['created'], default=None)
    newest_comment = max(comments, key=lambda x: x['created'], default=None)

    top_assignees = defaultdict(int)
    for comment in comments:
        for assignee in comment['assignees']:
            top_assignees[assignee] += 1
    top_assignees = sorted(top_assignees.items(), key=lambda x: x[1], reverse=True)[:5]

    due_comments = [c for c in comments if c['due_date']]
    due_comments.sort(key=lambda x: x['due_date'])

    with open(output_file, 'w', encoding='utf-8') as f:
        write_md_header_toc(f, current_date, COMMENT_TYPES, grouped_comments)
        write_md_summary(f, comments, oldest_comment, newest_comment, top_assignees, due_comments)
        write_md_statistics(f, grouped_comments, total_comments, priority_counts, {k: len(v) for k, v in grouped_comments.items()})
        write_md_comments_by_type(f, grouped_comments, repo_root, repo_url)
        write_md_comments_by_priority(f, comments, priority_counts, repo_root, repo_url)

def write_md_header_toc(file, current_date, comment_types, grouped_comments):
    """Write markdown report header and table of contents."""
    file.write(f"# Code Annotations Report\n\n")
    file.write(f"*Generated on {current_date}*\n\n")
    file.write(f"This report lists all annotations found in the source code.\n\n")

    file.write("## Table of Contents\n\n")
    file.write("- [Summary](#summary)\n")
    file.write("- [Statistics](#statistics)\n")

    for comment_type in comment_types:
        if comment_type in grouped_comments:
            count = len(grouped_comments[comment_type])
            emoji = COMMENT_TYPES[comment_type]["emoji"]
            description = COMMENT_TYPES[comment_type]["description"]
            file.write(f"- [{emoji} {description} ({count})](#user-content-{comment_type.lower().replace(' ', '-')})\n")

    file.write("- [By priority](#by-priority)\n")

def write_md_summary(file, comments, oldest_comment, newest_comment, top_assignees, due_comments):
    """Write summary section of markdown report."""
    file.write("\n## Summary\n\n")
    total = len(comments)
    file.write(f"**Total annotations:** {total}\n\n")

    if oldest_comment:
        oldest_age = calculate_age_in_days(oldest_comment['created'])
        file.write(f"**Oldest annotation:** {oldest_age} days ({oldest_comment['created']})\n")
        file.write(f"- {oldest_comment['file']}:{oldest_comment['line']} - {oldest_comment['text']}\n\n")

    if newest_comment:
        newest_age = calculate_age_in_days(newest_comment['created'])
        file.write(f"**Most recent annotation:** {newest_age} days ({newest_comment['created']})\n")
        file.write(f"- {newest_comment['file']}:{newest_comment['line']} - {newest_comment['text']}\n\n")

    if top_assignees:
        file.write("**Top contributors:**\n")
        for assignee, count in top_assignees:
            file.write(f"- @{assignee}: {count} annotations\n")
        file.write("\n")

    if due_comments:
        file.write("**Upcoming deadlines:**\n")
        for comment in due_comments[:5]:
            file.write(f"- {comment['due_date']} - {comment['file']}:{comment['line']} - {comment['text']}\n")
        file.write("\n")

def write_md_statistics(file, grouped_comments, total, priority_counts, assignees_count):
    """Write statistics section of markdown report."""
    file.write("## Statistics\n\n")

    file.write("### By type\n\n")
    file.write("| Type | Count | Percentage |\n")
    file.write("|------|-------|------------|\n")
    for comment_type in COMMENT_TYPES:
        if comment_type in grouped_comments:
            count = len(grouped_comments[comment_type])
            percentage = (count / total) * 100 if total > 0 else 0
            emoji = COMMENT_TYPES[comment_type]["emoji"]
            file.write(f"| {emoji} {comment_type} | {count} | {percentage:.1f}% |\n")
    file.write("\n")

    file.write("### By priority\n\n")
    file.write("| Priority | Count | Percentage |\n")
    file.write("|----------|-------|------------|\n")
    for priority in sorted(priority_counts.keys()):
        count = priority_counts[priority]
        percentage = (count / total) * 100 if total > 0 else 0
        priority_label = generate_priority_label(priority).replace("**", "")
        file.write(f"| {priority_label} | {count} | {percentage:.1f}% |\n")
    file.write("\n")

    if assignees_count:
        file.write("### By assignee\n\n")
        file.write("| Assignee | Count | Percentage |\n")
        file.write("|----------|-------|------------|\n")
        for assignee, count in sorted(assignees_count.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100 if total > 0 else 0
            file.write(f"| @{assignee} | {count} | {percentage:.1f}% |\n")
        file.write("\n")

def format_comment_metadata(comment, repo_url):
    """Format metadata for a comment."""
    metadata = []

    if comment['priority'] <= 2:  # Only for high priorities
        metadata.append(generate_priority_label(comment['priority']))

    if comment['due_date']:
        days_to_due = calculate_days_to_due(comment['due_date'])
        due_status = "🚨 **OVERDUE**" if days_to_due < 0 else f"⏰ Due in {days_to_due} days"
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
    age_text = f"{age} days ago" if age < 999 else "unknown date"
    metadata.append(f"📅 Created {age_text} by {comment['author']}")

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

def generate_json_data(comments, output_file, repo_root):
    """Generate JSON data from comments."""
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)
