#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 09/03/2020
           """

__all__ = ["AnnotationLevel", "Annotation", "parse_sphinx_warnings_log"]

import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class AnnotationLevel(Enum):
    WARNING = "warning"
    FAILURE = "error"


@dataclass
class Annotation:
    """
    __slots__ = ["file", 'message', 'start_line', 'end_line', 'annotation_level']
    """

    __slots__ = ["file", "message", "start_line", "end_line", "annotation_level"]

    file: str
    message: str
    start_line: int
    end_line: int
    annotation_level: AnnotationLevel

    def __repr__(self) -> str:
        return f"{self.annotation_level.value} - file={self.file} - line={self.start_line} - {self.message}"


def extract_line_information(line_information: str) -> Tuple:
    r"""Lines from sphinx log files look like this
    This method is responsible for parsing out the line number and file name from these lines.
    """
    file_and_line = line_information.split(":")
    # This is a dirty windows specific hack to deal with drive letters in the
    # start of the file-path, i.e D:\
    if len(file_and_line[0]) == 1:
        # If the first component is just one letter, we did an accidental split
        file_and_line[1] = file_and_line[0] + ":" + file_and_line[1]
        # Join the first component back up with the second and discard it.
        file_and_line = file_and_line[1:]

    if len(file_and_line) != 2 and len(file_and_line) != 3:
        return None, None
    # The case where we have no line number, in this case we return the line
    # number as 1 to mark the whole file.
    if len(file_and_line) == 2:
        line_num = 1
    else:
        try:
            line_num = int(file_and_line[1])
        except ValueError:
            return None, None

    file_name = os.path.relpath(file_and_line[0])
    return file_name, line_num


def parse_sphinx_warnings_log(logs: List) -> List[Annotation]:
    r"""Parses a sphinx file containing warnings and errors into a list of
    CheckAnnotation objects.
    """
    annotations = []

    for i, line in enumerate(logs):
        if "WARNING" not in line:
            continue

        warning_tokens = line.split("WARNING:")
        if len(warning_tokens) != 2:
            continue
        file_and_line, message = warning_tokens

        file_and_line = extract_line_information(file_and_line)
        if not file_and_line:
            continue

        file_name, line_number = file_and_line

        warning_message = message
        # If this isn't the last line and the next line isn't a warning,
        # treat it as part of this warning message.
        if (i != len(logs) - 1) and "WARNING" not in logs[i + 1]:
            warning_message += logs[i + 1]
        warning_message = warning_message.strip()

        annotations.append(
            Annotation(
                file=file_name,
                message=warning_message,
                start_line=line_number,
                end_line=line_number,
                annotation_level=AnnotationLevel.WARNING,
            )
        )

    return annotations
