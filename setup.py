import econtools
from setuptools import setup

with open('README.md') as fp:
    readme = fp.read()

install_requires = [
    "boto3<2.0.0",
]

setup(name='econtools',
    version=econtools.__version__,
    description='Tools for using article data in Python.',
    long_description=readme,
    packages=['econtools'],
    license = 'MIT',
    install_requires=install_requires,
    url='https://github.com/elifesciences/econ-tools',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='tech-team@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        ]
    )

