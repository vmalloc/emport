import os
import sys
import emport

import pytest


def test_import_from_non_package(modules):
    _import_and_verify(modules)


def test_multiple_imports_from_same_non_package(tmpdir):
    root = str(tmpdir)
    file1 = create_module(root)
    file2 = create_module(root)
    module1 = _import_and_verify(file1)
    module2 = _import_and_verify(file2)
    assert _PACKAGE_NAME(module1) == _PACKAGE_NAME(module2)
    assert module1 is not module2


def test_importing_sub_package():
    subpackage_dir = os.path.join(self.root, "subpackage")
    os.makedirs(subpackage_dir)
    _touch(subpackage_dir, "__init__.py")
    full_filename, expected_value = self._create_module(
        subpackage_dir, "module.py")
    module = emport.import_file(full_filename)
    self.assertTrue(module.__name__.endswith(".subpackage.module"))


def test_importing_sub_package_and_subdir():
    to_verify = self._create_modules([self.root])
    [module] = self._import_and_verify(to_verify)
    package_name = _PACKAGE_NAME(module)
    to_verify = self._create_modules([os.path.join(self.root, "sub")])
    _touch(self.root, "sub", "__init__.py")
    [sub_module] = self._import_and_verify(to_verify)
    self.assertEquals(_PACKAGE_NAME(module) + ".sub",
                      _PACKAGE_NAME(sub_module))


def test_importing_different_directories_same_escaping():
    dir1 = os.path.join(self.root, "pkg+")
    dir2 = os.path.join(self.root, "pkg-")
    filenames_and_expected_values = self._create_modules([dir1, dir2])
    module1, module2 = self._import_and_verify(filenames_and_expected_values)
    self.assertNotEquals(_PACKAGE_NAME(module1),
                         _PACKAGE_NAME(module2))


def test_importing_dotted_name():
    path_components = ["a", "b.c", "d"]
    path = self.root
    for c in path_components:
        path = os.path.join(path, c)
        os.makedirs(path)
        _touch(path, "__init__.py")
    filename, expected_value = self._create_module(path, "module.py")
    self._import_and_verify([(filename, expected_value)])


def test_importing_directory_no_init_file():
    with self.assertRaises(emport.NoInitFileFound):
        emport.import_file(self.root)


def test_importing_directory_directly():
    self._test_importing_directory(False)


def test_importing_directory_through_init_py():
    self._test_importing_directory(True)


def _test_importing_directory(self, init_py_directly):
    directory = os.path.join(self.root, "pkg")
    os.makedirs(directory)
    _, expected_value = self._create_module(directory, "__init__.py")
    if init_py_directly:
        module = emport.import_file(os.path.join(directory, "__init__.py"))
    else:
        module = emport.import_file(directory)
    self.assertRaises(module.__name__.endswith(".pkg"))
    self.assertEquals(module.value, expected_value)




def _import_and_verify(self, filenames_and_expected_values):
    returned = []
    for filename, expected_value in filenames_and_expected_values:
        module = emport.import_file(filename)
        self.assertEquals(module.value, expected_value)
        returned.append(module)
    return returned


def _touch(*p):
    with open(os.path.join(*p), "a"):
        pass


def _PACKAGE_NAME(m):
    return m.__name__.rsplit(".", 1)[0]
