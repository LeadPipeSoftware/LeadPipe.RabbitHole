from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

buildOptions = dict(
    packages = ["os", "RabbitHole.message", "RabbitHole.rabbitmq"],
    excludes = [])

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
      options = dict(build_exe = buildOptions),
      executables = executables)
