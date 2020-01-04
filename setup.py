from distutils.core import setup

setup(
    name='python-crud',
    version='0.0.1',
    author='Gustavo Hernandez',
    author_email='gushdezh@hotmail.com',
    url='https://github.com/GustavoHdezH/python-crud',
    license='MIT',
    description='Python script for show it data from sqlite',
    long_description=open('README.md').read(),
    packages=["crud-sqlite"],
)