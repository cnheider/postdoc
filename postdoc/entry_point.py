#!/usr/bin/env python3
import os

__all__ = ['main']

import subprocess

from pathlib import Path
from . import PROJECT_NAME
from .building import build_documentation


def main():
  '''
   This is the entrypoint called by Github when our action is run. All the Github specific setup is done
   here to make it easy to test the action code in isolation.

  :return:
  :rtype:
  '''
  print(f"[{PROJECT_NAME}] Starting build")

  docs_requirements = Path.cwd() / "requirements_docs.txt"

  if docs_requirements.exists():
    subprocess.check_call(["pip", "install", "-r", docs_requirements])

  return_code, annotations = build_documentation(os.environ.get("INPUT_OUTPUT_TYPE"),
                                                 os.environ.get("INPUT_DOCUMENTATION_PATH"))
  if return_code != 0:
    build_success = False
  else:
    build_success = True

  for annotation in annotations:
    print(annotation)

  status_message = (f"[{PROJECT_NAME}] Build {'succeeded' if build_success else 'failed'} with "
                   f"{len(annotations)} warnings")
  print(status_message)

  if not build_success:
    raise RuntimeError("Build failed")


if __name__ == "__main__":
  main()
