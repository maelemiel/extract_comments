# 📋 Extract Comments

A powerful tool to extract, analyze, and visualize annotations in your source code.

![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📝 Description

`extract_comments` is a command-line tool that scans your code to extract special comments (TODO, FIXME, BUG, etc.) and generates detailed Markdown reports, interactive HTML dashboards, and JSON exports. It helps you track all your tasks and issues directly from your codebase.

---

## ✨ Main Features

- **Smart extraction**: Detects all important annotation types
- **Rich metadata**: Assignees, priorities, due dates, GitHub links
- **Interactive HTML dashboard**: Modern, filterable visualization
- **Multi-branch reports**: Automatically generates a report for each Git branch
- **Flexible configuration**: Via YAML/JSON config file or CLI options
- **Folder exclusion**: Easily ignore decorative or bulky folders
- **PyInstaller compatibility**: Works as a standalone binary
- **CI/CD integration**: Ready-to-use GitHub Actions workflow

---

## 🚀 Installation

No external dependencies required. Simply clone this repository:

```bash
git clone https://github.com/maelemiel/extract_comments.git
cd extract_comments
```

To generate an executable:

```bash
make
```

---

## 📊 Supported Annotation Types

| Type         | Emoji | Description                  | Default Priority |
|--------------|-------|------------------------------|-----------------|
| TODO         | ✅    | Tasks to do                  | 2               |
| FIXME        | 🚨    | Critical issues to fix       | 1               |
| BUG          | 🐛    | Known bugs                   | 1               |
| HACK         | ⚙️    | Temporary solutions          | 2               |
| NOTE         | 📝    | Important notes              | 3               |
| TEMP         | 🕒    | Temporary code               | 2               |
| IN PROGRESS  | 🚧    | In progress                  | 2               |
| OPTIMIZE     | ⚡    | Optimizations to make        | 3               |
| REVIEW       | 👀    | Code to review               | 2               |
| QUESTION     | ❓    | Questions to clarify         | 2               |
| IDEA         | 💡    | Ideas to explore             | 3               |

---

## 🛠️ Quick Usage

### Basic Command

```bash
./extract_comments --directory /path/to/project
```

### Main Options

```
usage: extract_comments [-h] [--directory DIRECTORY] [--output OUTPUT] [--json-output JSON_OUTPUT]
                          [--extensions EXTENSIONS ...] [--repo-url REPO_URL]
                          [--exclude EXCLUDE ...] [--simple] [--per-branch] [--config CONFIG]

options:
  -h, --help            Show help message
  --directory, -d       Directory to scan (default: current directory)
  --output, -o          Output Markdown file
  --json-output, -j     Output JSON file
  --extensions, -e      File extensions to scan
  --repo-url, -r        GitHub repository URL (for links)
  --exclude, -x         Folders to exclude
  --simple, -s          Generate a simplified report/dashboard
  --per-branch          Generate a report for each Git branch
  --config, -c          YAML or JSON configuration file
```

### Usage Examples

- **Simplified report on a project:**

```bash
./extract_comments -d ./myproject -s
```

- **Multi-branch report with HTML dashboard:**

```bash
./extract_comments -d ./myproject --per-branch --simple
```

- **Using a configuration file:**

```bash
./extract_comments -c config.yaml
```

- **Exclude decorative folders:**

```bash
./extract_comments -d ./myproject -x node_modules tests examples
```

- **From a PyInstaller executable:**

```bash
./dist/extract_comments --config config.yaml
```

---

## ⚙️ Advanced Configuration

You can define all options in a `config.yaml` or `config.json` file:

```yaml
directory: ./myproject
output: ./docs/annotations.md
json_output: ./docs/annotations.json
exclude:
  - node_modules
  - tests
  - examples
repo_url: https://github.com/username/myproject
simple: true
per_branch: true
```

CLI options override those in the config file.

---

## 📌 How to Annotate Your Code

- **Basic syntax:**

```python
# TODO: Implement form validation
```

```javascript
// FIXME: Fix image loading
```

- **Add metadata:**

```python
# TODO: Optimize search @alice P1 DUE:2025-12-31 #42
```

- **Supported metadata:**
  - `@username`: assignee
  - `P1`, `P2`, ...: priority
  - `DUE:YYYY-MM-DD`: due date
  - `#123`: GitHub issue
  - `CREATED:YYYY-MM-DD`: creation date

---

## 📂 Output Formats

- **Simplified Markdown**: visual dashboard, urgent list, charts
- **Detailed Markdown**: statistics, grouped by type/priority, full metadata
- **JSON**: structured data for integration
- **HTML**: interactive dashboard (filtering, search, stats)

---

## 🖥️ Interactive HTML Dashboard

After extraction, a modern HTML dashboard is generated (filterable, interactive, ready to integrate into your docs or CI/CD).

---

## 🔄 GitHub Actions Integration (CI/CD)

Automate extraction with the provided workflow:

```yaml
name: Extract Code Annotations
on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]
  schedule:
    - cron: '0 9 * * 1'
jobs:
  extract-comments:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Extract comments
      run: |
        python ./extract_comments \
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

---

## 🤝 Contributing

Contributions are welcome! Open an issue or a pull request.

---

## 📄 License

Project under the MIT license. See the LICENSE file.

---

> For any questions or suggestions, contact [@maelemiel](https://github.com/maelemiel).
