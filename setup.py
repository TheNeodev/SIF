from setuptools import setup, find_packages

setup(
    name='sif',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'sif = sif.cli:main',
        ],
    },
    author='NeoDev',
    author_email='neoforevershog@gmail.com',
    description='SIF: Song Information Finder - Get BPM, key, and find mashup-compatible songs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/theneodev/sif',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
