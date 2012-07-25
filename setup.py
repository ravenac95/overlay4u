from setuptools import setup, find_packages

VERSION = '0.0.4'

LONG_DESCRIPTION = open('README.rst').read()

setup(name='overlay4u',
    version=VERSION,
    description='overlay4u',
    long_description=LONG_DESCRIPTION,
    keywords='overlayfs',
    author='Reuven V. Gonzales',
    author_email='reuven@tobetter.us',
    url='https://github.com/ravenac95/overlay4u',
    license='MIT',
    platforms='Ubuntu',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'subwrap',
    ],
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Build Tools',
    ],
)
