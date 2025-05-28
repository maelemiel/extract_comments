# 📋 Extract Comments

A powerful tool to extract, analyze, and visualize annotations in your source code.


![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-%3E%3D3.6-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📝 Description

`extract_comments` is a command-line tool that scans your codebase to extract special comments (TODO, FIXME, BUG, etc.) and generates a detailed Markdown report. It helps you keep track of all your tasks and issues directly from your source code.

![Example](https://via.placeholder.com/800x400?text=Exemple+de+rapport)

## ✨ Features

- **Smart extraction** - Scans code files for important annotations
- **Rich metadata** - Support for assignees, priorities, due dates, and GitHub issue links
- **Beautiful visualization** - Generates Markdown reports with visual charts
- **Multiple formats** - Simplified, detailed reports and JSON data for integration
- **Highly configurable** - Filter by extension, exclude directories
- **Git integration** - Automatically detects authors and creation dates

## 🚀 Installation

No external dependencies required. Simply clone this repository:

```bash
git clone https://github.com/maelemiel/extract_comments.git
cd extract_comments
chmod +x extract_comments.py
```

## 📊 Supported Annotation Types

| Type | Emoji | Description | Default Priority |
|------|-------|-------------|---------------------|
| TODO | ✅ | Tasks to be done	 | 2 |
| FIXME | 🚨 | Critical issues to fix	 | 1 |
| BUG | 🐛 | Known bugs	 | 1 |
| HACK | ⚙️ | Temporary solutions	 | 2 |
| NOTE | 📝 | Important notes	 | 3 |
| TEMP | 🕒 | Temporary code	 | 2 |
| IN PROGRESS | 🚧 | Work in progress	 | 2 |
| OPTIMIZE | ⚡ | Optimizations needed	 | 3 |
| REVIEW | 👀 | Code to review	 | 2 |
| QUESTION | ❓ | Questions to clarify	 | 2 |
| IDEA | 💡 | Ideas to explore	 | 3 |

## 🛠️ Usage

### Basic Command

```bash
./extract_comments.py --directory /path/to/your/project
```

### Available Options

```
usage: extract_comments.py [-h] [--directory DIRECTORY] [--output OUTPUT] [--json-output JSON_OUTPUT]
                           [--extensions EXTENSIONS [EXTENSIONS ...]] [--repo-url REPO_URL]
                           [--exclude EXCLUDE [EXCLUDE ...]] [--simple]

Extract and analyze code annotations

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Directory to scan (default: current directory)
  --output OUTPUT, -o OUTPUT
                        Output Markdown file (default: docs/todos/code_annotations.md)
  --json-output JSON_OUTPUT, -j JSON_OUTPUT
                        Output JSON file (default: docs/todos/code_annotations.json)
  --extensions EXTENSIONS [EXTENSIONS ...], -e EXTENSIONS [EXTENSIONS ...]
                        File extensions to scan (default: common code extensions)
  --repo-url REPO_URL, -r REPO_URL
                        GitHub repository URL (e.g., https://github.com/username/repo)
  --exclude EXCLUDE [EXCLUDE ...], -x EXCLUDE [EXCLUDE ...]
                        Directories to exclude
  --simple, -s          Generate a simplified, prettier report
```

### Examples

#### Scan a project with a simplified report:

```bash
./extract_comments.py -d /home/user/projects/myapp -s
```

#### Specify specific file extensions:

```bash
./extract_comments.py -d /home/user/projects/myapp -e .js .ts .py
```

#### Exclude certain directories:

```bash
./extract_comments.py -d /home/user/projects/myapp -x node_modules tests vendor
```

#### Enable GitHub links:

```bash
./extract_comments.py -d /home/user/projects/myapp -r https://github.com/username/myapp
```

## 📌 Annotating Your Code

To ensure your comments are detected, follow these conventions:

### Basic Syntax

```python
# TODO: Implement form validation
```

```javascript
// FIXME: Fix image loading issue
```

```html
<!-- NOTE: Add class for responsive design -->
```

### Add Metadata

You can enrich your annotations with metadata:

```python
# TODO: Optimize search algorithm @john P2 DUE:2023-12-31 #42
```

#### Supported Metadata:

- **Assignee**: `@username` - Person responsible
- **Priority**: `P1`, `P2`, `P3`, `P4` (1 is highest)
- **Due Date**: `DUE:YYYY-MM-DD` - Deadline
- **GitHub Issue**: `#123` - Reference to an issue
- **Created Date**: `CREATED:YYYY-MM-DD` - Manual creation date

If no priority is set, a default priority is applied based on the annotation type.

## 📂 Output Formats

### Simplified Report (-s option)

A visual dashboard showing:
- Annotation summary
- Priority and type charts
- Urgent task list
- Visual progress indicators

### Detailed Report

A full documentation including:
- Table of contents
- Detailed statistics
- Annotations grouped by type and priority
- Full metadata for each annotation

### JSON Data

Structured data for integration with other tools:

```json
[
  {
    "type": "TODO",
    "text": "Implement validation",
    "file": "src/form.js",
    "line": 42,
    "assignees": ["john"],
    "priority": 2,
    "due_date": "2023-12-31",
    "issue": "42",
    "created": "2023-10-15",
    "author": "jane"
  }
]
```

## 🔄 GitHub Actions Integration

You can automate annotation extraction using GitHub Actions. An example workflow is included in this repository.

### Workflow Configuration

Create a file `.github/workflows/extract-comments.yml` in your repository:

```yaml
name: Extract Code Annotations

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]
  schedule:
    - cron: '0 9 * * 1' # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  extract-comments:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0  # Required for git blame

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Extract comments
      run: |
        python ./extract_comments.py \
          --directory . \
          --output docs/todos/code_annotations.md \
          --json-output docs/todos/code_annotations.json \
          --repo-url https://github.com/${{ github.repository }} \
          --simple \
          --exclude node_modules .git dist build

    - name: Commit changes
      run: |
        git config --global user.name 'GitHub Actions'
        git config --global user.email 'actions@github.com'
        git add docs/todos/code_annotations.md docs/todos/code_annotations.json docs/todos/code_annotations_detailed.md
        git diff --quiet && git diff --staged --quiet || git commit -m "Update code annotations report"
        git push
```

### Benefits of Automation

- **Always up-to-date reports**: Auto-generated after every push or on schedule
- **Living documentation**: Team always has access to the latest annotations
- **Task history**: Track annotation evolution over time
- **Team visibility**: Easily integrate reports into your project docs

### Workflow Customization

Vous pouvez personnaliser le workflow en modifiant:

- **Triggers**: Change monitored branches or schedule
- **Output directory**: Define where reports are saved
- **Exclusion options**: Adjust which folders are ignored
- **Report format**: Choose between simplified or detailed

This integration is especially useful for teams using annotations as a communication and task-tracking method within the code.

## 🔧 Customization

To customize annotation types and their default priorities, edit the `COMMENT_TYPES` section at the top of the script.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
