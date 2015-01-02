from setuptools import setup,find_packages

setup(
    name = "togu",
    version = "0.1",
    packages = find_packages(),
    author = "Nicolas Limage",
    description = "supervisord event handler to watch shinken",
    license = "GPL",
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
    ],
    entry_points = {
        'console_scripts': [
            'togu = togu.main:main',
        ],
    },
    test_suite = 'togu.test',
)
