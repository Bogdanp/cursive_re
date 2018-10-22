# cursive_re

Readable regular expressions for Python 3.6 and up.

## Installation

    pip install cursive_re

## Examples

``` python
>>> from cursive_re import *

>>> hash = text("#")

>>> hexdigit = any_of(in_range("0", "9") + in_range("a-f") + in_range("A-F"))

>>> hexcolor = (
...   beginning_of_line() + hash +
...   group(repeated(hexdigit, exactly=6) | repeated(hexdigit, exactly=3)) +
...   end_of_line()
... )

>>> str(hexcolor)
'^\\#([a-f0-9]{6}|[a-f0-9]{3})$'

>>> hexcolor_re = compile(hexcolor)
re.compile('^\\#([a-f0-9]{6}|[a-f0-9]{3})$')

>>> hexcolor_re.match("#fff")
<re.Match object; span=(0, 4), match='#fff'>

>>> hexcolor_re.match("#ffff") is None
True

>>> hexcolor_re.match("#ffffff")
<re.Match object; span=(0, 7), match='#ffffff'>

>>> domain_name = one_or_more(any_of(in_range("a", "z") + in_range("0", "9") + text("-")))
>>> domain = domain_name + zero_or_more(text(".") + domain_name)
>>> path_segment = zero_or_more(none_of("/"))
>>> path = zero_or_more(text("/") + path_segment)
>>> url = (
...     group(one_or_more(any_of(in_range("a", "z"))), name="scheme") + text("://") +
...     group(domain, name="domain") +
...     group(path, name="path")
... )
>>> str(url)
"(?P<scheme>[a-z]+)://(?P<domain>[a-z0-9\-]+(?:\.[a-z0-9\-]+)*)(?P<path>(?:/[^/]*)*)"
```
