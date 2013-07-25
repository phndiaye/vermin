# -*- coding: utf-8 -*-
"""
    vermin.utils
    ~~~~~~~~~~~~

    This module implements some miscellanious utilities
    used in Vermin. Most of them are used in the wrappers.
"""
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)
