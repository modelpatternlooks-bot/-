# Camel case splitter overview

This document explains the camelCase/PascalCase utilities introduced for the
previous bug fix. The helpers live in [`src/text_processing.py`](../src/text_processing.py)
and are covered by [`tests/test_text_processing.py`](../tests/test_text_processing.py).

## Problem statement

Historically our formatter relied on a simple camelCase splitter that broke
whenever identifiers ended with an acronym. The classic failure looked like this:

```python
# Old behaviour (before the regression fix)
split_camel_case("DataXML") == ["Data", "", "XML"]
```

The empty component in the middle came from the regex reporting the trailing
acronym separately while the surrounding control flow still attempted to split
on the now-empty suffix. The result cascaded into downstream utilities, most
notably the snake_case converter, which produced stray underscores.

## Implementation strategy

To address the issue we reworked the splitter around a single, well documented
regular expression. The pattern is compiled once at module import time:

```python
_CAMEL_CASE_RE = re.compile(r"...", re.VERBOSE)
```

The verbose mode allows the expression to document each of its branches:

* **Acronym followed by a capitalised word** – captures the `HTTP` part of
  `HTTPRequest`.
* **Capitalised words** – handles typical `PascalCase` segments such as
  `Request`.
* **Lowercase runs** – covers the leading token in `camelCase` names.
* **Digits** – allows identifiers such as `ISO8601Date` to preserve the `8601`
  chunk.
* **Trailing acronyms** – matches the `XML` part of `DataXML` without creating
  an empty component.

Each identifier is pre-normalised by replacing non-alphanumeric delimiters with
spaces. The code then iterates over every whitespace-separated chunk and feeds
it through the regular expression. Successful matches are appended to the
resulting list in the order reported by `findall`, ensuring a deterministic
split for downstream consumers.

Because the splitter now gracefully handles trailing acronyms, the `to_snake_case`
helper can build predictable snake case identifiers by lowercasing every
component and joining them with underscores.

## Test coverage

`tests/test_text_processing.py` exercises the helper with a mixture of tricky
inputs: plain camelCase, PascalCase with acronyms, identifiers that contain
underscores or hyphens, and numbers wedged between letters. The regression test
for `DataXML` ensures we never reintroduce the empty-component bug.

All tests can be run with `pytest` from the project root.
