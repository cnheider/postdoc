#!/usr/bin/env python3
import os

__all__ = ["main"]

import subprocess

from pathlib import Path
from postdoc import PROJECT_NAME
from postdoc.building import build_documentation


def main():
  """
     This is the entrypoint called by Github when our action is run. All the Github specific setup is done
     here to make it easy to test the action code in isolation.

    :return:
    :rtype:
    """
  print(f"[{PROJECT_NAME}] Starting build")

  docs_requirements = Path.cwd() / 'requirements' / "requirements_docs.txt"

  if docs_requirements.exists():
    subprocess.check_call(["pip", "install", "-r", docs_requirements])

  return_code, annotations = build_documentation(
      os.environ.get("INPUT_OUTPUT_TYPE", "html"),
      os.environ.get("INPUT_DOCUMENTATION_PATH", ""),
      )

  if return_code != 0:
    raise RuntimeError("Build failed")
  else:
    for annotation in annotations:
      print(annotation)

    print(f"[{PROJECT_NAME}] Build succeeded with {len(annotations)} warnings")


if __name__ == "__main__":
  main()
