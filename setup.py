from cx_Freeze import setup, Executable

COMPANY_NAME = 'Lead Pipe Software'
PRODUCT_NAME = 'RabbitHole'

# This IS the documentation you're looking for...
# https://cx-freeze.readthedocs.org/en/latest/distutils.html

# Dependencies are automatically detected, but it might need
# fine tuning.

build_exe_options = dict(
    packages = ["os", "RabbitHole.message", "RabbitHole.rabbitmq"],
    excludes = [])

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
setup(name='LeadPipe.RabbitHole',
      version = '1.0.0',
      description = 'RabbitHole is a RabbitMQ message utility',
      options = {'build_exe': build_exe_options,
                 'bdist_msi': bdist_msi_options},
      executables = executables)
