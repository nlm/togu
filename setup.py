from setuptools import setup,find_packages

setup(
    name = "togu",
    version = "0.1.1",
    packages = find_packages(),
    author = "Nicolas Limage",
    description = "supervisord event listener to watch shinken daemons",
    url="https://github.com/nlm/togu",
    license = "MIT",
    keywords = "shinken watch supervisord",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Monitoring',
    ],
    install_requires = [
        'pycurl>=7',
        'supervisor>=2.999',
    ],
    entry_points = {
        'console_scripts': [
            'togu = togu.main:main',
        ],
    },
)
