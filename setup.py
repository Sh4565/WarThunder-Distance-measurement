
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='WT_Distance_Measurement',
    author='GoodMan',
    version='0.1.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'WT_Distance_Measurement=main:main',
            'wtdm=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
