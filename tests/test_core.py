import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.core import parse_comment_metadata, clean_comment_text, extract_comments, COMMENT_TYPES

@pytest.mark.parametrize("comment_text,comment_type,expected", [
    ("Faire ceci @alice P1 DUE:2025-12-31 #42 CREATED:2025-01-01", "TODO", {
        'assignees': ['alice'],
        'priority': 1,
        'due_date': '2025-12-31',
        'issue': '42',
        'created_match': True
    }),
    ("Corriger bug @bob P2", "BUG", {
        'assignees': ['bob'],
        'priority': 2,
        'due_date': None,
        'issue': None,
        'created_match': False
    })
])
def test_parse_comment_metadata(comment_text, comment_type, expected):
    meta = parse_comment_metadata(comment_text, comment_type)
    assert meta['assignees'] == expected['assignees']
    assert meta['priority'] == expected['priority']
    assert meta['due_date'] == expected['due_date']
    assert meta['issue'] == expected['issue']
    if expected['created_match']:
        assert meta['created_match'] is not None
    else:
        assert meta['created_match'] is None

def test_clean_comment_text():
    comment = "Faire ceci @alice P1 DUE:2025-12-31 #42 CREATED:2025-01-01"
    cleaned = clean_comment_text(comment)
    assert "@alice" not in cleaned
    assert "P1" not in cleaned
    assert "DUE:" not in cleaned
    assert "#42" not in cleaned
    assert "CREATED:" not in cleaned
    assert "Faire ceci" in cleaned

def test_extract_comments(tmp_path):
    file = tmp_path / "test.py"
    file.write_text("""
# TODO: Faire ceci @alice P1 DUE:2025-12-31 #42 CREATED:2025-01-01
# BUG: Corriger bug @bob P2
""")
    comments = list(extract_comments(str(file), COMMENT_TYPES.keys()))
    assert len(comments) == 2
    assert comments[0]['type'] == 'TODO'
    assert 'alice' in comments[0]['assignees']
    assert comments[1]['type'] == 'BUG'
    assert 'bob' in comments[1]['assignees']

def test_parse_comment_metadata_no_meta():
    comment = "Juste un commentaire simple"
    meta = parse_comment_metadata(comment, "TODO")
    assert meta['assignees'] == []
    assert meta['priority'] == 2  # priorité par défaut TODO
    assert meta['due_date'] is None
    assert meta['issue'] is None
    assert meta['created_match'] is None

def test_clean_comment_text_no_meta():
    comment = "Juste un commentaire simple"
    cleaned = clean_comment_text(comment)
    assert cleaned == "Juste un commentaire simple"

def test_extract_comments_no_match(tmp_path):
    file = tmp_path / "test2.py"
    file.write_text("""
print('Hello world')
# Un commentaire sans tag reconnu
""")
    comments = list(extract_comments(str(file), COMMENT_TYPES.keys()))
    assert comments == []

def test_extract_comments_empty_file(tmp_path):
    file = tmp_path / "empty.py"
    file.write_text("")
    comments = list(extract_comments(str(file), COMMENT_TYPES.keys()))
    assert comments == []

def test_parse_comment_metadata_priority_fallback():
    comment = "TODO: tâche sans priorité explicite"
    meta = parse_comment_metadata(comment, "TODO")
    assert meta['priority'] == 2  # priorité par défaut TODO
