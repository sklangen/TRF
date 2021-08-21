from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='trf',
    version='1.1.1',
    author='Schachklub Langen e. V.',
    author_email='Turnierleiter@sklangen.de',
    description='A parser and dumper for the fide approved tournament report format: trf',
    license='GPLv3+',
    keywords=['trf', 'fide', 'chess', 'tournaments'],
    packages=['trf'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sklangen/TRF',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)
