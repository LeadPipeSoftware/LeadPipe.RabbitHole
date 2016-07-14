import os
import io
import re
from cx_Freeze import setup, Executable

COMPANY_NAME = 'Lead Pipe Software'
PRODUCT_NAME = 'RabbitHole'

# This IS the documentation you're looking for...
# https://cx-freeze.readthedocs.org/en/latest/distutils.html

# Dependencies are automatically detected, but it might need
# fine tuning.

# build_exe_options = dict(
#     packages = ["os", "RabbitHole.message", "RabbitHole.rabbitmq"],
#     excludes = [])

build_exe_options = dict(
    packages=["os"],
    excludes=[],
    include_files=['README.md', 'LICENSE', 'RabbitHole/RabbitHole.ini'])

bdist_msi_options = {
    'upgrade_code': '{9E074566-9492-433C-BA5D-391D016D78D6}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (COMPANY_NAME, PRODUCT_NAME),
}

base = 'Console'

executables = [
    Executable('RabbitHole/__main__.py',
               compress=True,
               base=base,
               targetName='RabbitHole.exe')
]


def read(*names, **kwargs):
    with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='RabbitHole',
      version=find_version("RabbitHole", "__init__.py"),
      description='RabbitHole is a RabbitMQ message utility',
      options={'build_exe': build_exe_options,
               'bdist_msi': bdist_msi_options},
      executables=executables)
