import itertools
import os
import sys
import uuid

import logbook

import pytest

_filename_generator = ("module{0}.py".format(i) for i in itertools.count())


@pytest.fixture(scope='session', autouse=True)
def configure_logging():
    logbook.StderrHandler().push_application()


@pytest.fixture(autouse=True)
def preserve_sys_modules(request):
    old_modules = sys.modules.copy()
    old_path = sys.path[:]

    @request.addfinalizer
    def cleanup():
        sys.modules.clear()
        sys.modules.update(old_modules)
        sys.path[:] = old_path


def create_module_file(directory, filename=None):
    directory = str(directory)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    id = repr(uuid.uuid1())
    if filename is None:
        filename = next(_filename_generator)
    full_filename = os.path.join(directory, filename)
    with open(full_filename, "w") as f:
        f.write("value = {0!r}".format(id))
    return full_filename, id


@pytest.fixture
def module_file_factory(request):
    return create_module_file
