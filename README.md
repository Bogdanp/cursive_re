# cursive_re

Readable regular expressions for Python 3.6 and up.

## Installation

    pip install cursive_re

## Examples

``` python
>>> from cursive_re import *

>>> hash = text('#')
>>> hexdigit = any_of(in_range('0', '9') + in_range('a', 'f') + in_range('A', 'F'))
>>> hexcolor = (
...     beginning_of_line() + hash +
...     group(repeated(hexdigit, exactly=6) | repeated(hexdigit, exactly=3)) +
...     end_of_line()
... )
>>> str(hexcolor)
'^\\#([a-f0-9]{6}|[a-f0-9]{3})$'

>>> hexcolor_re = compile(hexcolor)
re.compile('^\\#([a-f0-9]{6}|[a-f0-9]{3})$')

>>> hexcolor_re.match('#fff')
<re.Match object; span=(0, 4), match='#fff'>

>>> hexcolor_re.match('#ffff') is None
True

>>> hexcolor_re.match('#ffffff')
<re.Match object; span=(0, 7), match='#ffffff'>

>>> domain_name = one_or_more(any_of(in_range('a', 'z') + in_range('0', '9') + text('-')))
>>> domain = domain_name + zero_or_more(text('.') + domain_name)
>>> path_segment = zero_or_more(none_of('/'))
>>> path = zero_or_more(text('/') + path_segment)
>>> url = (
...     group(one_or_more(any_of(in_range('a', 'z'))), name='scheme') + text('://') +
...     group(domain, name='domain') +
...     group(path, name='path')
... )
>>> str(url)
'(?P<scheme>[a-z]+)://(?P<domain>[a-z0-9\-]+(?:\.[a-z0-9\-]+)*)(?P<path>(?:/[^/]*)*)'
```

## Reference

### `cursive_re.compile`

Compile a cursive_re expression to a real regular expression.


### `cursive_re.beginning_of_line`

Matches the beginning of a line.

Examples:

    >>> str(beginning_of_line())
    '^'


### `cursive_re.end_of_line`

Matches the end of a line.

Examples:

    >>> str(end_of_line())
    '$'


### `cursive_re.anything`

Matches any character.

Examples:

    >>> str(anything())
    '.'


### `cursive_re.literal`

Inserts a literal regular expression.

Examples:

    >>> str(literal(r"\A\w"))
    '\\A\\w'


### `cursive_re.text`

Matches the given string exactly, escaping any special characters.

Examples:

    >>> str(text("abc"))
    'abc'


### `cursive_re.any_of`

Matches any of the given characters.

Examples:

    >>> str(any_of("ab"))
    '[ab]'

    >>> str(any_of(text("ab")))
    '[ab]'

    >>> str(any_of(text("[]")))
    '[\\[\\]]'


### `cursive_re.none_of`

Matches none of the given characters.

Examples:

    >>> str(none_of("ab"))
    '[^ab]'

    >>> str(none_of(text("ab")))
    '[^ab]'

    >>> str(none_of(text("[]")))
    '[^\\[\\]]'


### `cursive_re.in_range`

Matches a character in the given range.

Examples:

    >>> str(in_range("a", "z"))
    'a-z'


### `cursive_re.zero_or_more`

Matches zero or more of the given expr.

Examples:

    >>> str(zero_or_more("a"))
    '(?:a)*'

    >>> str(zero_or_more(text("a")))
    '(?:a)*'

    >>> str(zero_or_more(text("abc")))
    '(?:abc)*'

    >>> str(zero_or_more(group(text("abc"))))
    '(abc)*'


### `cursive_re.one_or_more`

Matches one or more of the given expr.

Examples:

    >>> str(one_or_more("a"))
    '(?:a)+'

    >>> str(one_or_more(text("a")))
    '(?:a)+'

    >>> str(one_or_more(group(text("abc"))))
    '(abc)+'


### `cursive_re.maybe`

Matches an expr if present.

Examples:

    >>> str(maybe("abc"))
    '(?:abc)?'

    >>> str(maybe(text("abc")))
    '(?:abc)?'

    >>> str(maybe(group(text("abc"))))
    '(abc)?'

    >>> str(maybe(any_of("abc")))
    '[abc]?'


### `cursive_re.repeated`

Matches an expr repeated an exact number of times.

Examples:

    >>> str(repeated("a", exactly=5))
    '(?:a){5}'

    >>> str(repeated(text("a"), exactly=5))
    '(?:a){5}'

    >>> str(repeated(text("a"), at_least=1))
    '(?:a){1,}'

    >>> str(repeated(text("a"), at_most=5))
    '(?:a){0,5}'

    >>> str(repeated(text("a"), at_least=2, at_most=5, greedy=False))
    '(?:a){2,5}?'


### `cursive_re.group`

Denotes a group whose contents can be retrieved after a match
is performed.

Examples:

    >>> str(group(text("a")))
    '(a)'

    >>> str(group(any_of("abc"), name="chars"))
    '(?P<chars>[abc])'
