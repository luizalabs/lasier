from setuptools import find_packages, setup


def read(fname):
    with open(fname) as f:
        return f.read()


description = 'A sync/async circuit breaker implementation'
try:
    long_description = read('README.md')
except IOError:
    long_description = description


download_url = 'https://github.com/luizalabs/lasier/tarball/master'

setup(
    name='lasier',
    version='0.0.0',
    install_requires=[],
    url='https://github.com/luizalabs/lasier',
    author='Luiza Labs',
    author_email='pypi@luizalabs.com',
    keywords='circuit breaker sync async',
    description=description,
    long_description=long_description,
    download_url=download_url,
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
