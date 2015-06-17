import sys
from contextlib import contextmanager

from emport import import_file
import dessert

import pytest
from _pytest.assertion.rewrite import AssertionRewritingHook as PytestRewriteHook


@contextmanager
def _disable_pytest_rewriting():
    old_meta_path = sys.meta_path[:]
    try:
        for index, plugin in reversed(list(enumerate(sys.meta_path))):
            if isinstance(plugin, PytestRewriteHook):
                sys.meta_path.pop(index)
        yield
    finally:
        sys.meta_path[:] = old_meta_path



def test_dessert_interop(tmpdir):
    path = tmpdir.join('testme.py')
    with path.open('w') as f:
        f.write("""def f():
    a = 1
    b = 2
    assert a == b
""")

    with _disable_pytest_rewriting():
        with dessert.rewrite_assertions_context():
            mod = import_file(str(path))
    with pytest.raises(AssertionError) as caught:
        mod.f()

    assert '1 == 2' in str(caught.value)
