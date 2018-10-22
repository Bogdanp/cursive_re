import pytest

from cursive_re import (
    alternative, any_of, anything, beginning_of_line, end_of_line, group, in_range, literal, maybe,
    none_of, one_or_more, repeated, text, zero_or_more
)


@pytest.mark.parametrize("expr,expected", [
    (beginning_of_line(), "^"),
    (end_of_line(), "$"),
    (anything(), "."),

    (literal("a"), "a"),
    (literal("["), "["),

    (text("a"), "a"),
    (text("["), "\\["),

    (any_of("abc"), "[abc]"),
    (any_of(text("abc")), "[abc]"),
    (any_of(text("ab[")), "[ab\\[]"),
    (any_of(text("a-z")), "[a\\-z]"),
    (any_of(in_range("a", "z")), "[a-z]"),

    (none_of("abc"), "[^abc]"),
    (none_of(text("abc")), "[^abc]"),
    (none_of(text("ab[")), "[^ab\\[]"),
    (none_of(literal("ab[")), "[^ab[]"),
    (none_of(text("a-z")), "[^a\\-z]"),
    (none_of(in_range("a", "z")), "[^a-z]"),

    (in_range("a", "z"), "a-z"),

    (zero_or_more(text("abc")), "(?:abc)*"),
    (zero_or_more(any_of("abc")), "[abc]*"),

    (one_or_more(text("abc")), "(?:abc)+"),
    (one_or_more(any_of("abc")), "[abc]+"),

    (maybe(text("a")), "(?:a)?"),
    (maybe(text("a") + text("b")), "(?:ab)?"),
    (maybe(none_of(in_range("a", "z"))), "[^a-z]?"),
    (maybe(text("a") + any_of(in_range("a", "z"))), "(?:a[a-z])?"),

    (repeated(text("a"), exactly=5), "(?:a){5}"),
    (repeated(text("a"), at_least=2), "(?:a){2,}"),
    (repeated(text("a"), at_most=2), "(?:a){0,2}"),
    (repeated(text("a"), at_least=1, at_most=2), "(?:a){1,2}"),
    (repeated(text("a"), at_least=1, at_most=2, greedy=False), "(?:a){1,2}?"),

    (alternative(text("a"), text("b")), "(?:a)|(?:b)"),
    (alternative(any_of("abc"), text("d")), "[abc]|(?:d)"),
    (alternative(text("a"), alternative(text("b"), text("c"))), "(?:a)|(?:b)|(?:c)"),
    (text("a") | text("b") | text("c"), "(?:a)|(?:b)|(?:c)"),
    (text("a") | (text("b") | text("c")), "(?:a)|(?:b)|(?:c)"),
    (literal("[]") | text("b"), "(?:[])|(?:b)"),

    (group(text("a")), "(a)"),
    (group(text("a"), name="foo"), "(?P<foo>a)"),
    (group(text("a"), capture=False), "(?:a)"),
])
def test_exprs(expr, expected):
    assert str(expr) == expected
