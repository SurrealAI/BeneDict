import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read().strip()


setup(
    name='BeneDict',
    version='0.3.1',
    author='Jim Fan',
    url='http://github.com/SurrealAI/BeneDict',
    description='',
    # long_description=read('README.rst'),
    keywords=['dict',
              'utility'],
    license='GPLv3',
    packages=['benedict'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyyaml',
    ],
    python_requires='>=3.5',
)
