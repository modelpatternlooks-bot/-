import pytest

import text_processing as tp


@pytest.mark.parametrize(
    "token, expected",
    [
        ("", []),
        ("simple", ["simple"]),
        ("camelCase", ["camel", "Case"]),
        ("HTTPRequest", ["HTTP", "Request"]),
        ("DataXML", ["Data", "XML"]),
        ("userID", ["user", "ID"]),
        ("ISO8601Date", ["ISO", "8601", "Date"]),
        ("my_function_name", ["my", "function", "name"]),
        ("already_snake_case", ["already", "snake", "case"]),
        ("contains-dash", ["contains", "dash"]),
    ],
)
def test_split_camel_case(token, expected):
    assert tp.split_camel_case(token) == expected


def test_split_camel_case_trailing_acronym_does_not_introduce_empty_component():
    # Reproduces a regression where ``split_camel_case("DataXML")`` yielded
    # ``["Data", "", "XML"]``. The fix ensures the empty component is removed.
    assert tp.split_camel_case("DataXML") == ["Data", "XML"]


@pytest.mark.parametrize(
    "token, expected",
    [
        ("", ""),
        ("simple", "simple"),
        ("camelCase", "camel_case"),
        ("HTTPRequest", "http_request"),
        ("DataXML", "data_xml"),
        ("my_function_name", "my_function_name"),
    ],
)
def test_to_snake_case(token, expected):
    assert tp.to_snake_case(token) == expected
