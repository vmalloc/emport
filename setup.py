import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "emport", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIERS = [
    'Logbook>=0.11.0',
]
if sys.version_info < (2, 7):
    _INSTALL_REQUIERS.append("importlib")

setup(name="emport",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          ],
      description="Utility library for performing programmatic imports",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),
      url="https://github.com/vmalloc/emport",
      install_requires=_INSTALL_REQUIERS,
      scripts=[],
      namespace_packages=[]
      )
