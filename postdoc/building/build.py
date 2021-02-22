import os
import subprocess
import tempfile
from enum import Enum

__all__ = ["build_documentation"]

from pathlib import Path

from .parse import parse_sphinx_warnings_log
from .. import PROJECT_NAME


class OutputType(Enum):
    html = "html"
    dirhtml = "dirhtml"
    singlehtml = "singlehtml"
    htmlhelp = "htmlhelp"
    qthelp = "qthelp"
    devhelp = "devhelp"
    epub = "epub"
    applehelp = "applehelp"
    latex = "latex"
    pdf = "latex"
    man = "man"
    texinfo = "texinfo"
    text = "text"
    gettext = "gettext"
    doctest = "doctest"
    linkcheck = "linkcheck"
    xml = "xml"
    pseudoxml = "pseudoxml"


def build_documentation(
    output_type: OutputType = OutputType.html, doc_path: Path = Path("docs")
) -> tuple:
    """
    """
    if not isinstance(output_type, OutputType):
        output_type = OutputType(output_type)

    if doc_path is None or doc_path == "":
        doc_path = Path.cwd() / "docs"
    if not isinstance(doc_path, Path):
        doc_path = Path(doc_path)

    assert (
        doc_path.exists()
    ), f"{doc_path} does not exist in working directory {os.listdir(str(Path.cwd()))}"

    print(f"[{PROJECT_NAME}] Making {output_type.value} documentation")

    log_file = Path(tempfile.gettempdir()) / "sphinx-log"

    if log_file.exists():
        log_file.unlink()

    return_code = subprocess.call(
        ["make", f"{output_type.value}", "-e"],
        env=dict(os.environ, SPHINXOPTS=f'--keep-going --no-color -w "{log_file}"'),
        cwd=str(doc_path),
    )

    with open(log_file, "r") as f:
        annotations = parse_sphinx_warnings_log(f.readlines())

    return return_code, annotations
