import pytest
from emport import import_file


def test_relative_imports(directory):
    module = import_file(str(directory.join('proxy.py')))
    assert module.file_1_value == 'file_1'


@pytest.fixture
def directory(tmpdir):
    returned = tmpdir.join('dir')

    returned.join('__init__.py').ensure(file=True)


    with returned.join('file_1.py').open('w') as f:
        f.write('value = "file_1"')

    with returned.join('proxy.py').open('w') as f:
        f.write('from .file_1 import value as file_1_value')

    return returned
