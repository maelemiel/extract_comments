# Guide d'utilisation des annotations dans le code

Ce guide explique comment utiliser les annotations dans le code pour faciliter le suivi des tâches, bugs et autres points d'attention.

## Types d'annotations supportés

| Type | Description | Priorité par défaut |
|------|-------------|---------------------|
| TODO | Tâches à accomplir | Moyenne |
| FIXME | Problèmes critiques à résoudre | Critique |
| BUG | Bugs connus | Critique |
| HACK | Solutions temporaires | Élevée |
| NOTE | Notes importantes | Moyenne |
| TEMP | Code temporaire | Élevée |
| IN PROGRESS | Travail en cours | Élevée |
| OPTIMIZE | Optimisations nécessaires | Moyenne |
| REVIEW | Code à revoir | Élevée |
| QUESTION | Questions à clarifier | Élevée |
| IDEA | Idées à explorer | Moyenne |

## Format des annotations

### Format de base

// TODO: Description de la tâche à accomplir

### Avec métadonnées

// TODO: Implémenter la pagination @maelemiel P1 DUE:2025-05-15 #123 CREATED:2025-04-10

## Métadonnées supportées

- **Assignation**: `@username` - Personne responsable de la tâche
- **Priorité**: `P1` à `P4` où:
  - `P1` = Critique (🔴)
  - `P2` = Élevée (🟠)
  - `P3` = Moyenne (🟡)
  - `P4` = Basse (🟢)
- **Date d'échéance**: `DUE:YYYY-MM-DD` - Date limite pour compléter la tâche
- **Issue GitHub**: `#123` - Référence à une issue GitHub
- **Date de création**: `CREATED:YYYY-MM-DD` - Date de création de l'annotation (facultatif, détecté automatiquement via git blame)

## Exemples par langage

### JavaScript/TypeScript

```javascript
// TODO: Ajouter validation du formulaire @maelemiel P2 DUE:2025-05-01
// FIXME: Le bouton ne fonctionne pas sur Safari P1 #42
// NOTE: Cette approche pourrait être améliorée plus tard
```

### Python

```python
# TODO: Optimiser cette requête, elle est trop lente @maelemiel P3
# BUG: Exception levée avec des valeurs négatives P1 DUE:2025-04-20
```

### CSS/SCSS

```css
/* TEMP: Utiliser une couleur temporaire jusqu'à validation du design @designteam DUE:2025-05-15 */
```

### HTML

```html
<!-- TODO: Ajouter des attributs ARIA pour l'accessibilité @maelemiel P2 -->
```

### Bonnes pratiques

1) Soyez spécifique - Décrivez clairement ce qui doit être fait
2) Ajoutez un assigné - Utilisez @username pour indiquer qui est responsable
3) Définissez une priorité - Ajoutez P1-P4 selon l'importance
4) Liez aux issues - Utilisez #123 pour référencer une issue GitHub
5) Fixez des échéances - Utilisez DUE:YYYY-MM-DD pour les tâches à date fixe
