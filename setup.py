from distutils.core import setup

setup(
    name='Watchy',
    version='1.0.0',
    author='Jean-Frederic Mainville',
    author_email='jfmainville@outlook.com',
    packages=['selemium'],
    scripts=['watchy/tv/main.py'],
    url='https://github.com/jfmainville/watchy',
    description='This repository contains the code required to automatically download the TV Shows and Movies from a TMDB Watchlist',
    long_description=open('README.md').read()
)
