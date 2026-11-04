import pytest
from aegis.skill_scout import (
    init_skill_scout_db,
    run_skill_scout,
    get_discovered_skills,
    mark_skill_status,
    format_skill_scout_display,
    get_installed_skills_inventory,
)


def test_init_and_run_skill_scout():
    init_skill_scout_db()
    skills = run_skill_scout()
    assert isinstance(skills, list)
    assert len(skills) > 0
    # Every skill has name, category, taste_score
    for s in skills:
        assert "name" in s
        assert "category" in s
        assert s["taste_score"] >= 80


def test_get_discovered_skills_filtering():
    skills = get_discovered_skills(status="recommended")
    assert isinstance(skills, list)
    assert all(s["status"] == "recommended" for s in skills)


def test_mark_skill_status():
    skills = get_discovered_skills(status="recommended")
    if skills:
        first = skills[0]
        name = first["name"]
        ok = mark_skill_status(name, "installed")
        assert ok is True
        
        remaining = [s["name"] for s in get_discovered_skills(status="recommended")]
        assert name not in remaining


def test_format_skill_scout_display():
    output = format_skill_scout_display()
    assert "AegisBrain Weekly Skill Scout" in output
    assert "Taste Match Algorithm" in output


def test_get_installed_skills_inventory():
    installed = get_installed_skills_inventory()
    assert isinstance(installed, list)
