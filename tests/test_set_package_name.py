from uuid import uuid4

import emport


def test_import_set_name(tmpdir):
    package_name = '__pkg_{0}__'.format(str(uuid4()).replace('-', '_'))
    emport.set_package_name(tmpdir, package_name)

    with tmpdir.join('file.py').open('w') as f:
        f.write('value = 666')

    mod = emport.import_file(f.name)
    assert mod.__name__ == '{0}.file'.format(package_name)
