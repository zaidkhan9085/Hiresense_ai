from pathlib import Path

import pytest

from backend.resume_source import (
    DirectoryResumeSource,
    InMemoryResumeSource,
    RawResume,
    load_resumes,
)

# tests/ -> backend/ -> repo root
SYNTHETIC_DIR = Path(__file__).resolve().parents[2] / "data" / "synthetic" / "resumes"


def test_directory_source_reads_only_txt_files_in_name_order(tmp_path: Path):
    # tmp_path is a pytest fixture: a fresh empty folder for each test, deleted afterwards.
    (tmp_path / "b.txt").write_text("Name: B", encoding="utf-8")
    (tmp_path / "a.txt").write_text("Name: A", encoding="utf-8")
    (tmp_path / "notes.md").write_text("ignore me", encoding="utf-8")

    raws = DirectoryResumeSource(tmp_path).read_all()

    assert raws == [RawResume("a.txt", "Name: A"), RawResume("b.txt", "Name: B")]


def test_directory_source_raises_for_missing_folder(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        DirectoryResumeSource(tmp_path / "does_not_exist").read_all()


def test_in_memory_source_returns_texts():
    source = InMemoryResumeSource({"one": "Name: One"})
    assert source.read_all() == [RawResume("one", "Name: One")]


def test_load_resumes_keeps_going_when_one_resume_is_bad():
    source = InMemoryResumeSource({"good": "Name: Good", "bad": "Email: x@example.com"})

    result = load_resumes(source)

    assert [r.name for r in result.resumes] == ["Good"]
    assert list(result.errors) == ["bad"]


def test_synthetic_dataset_loads_without_errors():
    result = load_resumes(DirectoryResumeSource(SYNTHETIC_DIR))

    assert result.errors == {}
    assert sorted(r.name for r in result.resumes) == ["Asha Verma", "Meera Nair", "Ravi Iyer"]
