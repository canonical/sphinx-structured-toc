from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.mark.slow
def test_package_docs_build(tmp_path: Path):
    project_root = Path(__file__).parents[2]
    build_dir = tmp_path / "html"

    subprocess.run(
        [
            "uv",
            "run",
            "--with-requirements",
            str(project_root / "docs" / "requirements.txt"),
            "sphinx-build",
            "-b",
            "html",
            "-W",
            str(project_root / "docs"),
            str(build_dir),
        ],
        check=True,
    )


@pytest.mark.slow
def test_package_docs_latex_build(tmp_path: Path):
    project_root = Path(__file__).parents[2]
    build_dir = tmp_path / "latex"

    subprocess.run(
        [
            "sphinx-build",
            "-b",
            "latex",
            str(project_root / "docs"),
            str(build_dir),
        ],
        check=True,
    )


@pytest.mark.slow
@pytest.mark.skipif(
    shutil.which("latexmk") is None or shutil.which("xelatex") is None,
    reason="TeX toolchain (latexmk/xelatex) not installed",
)
def test_package_docs_pdf_build(tmp_path: Path):
    project_root = Path(__file__).parents[2]
    build_dir = tmp_path / "pdf"

    subprocess.run(
        [
            "sphinx-build",
            "-M",
            "latexpdf",
            str(project_root / "docs"),
            str(build_dir),
        ],
        check=True,
    )

    pdfs = list((build_dir / "latex").glob("*.pdf"))
    assert pdfs, "expected a PDF in the latexpdf output"


def test_docs_pdf_target_runs_latexpdf():
    project_root = Path(__file__).parents[2]

    result = subprocess.run(
        ["make", "-n", "-C", "docs", "pdf"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "sphinx-build" in result.stdout
    assert "-M latexpdf" in result.stdout
