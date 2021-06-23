#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='sections',
    version='0.0.0',
    license='MIT',
    description='Flexible tree data structures for organizing lists and dicts into sections.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges',
                   re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Trevor Edwin Pogue',
    author_email='trevorpogue@gmail.com',
    url='https://github.com/trevorpogue/sections',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://sections.readthedocs.io/',
        'Changelog': 'https://sections.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/trevorpogue/sections/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
        'tree', 'data', 'structure', 'organize', 'section', 'category',
        'attr', 'dict', 'list', 'node', 'vertex', 'graph'
    ],
    python_requires='>=3.6',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        # 'debug>=0.0.0',
        # 'utils>=0.0.0',
        'pluralizer>=0.0.0'
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
        # ':python_version>="3.6"': ['pluralizer'],
    },
)
