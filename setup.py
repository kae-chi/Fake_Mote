from setuptools import setup

setup(
    name ='mirage',
    version='0.1.0' ,
    py_modules=['mirage'],
    install_requires=[],
    entry_points={
        'console scripts' : [
                'mirage = mirage:mirage_entry' 
        ]

    
    }



)