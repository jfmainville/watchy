from distutils.core import setup

setup(
    name='SeriesWatcher',
    version='1.0.0',
    author='Jean-Frederic Mainville',
    author_email='jfmainville@outlook.com',
    packages=['selemium'],
    scripts=['serieswatcher/download.py'],
    url='https://github.com/jfmainville/serieswatcher',
    description='This repository contains the code required to automatically download the desired TV shows from EZTV.',
    long_description=open('README.md').read()
)
