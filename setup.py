from setuptools import setup, find_packages

import contextext

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='contextext',
    version=contextext.__version__,
    description='A minimal API for modifying Windows context menu entries',
    long_description=readme,
    author='Luke Turner',
    author_email='github@luketurner.org',
    url='http://github.com/luketurner/contextext.py',
    packages=['contextext'],
    install_requires=[],
    license=contextext.__license__,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Topic :: Desktop Environment :: File Managers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4'
    )
)

