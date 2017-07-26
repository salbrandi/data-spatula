from setuptools import setup

setup(
    name='patella',
    version='0.0.1',
    py_modules=['htmlparser'],
    entry_points='''
        [console_scripts]
        patella=patella.click_commands:patella
        ''',

)
