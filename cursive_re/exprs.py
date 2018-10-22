import re
from typing import List, Optional, Pattern, Union


def compile(expr: "expr", flags: int = 0) -> Pattern[str]:
    """Compile a cursive_re expression to a real regular expression.
    """
    return re.compile(str(expr), flags)


class expr:
    def __add__(self, other: "expr") -> "expr":
        return sequence([self]) + other

    def __or__(self, other: "expr") -> "expr":
        if isinstance(other, alternative):
            return alternative(self, *other.exprs)
        return alternative(self, other)

    def __str__(self) -> str:  # pragma: no cover
        raise NotImplementedError("subclasses must implement __str__()")


class beginning_of_line(expr):
    """Matches the beginning of a line.

    Examples:
      >>> str(beginning_of_line())
      ... "^"
    """

    def __str__(self) -> str:
        return "^"


class end_of_line:
    """Matches the end of a line.

    Examples:
      >>> str(end_of_line())
      ... "$"
    """

    def __str__(self) -> str:
        return "$"


class anything(expr):
    """Matches any character.

    Examples:
      >>> str(anything())
      ... "."
    """

    def __str__(self) -> str:
        return "."


class literal(expr):
    """Inserts a literal regular expression.

    Examples:
      >>> str(literal("\A\w"))
      ... "\A\w"
    """

    def __init__(self, literal: str) -> None:
        self.literal = literal

    def __str__(self) -> str:
        return self.literal


class text(expr):
    """Matches the given string exactly, escaping any special characters.

    Examples:
      >>> str(text("abc"))
      ... "abc"
    """

    def __init__(self, text: str) -> None:
        self.text = re.escape(text)

    def __str__(self) -> str:
        return self.text


class any_of(expr):
    """Matches any of the given characters.

    Examples:
      >>> str(any_of("ab"))
      ... "[ab]"

      >>> str(any_of(text("ab")))
      ... "[ab]"

      >>> str(any_of(text("[]")))
      ... "[\\[\\]]"
    """

    def __init__(self, e: Union[str, expr]) -> None:
        self.expr = text(e) if isinstance(e, str) else e

    def __str__(self) -> str:
        return f"[{self.expr}]"


class none_of(expr):
    """Matches none of the given characters.

    Examples:
      >>> str(none_of(text("ab")))
      ... "[^ab]"

      >>> str(none_of(text("[]")))
      ... "[^\\[\\]]"
    """

    def __init__(self, e: Union[str, expr]) -> None:
        self.expr = text(e) if isinstance(e, str) else e

    def __str__(self) -> str:
        return f"[^{self.expr}]"


class in_range(expr):
    """Matches a character in the given range.

    Examples:
      >>> str(in_range("a", "z"))
      ... "a-z"
    """

    def __init__(self, lo: str, hi: str) -> None:
        self.lo = lo
        self.hi = hi

    def __str__(self) -> str:
        return f"{self.lo}-{self.hi}"


class zero_or_more(expr):
    """Matches zero or more of the given expr.

    Examples:
      >>> str(zero_or_more(text("a")))
      ... "a*"

      >>> str(zero_or_more(group(text("abc"))))
      ... "(abc)*"
    """

    def __init__(self, e: expr) -> None:
        assert isinstance(e, expr), "zero_or_more must be passed an expr"
        self.expr = e if isinstance(e, GROUPLIKES) else group(e, capture=False)

    def __str__(self) -> str:
        return f"{self.expr}*"


class one_or_more(expr):
    """Matches one or more of the given expr.

    Examples:
      >>> str(one_or_more(text("a")))
      ... "a+"

      >>> str(one_or_more(group(text("abc"))))
      ... "(abc)+"
    """

    def __init__(self, e: expr) -> None:
        self.expr = e if isinstance(e, GROUPLIKES) else group(e, capture=False)

    def __str__(self) -> str:
        return f"{self.expr}+"


class maybe(expr):
    """Matches an expr if present.

    Example:
      >>> str(maybe(text("abc")))
      ... "(?:abc)?"
    """

    def __init__(self, e: expr) -> None:
        assert isinstance(e, expr), "maybe must be passed an expr"
        self.expr = e if isinstance(e, GROUPLIKES) else group(e, capture=False)

    def __str__(self) -> str:
        return f"{self.expr}?"


class repeated(expr):
    """Matches an expr repeated an exact number of times.

    Example:
      >>> str(repeated(text("a"), exactly=5))
      ... "(?:a){5}"

      >>> str(repeated(text("a"), at_least=1))
      ... "(?:a){1,}"

      >>> str(repeated(text("a"), at_most=5))
      ... "(?:a){0,5}"

      >>> str(repeated(text("a"), at_least=2, at_most=5, greedy=False))
      ... "(?:a){2,5}?"
    """

    def __init__(
            self, e: expr, *,
            exactly: Optional[int] = None,
            at_least: int = 0,
            at_most: Optional[int] = None,
            greedy: bool = True,
    ) -> None:
        assert isinstance(e, expr), "repeated must be passed an expr"
        self.expr = e if isinstance(e, GROUPLIKES) else group(e, capture=False)
        self.exactly = exactly
        self.at_least = at_least
        self.at_most = at_most
        self.greedy = greedy

    def __str__(self) -> str:
        if self.exactly is not None:
            return f"{self.expr}{{{self.exactly}}}"

        if self.at_most is not None:
            expr = f"{self.expr}{{{self.at_least},{self.at_most}}}"
        else:
            expr = f"{self.expr}{{{self.at_least},}}"

        if not self.greedy:
            return f"{expr}?"
        return expr


class alternative(expr):
    """Matches one of the given list of exprs.
    """

    def __init__(self, *exprs: expr) -> None:
        self.exprs = list(exprs)

    def __str__(self) -> str:
        return "|".join(str(expr) for expr in self.exprs)


class sequence(expr):
    """Groups the given set of exprs in order.
    """

    def __init__(self, exprs: List[expr]) -> None:
        self.exprs = exprs

    def __add__(self, other: expr) -> expr:
        if isinstance(other, sequence):
            return sequence(self.exprs + other.exprs)
        return sequence(self.exprs + [other])

    def __str__(self) -> str:
        return "".join(str(expr) for expr in self.exprs)


class group(expr):
    """Denotes a group whose contents can be retrieved after a match
    is performed.

    Examples:
      >>> str(group(text("a")))
      ... "(a)"

      >>> str(group(any_of("abc"), name="chars"))
      ... "(?P<chars>[abc])"
    """

    def __init__(self, e: expr, *, name: Optional[str] = None, capture: bool = True) -> None:
        assert isinstance(e, expr), "group must be passed an expr"
        self.expr = e
        self.name = name
        self.capture = capture

    def __str__(self) -> str:
        if not self.capture:
            return f"(?:{self.expr})"
        if self.name is not None:
            return f"(?P<{self.name}>{self.expr})"
        return f"({self.expr})"


GROUPLIKES = (group, any_of, none_of)
