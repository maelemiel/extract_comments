# Guide to Using Code Annotations

This guide explains how to use annotations in code to facilitate tracking of tasks, bugs, and other important points.

## Supported Annotation Types

| Type | Description | Default Priority |
|------|-------------|------------------|
| TODO | Tasks to be completed | Medium |
| FIXME | Critical issues to fix | Critical |
| BUG | Known bugs | Critical |
| HACK | Temporary solutions | High |
| NOTE | Important notes | Medium |
| TEMP | Temporary code | High |
| IN PROGRESS | Work in progress | High |
| OPTIMIZE | Needed optimizations | Medium |
| REVIEW | Code to review | High |
| QUESTION | Questions to clarify | High |
| IDEA | Ideas to explore | Medium |

## Annotation Format

### Basic Format

// TODO: Description of the task to be completed

### With Metadata

// TODO: Implement pagination @maelemiel P1 DUE:2025-05-15 #123 CREATED:2025-04-10

## Supported Metadata

- **Assignee**: `@username` - Person responsible for the task
- **Priority**: `P1` to `P4` where:
  - `P1` = Critical (🔴)
  - `P2` = High (🟠)
  - `P3` = Medium (🟡)
  - `P4` = Low (🟢)
- **Due date**: `DUE:YYYY-MM-DD` - Deadline to complete the task
- **GitHub Issue**: `#123` - Reference to a GitHub issue
- **Creation date**: `CREATED:YYYY-MM-DD` - Date the annotation was created (optional, automatically detected via git blame)

## Examples by Language

### JavaScript/TypeScript

```javascript
// TODO: Add form validation @maelemiel P2 DUE:2025-05-01
// FIXME: Button does not work on Safari P1 #42
// NOTE: This approach could be improved later
```

### Python

```python
# TODO: Optimize this query, it's too slow @maelemiel P3
# BUG: Exception raised with negative values P1 DUE:2025-04-20
```

### CSS/SCSS

```css
/* TEMP: Use a temporary color until design is validated @designteam DUE:2025-05-15 */
```

### HTML

```html
<!-- TODO: Add ARIA attributes for accessibility @maelemiel P2 -->
```

### Best Practices

1) Be specific - Clearly describe what needs to be done
2) Add an assignee - Use @username to indicate who is responsible
3) Set a priority - Add P1-P4 according to importance
4) Link to issues - Use #123 to reference a GitHub issue
5) Set deadlines - Use DUE:YYYY-MM-DD for tasks with a fixed date
