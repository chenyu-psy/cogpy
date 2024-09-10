from setuptools import setup, find_packages

setup(
    name='cogpy',
    version='0.1.2',
    description='This is a psychopy plugin for cognitive psychology experiments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chenyu Li',
    author_email='chenyu.li.hz@gmail.com',
    url='https://github.com/chenyu-psy/cogpy.git',
    packages=find_packages(),
    install_requires=[
        'psychopy',
        'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
