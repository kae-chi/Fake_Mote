from setuptools import setup

setup(
    name ='script',
    version='0.1.0' ,
    py_modules=['mirage', 'networking.py'],
    install_requires=[
        'Click', 'networking.py'
    ],
    entry_points={
        'console scripts' : [
                'mirage = mirage:mirage_entry' 
        ]

    
    }



)