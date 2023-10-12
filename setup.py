from setuptools import find_packages, setup


def readme():
    with open('README.md', 'r') as file:
        return file.read()


NAME = 'catpig'
VERSION = '0.3.0'

setup(
    name=NAME,
    version=VERSION,
    license='CC0',
    author='Alexey Avramov',
    author_email='hakavlad@gmail.com',
    description='A memory-hard password-hashing function',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/hakavlad/catpig',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='kdf', 'pbkdf', 'memory-hard',
    project_urls={
        'Homepage': 'https://github.com/hakavlad/catpig',
        'Bug Tracker': 'https://github.com/hakavlad/catpig/issues',
        'Documentation': 'https://github.com/hakavlad/catpig/blob/main/README.md'
    },
    python_requires='>=3.6'
)
