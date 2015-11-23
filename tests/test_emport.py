import os
import emport

import pytest


def test_import_from_non_package(tmpdir, module_file_factory):
    _import_and_verify(
        [module_file_factory(tmpdir, filename='{0}.py'.format(i)) for i in range(5)])


def test_multiple_imports_from_same_non_package(tmpdir, module_file_factory):
    file1 = module_file_factory(tmpdir)
    file2 = module_file_factory(tmpdir)
    [module1] = _import_and_verify([file1])
    [module2] = _import_and_verify([file2])
    assert _PACKAGE_NAME(module1) == _PACKAGE_NAME(module2)
    assert module1 is not module2


def test_importing_sub_package(tmpdir, module_file_factory):
    subpackage_dir = tmpdir.join('subpackage')
    subpackage_dir.join('__init__.py').ensure(file=True)
    full_filename, expected_value = module_file_factory(
        subpackage_dir, "module.py")
    module = emport.import_file(full_filename)
    assert module.__name__.endswith('.subpackage.module')


def test_importing_sub_package_and_subdir(tmpdir, module_file_factory):
    to_verify = module_file_factory(tmpdir)
    [module] = _import_and_verify([to_verify])
    package_name = _PACKAGE_NAME(module)

    subdir = tmpdir.join('sub')

    subdir.join('__init__.py').ensure(file=True)
    [sub_module] = _import_and_verify([module_file_factory(subdir)])
    assert (_PACKAGE_NAME(module) + '.sub') == _PACKAGE_NAME(sub_module)


def test_importing_different_directories_same_escaping(tmpdir, module_file_factory):
    dir1 = tmpdir.join("pkg+")
    dir2 = tmpdir.join("pkg-")
    filenames_and_expected_values = [module_file_factory(x) for x in [dir1, dir2]]
    module1, module2 = _import_and_verify(filenames_and_expected_values)
    assert _PACKAGE_NAME(module1) != _PACKAGE_NAME(module2)


def test_importing_dotted_name(tmpdir, module_file_factory):
    path_components = ["a", "b.c", "d"]
    path = tmpdir
    for c in path_components:
        path = path.join(c)
        path.join('__init__.py').ensure(file=True)
    filename, expected_value = module_file_factory(path, "module.py")
    _import_and_verify([(filename, expected_value)])


def test_importing_directory_no_init_file(tmpdir):
    with pytest.raises(emport.NoInitFileFound):
        emport.import_file(str(tmpdir))


@pytest.mark.parametrize('init_py_directly', [True, False])
def test_importing_directory(init_py_directly, tmpdir, module_file_factory):
    directory = str(tmpdir.join("pkg"))
    os.makedirs(directory)
    _, expected_value = module_file_factory(directory, "__init__.py")
    if init_py_directly:
        module = emport.import_file(os.path.join(directory, "__init__.py"))
    else:
        module = emport.import_file(directory)

    assert module.__name__.endswith(".pkg")
    assert module.value == expected_value


def test_importing_subdirectory_init_file(tmpdir, module_file_factory):
    directory = tmpdir.join('pkg')
    module_file_factory(directory, '__init__.py')
    subdir = directory.join('subpkg')
    filename, expected_value = module_file_factory(subdir, '__init__.py')
    module = emport.import_file(filename)
    assert module.value == expected_value


def _import_and_verify(filenames_and_expected_values):
    returned = []
    for filename, expected_value in filenames_and_expected_values:
        module = emport.import_file(filename)
        assert module.value == expected_value
        returned.append(module)
    return returned


def _PACKAGE_NAME(m):
    return m.__name__.rsplit(".", 1)[0]
