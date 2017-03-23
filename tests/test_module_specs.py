import os
import sys

import emport
import pytest

@pytest.mark.skipif(sys.version_info < (3, 6), reason='requires Python 3.6')
def test_module_specs(tmpdir, recwarn):

    package_dir = tmpdir.join('package')

    subpackage_dir = package_dir.join('sub')

    for p in (package_dir, subpackage_dir):
        with p.join('__init__.py').open('w', ensure=True) as f:
            pass

    with subpackage_dir.join('utils.py').open('w') as f:
        pass

    filename = subpackage_dir.join('module.py')
    with filename.open('w', ensure=True) as f:
        f.write('from . import utils')

    mod = emport.import_file(str(filename))

    for m in (mod, mod.utils):

        metapackage_name, remainder = m.__spec__.name.split('.', 1)
        assert remainder == 'package.sub.{}'.format(m.__name__.split('.')[-1]) # pylint: disable=no-member
        assert mod.__spec__.parent == '{0}.package.sub'.format(metapackage_name)      # pylint: disable=no-member


    metapackage = sys.modules[metapackage_name]


    assert metapackage.__spec__ is not None
    assert metapackage.__spec__.origin == str(package_dir.dirname)
    assert metapackage.__spec__.name == metapackage_name
    # TODO: restore this
    #assert metapackage.__spec__.parent == metapackage_name
    assert metapackage.__spec__.submodule_search_locations is not None
    assert str(package_dir.dirname) in metapackage.__spec__.submodule_search_locations
    assert metapackage.__package__ == metapackage_name

    assert not recwarn.list
