import itertools
import os
import sys
import uuid

import pytest

_filename_generator = ("module{0}.py".format(i) for i in itertools.count())


@pytest.fixture(autouse=True)
def preserve_sys_modules(request):
    old_modules = sys.modules.copy()
    old_path = sys.path[:]

    @request.addfinalizer
    def cleanup():
        sys.modules = old_modules
        sys.path = old_path


@pytest.fixture
def modules(tmpdir):
    returned = []
    for i in range(5):
        d = str(tmpdir.join('dir_{0}'.format(i)))
        returned.append
        os.makedirs(d)
        returned.append(create_module(d))
    return returned


def create_module(directory, filename=None):
    id = repr(uuid.uuid1())
    if filename is None:
        filename = next(_filename_generator)
    full_filename = os.path.join(directory, filename)
    with open(full_filename, "w") as f:
        f.write("value = {0!r}".format(id))
    return full_filename, id
