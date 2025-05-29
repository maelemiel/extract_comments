import argparse
import os
from src.core import find_code_files, extract_comments, COMMENT_TYPES
from src.report import generate_simple_report, generate_markdown_report, generate_json_data
import importlib.util
import sys
import pathlib

# Import dynamique de report_html compatible PyInstaller et exécution source
candidates = []
if hasattr(sys, '_MEIPASS'):
    root_path = pathlib.Path(sys._MEIPASS)
    # PyInstaller : racine du bundle puis src/
    candidates.append(root_path / "report_html.py")
    candidates.append(root_path / "src" / "report_html.py")
# Toujours ajouter le chemin source pour fallback
candidates.append(pathlib.Path(__file__).parent / "report_html.py")

report_html_path = None
for path in candidates:
    if path.exists():
        report_html_path = path
        break
if not report_html_path:
    raise FileNotFoundError(f"report_html.py introuvable dans : {[str(p) for p in candidates]}\nVérifiez l'option --add-data de PyInstaller et la présence du fichier.")

spec = importlib.util.spec_from_file_location("report_html", str(report_html_path))
report_html = importlib.util.module_from_spec(spec)
sys.modules["report_html"] = report_html
spec.loader.exec_module(report_html)
generate_html_dashboard = report_html.generate_html_dashboard

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
    parser.add_argument('--per-branch', action='store_true', help='Generate a report for each Git branch')
    args = parser.parse_args()

    if args.per_branch:
        import subprocess
        import shutil
        # Récupérer la branche courante
        current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True).strip()
        # Lister toutes les branches locales
        branches = subprocess.check_output(['git', 'branch', '--format', '%(refname:short)'], universal_newlines=True).splitlines()
        for branch in branches:
            print(f"\n[extract_comments] Checkout branche: {branch}")
            subprocess.check_call(['git', 'checkout', branch])
            branch_dir = os.path.join('reports', branch)
            os.makedirs(branch_dir, exist_ok=True)
            output_md = os.path.join(branch_dir, 'rapport.md')
            output_json = os.path.join(branch_dir, 'rapport.json')
            # Réutilise la logique d'extraction
            extensions = args.extensions if args.extensions else DEFAULT_EXTENSIONS
            all_comments = []
            file_count = 0
            for file_path in find_code_files(args.directory, extensions, args.exclude):
                file_comments = extract_comments(file_path, COMMENT_TYPES.keys())
                all_comments.extend(file_comments)
                file_count += 1
            if all_comments:
                print(f"Génération du rapport pour {branch}...")
                generate_simple_report(all_comments, output_md, args.directory, args.repo_url)
                generate_json_data(all_comments, output_json, args.directory)
                # Générer le dashboard HTML pour la branche
                try:
                    html_output = os.path.join(branch_dir, 'dashboard.html')
                    generate_html_dashboard(output_json, html_output, branch=branch)
                    print(f"Dashboard HTML généré dans {html_output}")
                except Exception as e:
                    print(f"[WARN] Dashboard HTML non généré pour {branch}: {e}")
            else:
                print(f"Aucune annotation trouvée sur {branch}.")
        # Retour à la branche initiale
        subprocess.check_call(['git', 'checkout', current_branch])
        print(f"\nRetour à la branche initiale: {current_branch}")
        return

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
    
    # Après la génération du JSON, produire un dashboard HTML
    try:
        html_output = os.path.splitext(args.json_output)[0] + '_dashboard.html'
        generate_html_dashboard(args.json_output, html_output)
        print(f"Dashboard HTML généré dans {html_output}")
    except Exception as e:
        print(f"[WARN] Dashboard HTML non généré: {e}")
        
    print(f"Total files scanned: {file_count}")
    print(f"Total annotations found: {len(all_comments)}")
    print(f"Report generated in {args.output}")
    print(f"JSON data generated in {args.json_output}")
