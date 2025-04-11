# Exemple d'utilisation d'Extract Comments

Ce dossier contient un exemple de projet pour démontrer les fonctionnalités d'`extract_comments.py`.

## Structure du projet

- `app.py` : Application Python fictive
- `script.js` : JavaScript avec diverses annotations
- `styles.css` : Fichier CSS pour le style
- `index.html` : Page HTML simple

## Types d'annotations présents

- TODO
- FIXME
- BUG
- HACK
- NOTE
- OPTIMIZE
- REVIEW
- QUESTION
- IDEA

## Comment exécuter l'extraction sur cet exemple

Pour analyser uniquement ce répertoire d'exemples, exécutez la commande:

```bash
cd ..
python3 extract_comments.py --directory ./examples --output ./examples/rapport.md --json-output ./examples/rapport.json --simple
```

Ou

```bash
chmod +x extract_comments.py
./extract_comments.py --directory ./examples --output ./examples/rapport.md --json-output ./examples/rapport.json --simple
```

Ou

```bash
chmod +x run_example.sh
./run_example.sh
```

Cela générera:

- `./examples/rapport.md` - Rapport simplifié
- `./examples/rapport_detailed.md` - Rapport détaillé
- `./examples/rapport.json` - Données au format JSON
