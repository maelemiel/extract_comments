#!/bin/bash

cd "$(dirname "$0")/.."

echo -e "Exécution de l'extraction des commentaires sur le dossier d'exemples...\n"

python3 ./extract_comments.py \
  --directory ./examples \
  --output ./examples/rapport.md \
  --json-output ./examples/rapport.json \
  --simple

echo ""
echo "Extraction terminée!"
echo "Rapports générés:"
echo "- ./examples/rapport.md (simplifié)"
echo "- ./examples/rapport_detailed.md (détaillé)"
echo "- ./examples/rapport.json (données JSON)"
echo ""
echo "Ouvrez ces fichiers pour voir le résultat de l'extraction."
