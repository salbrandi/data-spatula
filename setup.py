from setuptools import setup

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
    entry_points='''
        [console_scripts]
        patella=click_commands:patella
        ''',

)
