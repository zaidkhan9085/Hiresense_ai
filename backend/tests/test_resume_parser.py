import pytest

from backend.resume_parser import Resume, parse_resume

FULL_RESUME = """
Name: Asha Verma
Email: asha.verma@example.com
Experience: 4.5
Skills: Python, FastAPI, PostgreSQL
"""


def test_parses_all_fields():
    assert parse_resume(FULL_RESUME) == Resume(
        name="Asha Verma",
        email="asha.verma@example.com",
        experience_years=4.5,
        skills=["Python", "FastAPI", "PostgreSQL"],
    )


def test_keys_are_case_insensitive_and_values_trimmed():
    resume = parse_resume("NAME:   Ravi Iyer  \nskills:  Django ")
    assert resume.name == "Ravi Iyer"
    assert resume.skills == ["Django"]


def test_optional_fields_default_when_missing():
    resume = parse_resume("Name: Meera Nair")
    assert resume.email is None
    assert resume.experience_years is None
    assert resume.skills == []


def test_skills_are_cleaned_and_deduplicated_in_order():
    resume = parse_resume("Name: Kabir Rao\nSkills: Python, , python, Docker,PYTHON , Redis")
    assert resume.skills == ["Python", "Docker", "Redis"]


def test_ignores_lines_without_colon():
    resume = parse_resume("Name: Neha Joshi\nThis line has no separator\n\n")
    assert resume.name == "Neha Joshi"


@pytest.mark.parametrize("text", ["Email: a@example.com", "Name:   "])
def test_missing_name_raises_value_error(text):
    with pytest.raises(ValueError):
        parse_resume(text)


def test_non_numeric_experience_raises_value_error():
    with pytest.raises(ValueError):
        parse_resume("Name: Arjun Das\nExperience: five years")


def test_two_resumes_do_not_share_skill_lists():
    first = parse_resume("Name: A")
    second = parse_resume("Name: B")
    first.skills.append("Go")
    assert second.skills == []
