import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='spacestills',
    version='0.2.0',
    description='NASA TV still frame viewer',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/pamoroso/spacestills',
    author='Paolo Amoroso',
    author_email='info@paoloamoroso.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering'
    ],
    python_requires='>=3.6',
    packages=['spacestills'],
    install_requires=['pysimplegui', 'pillow', 'requests'],
    entry_points={
        'console_scripts': [
            'spacestills=spacestills.gui:main'
        ]
    }
)