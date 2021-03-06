from setuptools import setup, find_packages
import os

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

setup(name='fxapom',
      version='1.0',
      description="Mozilla Firefox Accounts Page Object Model",
      long_description=description,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Mozilla Web QA',
      author_email='mozwebqa@mozilla.org',
      url='https://github.com/AndreiH/fxapom',
      license='MPL 2.0',
      packages=['fxapom', 'fxapom.pages'],
      include_package_data=True)
