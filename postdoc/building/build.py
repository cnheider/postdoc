import os
import subprocess
import tempfile
from enum import Enum

__all__ = ["build_documentation"]

from pathlib import Path

from sorcery import assigned_names

from .parse import parse_sphinx_warnings_log
from .. import PROJECT_NAME


class OutputType(Enum):
    (
        html,
        dirhtml,
        singlehtml,
        htmlhelp,
        qthelp,
        devhelp,
        epub,
        applehelp,
        latex,
        man,
        texinfo,
        text,
        gettext,
        doctest,
        linkcheck,
        xml,
        pseudoxml,
    ) = assigned_names()
    pdf = "latex"


def build_documentation(
    output_type: OutputType = OutputType.html, doc_path: Path = Path("docs")
) -> tuple:
    """ """
    if not isinstance(output_type, OutputType):
        output_type = OutputType(output_type)

    if doc_path is None or doc_path == "":
        doc_path = Path.cwd() / "docs"
    if not isinstance(doc_path, Path):
        doc_path = Path(doc_path)

    assert (
        doc_path.exists()
    ), f"{doc_path} does not exist in working directory {os.listdir(str(Path.cwd()))}"

    print(f"[{PROJECT_NAME}] Making {output_type} documentation")

    log_file = Path(tempfile.gettempdir()) / "sphinx-log"

    if log_file.exists():
        log_file.unlink()

    return_code = subprocess.call(
        ["make", f"{output_type.value}", "-e"],
        env=dict(
            os.environ, SPHINXOPTS=f'--keep-going --no-color -w "{str(log_file)}"'
        ),
        cwd=str(doc_path),
    )

    with open(str(log_file), "r") as f:
        annotations = parse_sphinx_warnings_log(f.readlines())

    return return_code, annotations
