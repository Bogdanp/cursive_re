import cursive_re
from cursive_re import *

domain_name = one_or_more(any_of(in_range("a", "z") + in_range("0", "9") + text("-")))
domain = domain_name + zero_or_more(text(".") + domain_name)
path_segment = zero_or_more(none_of("/"))
path = zero_or_more(text("/") + path_segment)
url = (
    group(one_or_more(any_of(in_range("a", "z"))), name="scheme") + text("://") +
    group(domain, name="domain") +
    group(path, name="path")
)

def test_url_pattern():
    assert str(url) == "(?P<scheme>[a-z]+)://(?P<domain>[a-z0-9\-]+(?:\.[a-z0-9\-]+)*)(?P<path>(?:/[^/]*)*)"

    pattern = cursive_re.compile(url)
    assert pattern.match("://foo") is None
    assert pattern.match("https://google.com").groupdict() == \
        {"scheme": "https", "domain": "google.com", "path": ""}
    assert pattern.match("https://google.com/test/1/2/3").groupdict() == \
        {"scheme": "https", "domain": "google.com", "path": "/test/1/2/3"}
