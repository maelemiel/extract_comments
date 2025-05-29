import subprocess
import re
from datetime import datetime as dt

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
