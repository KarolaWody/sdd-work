"""Tests for SDD Workflow CLI."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

SDD_PATH = Path(__file__).resolve().parent.parent / "sdd.py"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_sdd(*args, cwd=None, env=None):
    cmd = [sys.executable, str(SDD_PATH), *args]
    merged_env = {**os.environ, **(env or {})}
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=cwd, env=merged_env
    )
    return result


def specs_dir(path):
    return Path(path) / "specs"


def test_init_creates_specs_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_sdd("init", cwd=tmp)
        assert result.returncode == 0
        sd = specs_dir(tmp)
        assert sd.is_dir()
        for name in ["mission.md", "tech-stack.md", "roadmap.md", "state.md"]:
            assert (sd / name).is_file()


def test_init_on_existing_dir_skips_without_stdin():
    with tempfile.TemporaryDirectory() as tmp:
        sd = specs_dir(tmp)
        sd.mkdir()
        (sd / "custom.md").write_text("keep")
        result = run_sdd("init", cwd=tmp)
        assert result.returncode == 0
        assert (sd / "custom.md").exists()


def test_feature_requires_init_first():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_sdd("feature", "my-feature", cwd=tmp)
        assert result.returncode == 1
        assert "specs/ directory not found" in result.stderr


def test_feature_creates_spec_files():
    with tempfile.TemporaryDirectory() as tmp:
        run_sdd("init", cwd=tmp)
        result = run_sdd("feature", "my-feature", cwd=tmp)
        assert result.returncode == 0
        sd = specs_dir(tmp)
        for name in ["plan.md", "requirements.md", "validation.md"]:
            path = sd / name
            assert path.is_file()
            assert "my-feature" in path.read_text()


def test_feature_rejects_invalid_name():
    with tempfile.TemporaryDirectory() as tmp:
        run_sdd("init", cwd=tmp)
        result = run_sdd("feature", "UPPERCASE", cwd=tmp)
        assert result.returncode == 1
        assert "not a valid feature name" in result.stderr


def test_state_current_needs_init():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_sdd("state", "--current", cwd=tmp)
        assert result.returncode == 1
        assert "not found" in result.stderr


def test_state_current():
    with tempfile.TemporaryDirectory() as tmp:
        run_sdd("init", cwd=tmp)
        result = run_sdd("state", "--current", cwd=tmp)
        assert result.returncode == 0
        assert "State" in result.stdout


def test_state_append_skipped_noninteractive():
    with tempfile.TemporaryDirectory() as tmp:
        run_sdd("init", cwd=tmp)
        result = run_sdd("state", cwd=tmp)
        assert result.returncode == 0
        assert "Non-interactive" in result.stdout


def test_validate_no_specs():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_sdd("validate", cwd=tmp)
        assert result.returncode == 1
        assert "not found" in result.stderr


def test_validate_after_init():
    with tempfile.TemporaryDirectory() as tmp:
        run_sdd("init", cwd=tmp)
        result = run_sdd("validate", cwd=tmp)
        assert result.returncode in (0, 1)


def test_status_no_specs():
    with tempfile.TemporaryDirectory() as tmp:
        result = run_sdd("status", cwd=tmp)
        assert result.returncode == 0
        assert "No specs/" in result.stdout


def test_status_after_init():
    with tempfile.TemporaryDirectory() as tmp:
        run_sdd("init", cwd=tmp)
        result = run_sdd("status", cwd=tmp)
        assert result.returncode == 0
        assert "OK" in result.stdout


def test_help():
    result = run_sdd("--help")
    assert result.returncode == 0
    assert "SDD" in result.stdout or "Spec-Driven" in result.stdout


def test_init_help():
    result = run_sdd("init", "--help")
    assert result.returncode == 0


def test_invalid_command():
    result = run_sdd("nonexistent")
    assert result.returncode in (1, 2)


def test_has_content_direct():
    sys.path.insert(0, str(PROJECT_ROOT))
    import sdd
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "test.md"
        p.write_text("<!-- empty -->")
        assert not sdd._has_content(p)
        p.write_text("Real content here " * 20)
        assert sdd._has_content(p)
        assert not sdd._has_content(Path(tmp) / "missing.md")


def test_sanitize_md_direct():
    sys.path.insert(0, str(PROJECT_ROOT))
    import sdd
    assert sdd._sanitize_md("hello world") == "hello world"
    assert "\\# header" in sdd._sanitize_md("# header")
    assert "\\- item" in sdd._sanitize_md("- item")
    assert "\\> quote" in sdd._sanitize_md("> quote")
    result = sdd._sanitize_md("see [link](url)")
    assert "[link](url)" in result
    multi = sdd._sanitize_md("normal\n# header\nnormal")
    assert multi == "normal\n\\# header\nnormal"
    long_text = "x" * 3000
    assert len(sdd._sanitize_md(long_text)) <= 2000
