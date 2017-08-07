from setuptools import setup

setup(
    name='patella',
    packages=['patella'],
    version='0.1.0',
    author='Salvador Brandi',
    author_email='salbrandi@gmail.com',
    url='https://github.com/salbrandi/patella',
    download_url='https://github.com/salbrandi/patella/archive/0.1.tar.gz',
    py_modules=['htmlparser', 'hello'],
    entry_points='''
        [console_scripts]
        patella=click_commands:patella
        ''',

)
