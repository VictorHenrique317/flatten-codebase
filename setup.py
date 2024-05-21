from setuptools import setup, find_packages

setup(
    name='codebase-flatter',
    version='1.1',
    packages=find_packages(),
    description='Codebase Flatter simplifies codebase preparation for Language Models by converting it into a single Markdown file, making it easier for the developer to provide the codebase to the LM',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Victor Henrique Silva Ribeiro',
    author_email='victor.henrique5800@gmail.com',
    url='https://github.com/VictorHenrique317/codebase-flatter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'flatten_codebase=flatten_codebase:main',
        ],
    },
)
