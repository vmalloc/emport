import pytest
import warnings
from uuid import uuid4
from emport import import_file


@pytest.mark.parametrize('add_init_py', [True, False])
def test_importing_doesnt_emit_warnings(tmpdir, recwarn, add_init_py):
    value = str(uuid4())
    warnings.simplefilter('always')

    directory = tmpdir.join('files')

    filename = directory.join('testfile.py')
    with directory.join('utils.py').open('w', ensure=True) as f:
        f.write('value = {0!r}'.format(value))

    with filename.open('w') as f:
        f.write('from .utils import value as new_value')

    if add_init_py:
        with directory.join('__init__.py').open('w') as f:
            pass

    module = import_file(str(filename))
    assert module.new_value == value
    assert len(recwarn.list) == 0
