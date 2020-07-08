from setuptools import setup, find_packages

from wireviz_gui import __version__

with open('requirements.txt', 'r') as f:
    REQUIREMENTS = [s.strip() for s in f.readlines()]

with open('readme.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='wireviz-gui',
    version=__version__,
    description='A GUI for WireViz',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Jason R. Jones',
    python_requires='>=3.6.0',
    url='https://github.com/slightlynybbled/wireviz-gui',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
