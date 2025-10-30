"""Utility helpers for text processing.

Currently contains camelCase splitting logic used by various formatting layers.
"""

from __future__ import annotations

import re
from typing import List

# Regular expression to split camelCase tokens. We use a verbose pattern so that we can
# express the different edge cases clearly. The pattern first consumes groups of
# uppercase letters that are followed by another uppercase letter and a lowercase
# character (handling words like "HTTPRequest" -> "HTTP"). It then consumes a single
# uppercase letter optionally followed by lowercase letters, or a run of lowercase
# letters or digits. Finally, it matches standalone digits. All matches are grouped so
# that findall returns each logical token.
_CAMEL_CASE_RE = re.compile(
    r"""
    (?:
        # Uppercase acronym followed by another capitalized word, e.g. HTTPRequest
        [A-Z]+(?=[A-Z][a-z])
        |
        # Uppercase letter followed by lowercase letters
        [A-Z][a-z]+
        |
        # A run of lowercase letters
        [a-z]+
        |
        # A run of digits
        \d+
        |
        # A trailing sequence of capitals (acronyms at the end)
        [A-Z]+
    )
    """,
    re.VERBOSE,
)


def split_camel_case(token: str) -> List[str]:
    """Split ``token`` into its camelCase/PascalCase components.

    The implementation is careful to preserve common acronyms: ``HTTPRequest`` will be
    returned as ``["HTTP", "Request"]`` instead of ``["HT", "TPRequest"]``.

    Parameters
    ----------
    token:
        The string to split. Non-alphanumeric characters are treated as delimiters.

    Returns
    -------
    list[str]
        A list containing the individual components.
    """

    if not token:
        return []

    # Replace common delimiters with spaces so we can split the string into chunks. This
    # allows callers to pass in names such as "my_function_name" and still get useful
    # tokens.
    normalized = re.sub(r"[^0-9A-Za-z]+", " ", token)

    parts: List[str] = []
    for chunk in normalized.split():
        matches = _CAMEL_CASE_RE.findall(chunk)
        if not matches:
            parts.append(chunk)
            continue

        # Previous implementations produced empty components when chunks ended with a
        # transition from lowercase to uppercase without an intervening lowercase
        # character (e.g. "DataXML"). ``findall`` would report the trailing "XML" as a
        # single match but we still added an empty string before it. The guard below
        # avoids that by only extending the list when ``matches`` is non-empty.
        parts.extend(filter(None, matches))

    return parts


def to_snake_case(token: str) -> str:
    """Convert a camelCase/PascalCase token to snake_case.

    This helper relies on :func:`split_camel_case` and is used extensively by the
    configuration loader. The correctness of :func:`split_camel_case` is therefore
    critical for producing predictable identifiers.
    """

    return "_".join(part.lower() for part in split_camel_case(token))
