from setuptools import setup

version = '1.1.1'

setup(
    name='uwsgi-tools',
    version=version,
    author='Andrei Fokau',
    author_email='andrei@5monkeys.se',
    url='https://github.com/andreif/uwsgi-tools',
    download_url='https://github.com/andreif/uwsgi-tools/tarball/%s' % version,
    license='MIT',
    description='uwsgi tools: curl and reverse proxy',
    long_description='''
        Reverse proxy and curl for uWSGI server using `uwsgi` protocol
    ''',
    classifiers=[
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['uwsgi_tools'],
    entry_points={
        'console_scripts': [
            'uwsgi_proxy = uwsgi_tools.proxy:cli',
            'uwsgi_curl = uwsgi_tools.curl:cli',
        ]
    },
    install_requires=[],
    tests_require=[],
    test_suite='runtests.main'
)
