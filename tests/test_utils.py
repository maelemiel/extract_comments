import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.utils import calculate_age_in_days, generate_priority_label, format_due_date_text, format_assignees_text, generate_progress_bar
from datetime import datetime, timedelta

def test_calculate_age_in_days():
    today = datetime.now().strftime('%Y-%m-%d')
    assert calculate_age_in_days(today) == 0
    old = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    assert calculate_age_in_days(old) == 10
    assert calculate_age_in_days('Unknown') == 999
    assert calculate_age_in_days('invalid') == 999

def test_generate_priority_label():
    assert generate_priority_label(1).startswith('🔴')
    assert generate_priority_label(2).startswith('🟠')
    assert generate_priority_label(3).startswith('🟡')
    assert generate_priority_label(4).startswith('🟢')
    assert 'P5' in generate_priority_label(5)

def test_format_due_date_text():
    future = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    past = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    assert 'Dans' in format_due_date_text(future)
    assert 'retard' in format_due_date_text(past)
    assert format_due_date_text(None) == ''

def test_format_assignees_text():
    assert format_assignees_text(['alice', 'bob']) == '👤 @alice, @bob'
    assert format_assignees_text([]) == ''

def test_generate_progress_bar():
    assert generate_progress_bar(5, 10, 10) == '█████░░░░░'
    assert generate_progress_bar(0, 10, 10) == '░░░░░░░░░░'
    assert generate_progress_bar(10, 10, 10) == '██████████'
