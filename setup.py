from setuptools import setup, find_packages

setup(
    name='auto_call',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    install_requires=['Flask', 'requests', 'peewee'],
    include_package_data=True
)
