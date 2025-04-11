# 📋 Extract Comments

Un outil puissant pour extraire, analyser et visualiser les annotations dans votre code source.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-%3E%3D3.6-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📝 Description

`extract_comments` est un outil de ligne de commande qui analyse votre base de code pour extraire tous les commentaires spéciaux (TODO, FIXME, BUG, etc.) et génère un rapport détaillé au format Markdown. Il vous aide à garder une trace de toutes vos tâches et problèmes directement à partir de votre code source.

![Exemple de rapport](https://via.placeholder.com/800x400?text=Exemple+de+rapport)

## ✨ Fonctionnalités

- **Extraction intelligente** - Analyse les fichiers de code pour trouver les annotations importantes
- **Métadonnées riches** - Support pour assignés, priorités, échéances et liens vers issues GitHub
- **Visualisation élégante** - Génère des rapports Markdown avec graphiques visuels
- **Plusieurs formats** - Rapports simplifiés, détaillés et données JSON pour intégration
- **Hautement configurable** - Filtrage par extension, exclusion de répertoires
- **Intégration Git** - Détection automatique des auteurs et dates de création

## 🚀 Installation

Aucune dépendance externe n'est requise. Clonez simplement ce dépôt:

```bash
git clone https://github.com/username/extract_comments.git
cd extract_comments
chmod +x extract_comments.py
```

## 📊 Types d'annotations supportés

| Type | Emoji | Description | Priorité par défaut |
|------|-------|-------------|---------------------|
| TODO | ✅ | Tâches à accomplir | 2 |
| FIXME | 🚨 | Problèmes critiques à résoudre | 1 |
| BUG | 🐛 | Bugs connus | 1 |
| HACK | ⚙️ | Solutions temporaires | 2 |
| NOTE | 📝 | Notes importantes | 3 |
| TEMP | 🕒 | Code temporaire | 2 |
| IN PROGRESS | 🚧 | Travail en cours | 2 |
| OPTIMIZE | ⚡ | Optimisations nécessaires | 3 |
| REVIEW | 👀 | Code à revoir | 2 |
| QUESTION | ❓ | Questions à clarifier | 2 |
| IDEA | 💡 | Idées à explorer | 3 |

## 🛠️ Utilisation

### Commande de base

```bash
./extract_comments.py --directory /chemin/vers/votre/projet
```

### Options disponibles

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

### Exemples

#### Analyser un projet avec rapport simplifié:

```bash
./extract_comments.py -d /home/user/projects/myapp -s
```

#### Spécifier des extensions de fichier particulières:

```bash
./extract_comments.py -d /home/user/projects/myapp -e .js .ts .py
```

#### Exclure certains répertoires:

```bash
./extract_comments.py -d /home/user/projects/myapp -x node_modules tests vendor
```

#### Activer les liens GitHub:

```bash
./extract_comments.py -d /home/user/projects/myapp -r https://github.com/username/myapp
```

## 📌 Annotation de votre code

Pour que vos commentaires soient détectés, suivez ces conventions:

### Syntaxe de base

```python
# TODO: Implémenter la validation des formulaires
```

```javascript
// FIXME: Corriger le problème de chargement des images
```

```html
<!-- NOTE: Ajouter une classe pour le responsive design -->
```

### Ajouter des métadonnées

Vous pouvez enrichir vos annotations avec des métadonnées:

```python
# TODO: Optimiser l'algorithme de recherche @john P2 DUE:2023-12-31 #42
```

#### Métadonnées supportées:

- **Assigné**: `@username` - La personne responsable
- **Priorité**: `P1`, `P2`, `P3`, `P4` (1 étant la plus haute)
- **Date d'échéance**: `DUE:YYYY-MM-DD` - Date limite
- **Issue GitHub**: `#123` - Référence à une issue
- **Date de création**: `CREATED:YYYY-MM-DD` - Date de création manuelle

Si vous n'indiquez pas de priorité, une priorité par défaut sera assignée selon le type d'annotation.

## 📂 Formats de sortie

### Rapport simplifié (option `-s`)

Un tableau de bord visuel montrant:
- Résumé des annotations
- Graphiques de priorités et types
- Liste des tâches urgentes
- Indicateurs visuels de progression

### Rapport détaillé

Une documentation complète avec:
- Table des matières
- Statistiques détaillées
- Annotations groupées par type et priorité
- Métadonnées complètes pour chaque annotation

### Données JSON

Données structurées pour intégration avec d'autres outils:
```json
[
  {
    "type": "TODO",
    "text": "Implémenter la validation",
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

## 🔄 Intégration avec GitHub Actions

Vous pouvez automatiser l'extraction des annotations de code en utilisant GitHub Actions. Un exemple de workflow est fourni dans ce dépôt.

### Configuration du workflow

Créez un fichier `.github/workflows/extract-comments.yml` dans votre dépôt:

```yaml
name: Extract Code Annotations

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]
  # Exécute automatiquement tous les lundis à 9h00
  schedule:
    - cron: '0 9 * * 1'
  # Permet aussi de lancer manuellement
  workflow_dispatch:

jobs:
  extract-comments:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0  # Nécessaire pour git blame

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

### Avantages de l'automatisation

- **Rapports toujours à jour**: Génération automatique après chaque push ou à intervalle régulier
- **Documentation vivante**: Votre équipe a toujours accès aux dernières annotations
- **Historique des tâches**: Suivez l'évolution des annotations au fil du temps
- **Visibilité de l'équipe**: Intégrez facilement les rapports dans votre documentation de projet

### Personnalisation du workflow

Vous pouvez personnaliser le workflow en modifiant:

- **Déclencheurs**: Changez les branches surveillées ou la planification
- **Répertoire de sortie**: Définissez où les rapports sont générés
- **Options d'exclusion**: Adaptez les dossiers à ignorer
- **Format de rapport**: Choisissez entre rapport simplifié ou détaillé

Cette intégration est particulièrement utile pour les équipes qui utilisent activement les annotations comme moyen de communication et de suivi des tâches dans le code.

## 🔧 Personnalisation

Pour personnaliser les types d'annotations et leurs priorités par défaut, modifiez la section `COMMENT_TYPES` au début du script.

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.