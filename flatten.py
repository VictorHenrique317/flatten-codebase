from setuptools import setup, find_packages

setup(
    name='flatten-codebase',
    version='1.3',
    packages=find_packages(),
    description="Flatten Codebase simplifies codebase preparation for Language Models by converting it into a single Markdown file, making it easier for the developer to provide the codebase to the LM",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Victor Henrique Silva Ribeiro',
    author_email='victor.henrique5800@gmail.com',
    url='https://github.com/VictorHenrique317/flatten-codebase',
    entry_points={
        'console_scripts': [
            'flatten-codebase=flatten_codebase.main:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)