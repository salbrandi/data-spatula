from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='patella',
    packages=['patella'],
    version='0.1.2',
    author='Salvador Brandi',
    author_email='salbrandi@gmail.com',
    url='https://github.com/salbrandi/patella',
    download_url='https://github.com/salbrandi/patella/archive/0.1.tar.gz',
    py_modules=['htmlparser'],
    description='A webservice for scraping files and plotting data against presidential party variation',
    long_description=long_description,
    entry_points='''
        [console_scripts]
        patella=click_commands:patella
        ''',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers/Data Analysts',
        'Topic :: Data Visualisation',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6.2',
    ],
    keywords='plotting data party presidential office term year bokeh'
)
