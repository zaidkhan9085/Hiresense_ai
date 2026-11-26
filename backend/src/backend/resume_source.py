"""Where resume text comes from (Phase 1: classes, Protocol, pathlib).

A ResumeSource is anything that can hand us raw resume texts. Today: a folder of .txt files
and an in-memory dict (for tests). Later (Phase 4): PDF/DOCX uploads, the same interface.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from backend.resume_parser import Resume, parse_resume


@dataclass(frozen=True)
class RawResume:
    source_id: str  # where it came from, e.g. "asha_verma.txt"
    text: str


class ResumeSource(Protocol):
    """Interface: any class with a matching read_all() method counts as a ResumeSource."""

    def read_all(self) -> list[RawResume]: ...


class DirectoryResumeSource:
    """Reads every *.txt file in one folder (not sub-folders), in name order."""

    def __init__(self, directory: Path, pattern: str = "*.txt") -> None:
        self.directory = directory
        self.pattern = pattern

    def read_all(self) -> list[RawResume]:
        if not self.directory.is_dir():
            raise FileNotFoundError(f"Resume folder not found: {self.directory}")
        return [
            RawResume(source_id=path.name, text=path.read_text(encoding="utf-8"))
            for path in sorted(self.directory.glob(self.pattern))
            if path.is_file()
        ]


class InMemoryResumeSource:
    """Holds texts in a dict, which makes tests fast and needs no files."""

    def __init__(self, texts: dict[str, str]) -> None:
        self.texts = texts

    def read_all(self) -> list[RawResume]:
        return [RawResume(source_id=key, text=value) for key, value in self.texts.items()]


@dataclass
class LoadResult:
    resumes: list[Resume] = field(default_factory=list)
    errors: dict[str, str] = field(default_factory=dict)  # source_id -> error message


def load_resumes(source: ResumeSource) -> LoadResult:
    """Parse every resume from the source. One bad resume never stops the others."""
    result = LoadResult()
    for raw in source.read_all():
        try:
            result.resumes.append(parse_resume(raw.text))
        except ValueError as error:
            result.errors[raw.source_id] = str(error)
    return result
