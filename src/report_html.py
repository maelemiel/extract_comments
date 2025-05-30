import json
import os
from collections import Counter, defaultdict

def generate_html_dashboard(json_path, output_path, branch=None):
    """
    Génère un tableau de bord HTML interactif à partir du fichier JSON d'annotations.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        comments = json.load(f)

    # Statistiques globales
    total = len(comments)
    by_type = Counter(c['type'] for c in comments)
    by_priority = Counter(c['priority'] for c in comments)
    by_author = Counter(c.get('author', 'Unknown') for c in comments)
    by_assignee = Counter(a for c in comments for a in c.get('assignees', []) if a)

    # Préparation des données pour le JS
    comments_js = json.dumps(comments, ensure_ascii=False)
    branch_title = f"<h2>Branche : {branch}</h2>" if branch else ""

    html = f"""
<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <title>Code Annotations Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; background: #f9f9f9; }}
        h1 {{ color: #2c3e50; }}
        .stats, .filters {{ margin-bottom: 2em; }}
        table {{ border-collapse: collapse; width: 100%; background: #fff; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background: #f0f0f0; }}
        tr:hover {{ background: #f5f5f5; }}
        .tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.9em; margin-right: 4px; }}
        .prio1 {{ background: #e74c3c; color: #fff; }}
        .prio2 {{ background: #f39c12; color: #fff; }}
        .prio3 {{ background: #f1c40f; color: #222; }}
        .prio4 {{ background: #2ecc71; color: #fff; }}
        ul.stats-list {{ margin: 0 0 0 1em; padding: 0; }}
        ul.stats-list li {{ list-style: disc; margin-left: 1em; }}
    </style>
</head>
<body>
    <h1>📊 Code Annotations Dashboard</h1>
    {branch_title}
    <div class='stats'>
        <b>Total annotations :</b> {total}<br>
        <b>By type :</b>
        <ul class='stats-list'>
            {''.join(f'<li><b>{k}</b> : {v}</li>' for k, v in by_type.items())}
        </ul>
        <b>By priority :</b>
        <ul class='stats-list'>
            {''.join(f'<li><b>P{k}</b> : {v}</li>' for k, v in by_priority.items())}
        </ul>
        <b>By author :</b>
        <ul class='stats-list'>
            {''.join(f'<li><b>{k}</b> : {v}</li>' for k, v in by_author.items())}
        </ul>
        <b>By assignee :</b>
        <ul class='stats-list'>
            {''.join(f'<li><b>{k}</b> : {v}</li>' for k, v in by_assignee.items())}
        </ul>
    </div>
    <div class='filters'>
        <label>Type: <select id='typeFilter'><option value=''>All</option></select></label>
        <label>Priority: <select id='prioFilter'><option value=''>All</option></select></label>
        <label>Assignee: <select id='assigneeFilter'><option value=''>All</option></select></label>
        <label>Author: <select id='authorFilter'><option value=''>All</option></select></label>
    </div>
    <table id='annotationsTable'>
        <thead>
            <tr>
                <th>Type</th><th>Text</th><th>File</th><th>Line</th><th>Priority</th><th>Assignees</th><th>Author</th><th>Due</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>
    <script>
    const data = {comments_js};
    const typeSet = new Set(data.map(c => c.type));
    const prioSet = new Set(data.map(c => c.priority));
    const assigneeSet = new Set(data.flatMap(c => c.assignees || []));
    const authorSet = new Set(data.map(c => c.author || 'Unknown'));
    // Remplir les filtres
    for (const t of typeSet) document.getElementById('typeFilter').innerHTML += `<option>${{t}}</option>`;
    for (const p of prioSet) document.getElementById('prioFilter').innerHTML += `<option>${{p}}</option>`;
    for (const a of assigneeSet) document.getElementById('assigneeFilter').innerHTML += `<option>${{a}}</option>`;
    for (const a of authorSet) document.getElementById('authorFilter').innerHTML += `<option>${{a}}</option>`;
    function renderTable() {{
        const type = document.getElementById('typeFilter').value;
        const prio = document.getElementById('prioFilter').value;
        const assignee = document.getElementById('assigneeFilter').value;
        const author = document.getElementById('authorFilter').value;
        const tbody = document.querySelector('#annotationsTable tbody');
        tbody.innerHTML = '';
        data.filter(c =>
            (!type || c.type === type) &&
            (!prio || c.priority == prio) &&
            (!assignee || (c.assignees && c.assignees.includes(assignee))) &&
            (!author || c.author === author)
        ).forEach(c => {{
            tbody.innerHTML += `<tr>
                <td>${{c.type}}</td>
                <td>${{c.text}}</td>
                <td>${{c.file}}:${{c.line}}</td>
                <td>${{c.line}}</td>
                <td><span class='tag prio${{c.priority}}'>P${{c.priority}}</span></td>
                <td>${{(c.assignees||[]).map(a=>`<span class='tag'>@${{a}}</span>`).join(' ')}}</td>
                <td>${{c.author||''}}</td>
                <td>${{c.due_date||''}}</td>
            </tr>`;
        }});
    }}
    document.querySelectorAll('.filters select').forEach(sel => sel.onchange = renderTable);
    renderTable();
    </script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
