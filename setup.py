from setuptools import setup, find_packages

with open("./requirements.txt") as f:
    required = f.readlines()


setup(
    name='pynest',
    version='1.0.0',
    description='PyNest',
    author='Marinelli, G.',
    author_email='marinelli.giovanna@gmail.com',
    packages=find_packages(),
    install_requires=required
)
