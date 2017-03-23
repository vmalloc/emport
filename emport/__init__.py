import imp
import itertools
import os
import sys
import platform
import importlib

import logbook

_logger = logbook.Logger(__name__)
_HAS_NEW_IMPORTLIB = (sys.version_info > (3, 3))
_REQUIRES_MODULE_SPECS = (sys.version_info > (3, 6))

if _HAS_NEW_IMPORTLIB:
    from importlib.machinery import SourceFileLoader

if _REQUIRES_MODULE_SPECS:
    from importlib.machinery import ModuleSpec


class NoInitFileFound(Exception):
    pass


def import_file(filename):
    """Given a path to a file, imports it as a Python module
    """
    module_name = _setup_module_name_for_import(filename)

    if _HAS_NEW_IMPORTLIB:
        return _import_using_new_importlib(module_name, filename)
    return __import__(module_name, fromlist=[''])


def set_package_name(directory, name):
    """Given a directory, establishes that directory as a pseudo-package, enabling clearer future imports
    """
    directory = _normalize_path(directory)
    if directory not in _cached_package_names:
        _create_package_module(name, directory)
        _cached_package_names[directory] = name


def _import_using_new_importlib(module_name, filename):
    is_package = os.path.isdir(filename) or filename.endswith('__init__.py')
    if os.path.isdir(filename):
        filename = os.path.join(filename, "__init__.py")

    package_name = module_name if is_package else module_name.rsplit('.', 1)[0]
    if package_name != module_name and package_name not in sys.modules:
        # need to import the package first
        pkg = SourceFileLoader(package_name, os.path.join(
            os.path.dirname(filename), '__init__.py')).load_module()
        sys.modules[package_name] = pkg

    return __import__(module_name, fromlist=[''])

_package_name_generator = ('_{0}'.format(x) for x in itertools.count())


def _generate_package_name():
    for suggested in _package_name_generator:
        if not _package_name_exists(suggested):
            return suggested


def _package_name_exists(pkg_name):
    return pkg_name in sys.modules


def _setup_module_name_for_import(filename):
    return _create_new_module_name(filename)

_cached_package_names = {}


def _create_new_module_name(filename):
    _logger.trace("Creating new package for {0}", filename)
    nonpackage_dir, remainder = _split_nonpackage_dir(filename)
    _logger.trace("After split: {0}, {1}", nonpackage_dir, remainder)
    package_name = _cached_package_names.get(nonpackage_dir, None)
    if package_name is None:
        package_name = _generate_package_name()
        sys.modules[package_name] = _create_package_module(
            package_name, nonpackage_dir)
        _cached_package_names[nonpackage_dir] = package_name
    returned = '{0}.{1}'.format(package_name, remainder)
    if returned.endswith('.__init__'):
        returned = returned.rsplit('.', 1)[0]
    return returned


def _split_nonpackage_dir(path):
    if not os.path.isdir(path):
        nonpackage_dir, module = os.path.split(_normalize_path(path))
        module = _make_module_name(module).split(".")
    else:
        nonpackage_dir = path
        module = []
    while os.path.isfile(os.path.join(nonpackage_dir, "__init__.py")):
        if '.' in os.path.split(nonpackage_dir)[-1]:
            # we cannot import from such packages, stop traversing upwards...
            break
        nonpackage_dir, current_component = os.path.split(nonpackage_dir)
        module.insert(0, current_component)
        _logger.trace("Now at {0}, {1}", nonpackage_dir, module)
    if not module:
        raise NoInitFileFound(
            "Could not find __init__.py file in {0}".format(path))
    return nonpackage_dir, ".".join(module)


def _normalize_path(path):
    return os.path.normpath(os.path.abspath(str(path)))


def _make_module_name(filename):
    assert filename.endswith('.py') or filename.endswith('.pyc')
    return filename.rsplit(".", 1)[0].replace(os.path.sep, ".")


def _create_package_module(name, path):
    imp.acquire_lock()
    try:
        if _HAS_NEW_IMPORTLIB:
            # the package import machinery works a bit differently in
            # python 3.3
            returned = imp.new_module(name)
            returned.__path__ = [path]
            returned.__package__ = name

            if _REQUIRES_MODULE_SPECS:
                returned.__spec__ = ModuleSpec(
                    origin=path, name=name, loader=SourceFileLoader(name, path), is_package=True)
                returned.__spec__.submodule_search_locations.append(path)

            sys.modules[name] = returned
        else:
            returned = imp.load_module(
                name, None, path, ('', '', imp.PKG_DIRECTORY))
    finally:
        imp.release_lock()
    return returned
