"""Parse a plain-text synthetic resume into a Resume object (Phase 1, Exercise 1).

Input format (one "Key: value" per line, blank lines allowed, keys case-insensitive):

    Name: Asha Verma
    Email: asha.verma@example.com
    Experience: 4.5
    Skills: Python, FastAPI, PostgreSQL

Run the tests:  uv run pytest -v
"""

from dataclasses import dataclass, field


@dataclass
class Resume:
    name: str
    email: str | None = None
    experience_years: float | None = None
    # `= []` would make every Resume share ONE list; default_factory builds a new list each time.
    skills: list[str] = field(default_factory=list)


def _parse_fields(text: str) -> dict[str, str]:
    """Turn "Key: value" lines into {"key": "value"}. Lines without ":" are skipped."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        key, separator, value = line.partition(":")
        if not separator:  # "" is falsy, so this means "no ':' in the line"
            continue
        fields[key.strip().lower()] = value.strip()
    return fields


def _parse_skills(raw: str) -> list[str]:
    """Split on commas, trim, drop empties, de-duplicate case-insensitively, keep order."""
    skills: list[str] = []
    seen: set[str] = set()
    for skill in raw.split(","):
        skill = skill.strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            skills.append(skill)
    return skills


def _parse_experience(raw: str | None) -> float | None:
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError as error:
        raise ValueError(f"Experience must be a number, got {raw!r}") from error


def parse_resume(text: str) -> Resume:
    """Convert resume text into a Resume. Raises ValueError if the name is missing."""
    fields = _parse_fields(text)

    name = fields.get("name")
    if not name:  # catches both a missing key (None) and an empty value ("")
        raise ValueError("Resume must include a non-empty 'Name' field")

    return Resume(
        name=name,
        email=fields.get("email"),
        experience_years=_parse_experience(fields.get("experience")),
        skills=_parse_skills(fields.get("skills", "")),
    )
