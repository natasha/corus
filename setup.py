
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


setup(
    name='corus',
    version='0.8.0',
    description='Links to russian corpora, functions for loading and parsing',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/natasha/corus',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='corpora, russian, nlp, datasets',
    install_requires=[],
    packages=find_packages(),
)

