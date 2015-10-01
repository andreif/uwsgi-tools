from setuptools import setup

v = '1.0'

setup(
    name='uwsgi-tools',
    version=v,
    author='Andrei Fokau',
    author_email='andrei@5monkeys.se',
    url='https://github.com/andreif/uwsgi-tools',
    download_url='https://github.com/andreif/uwsgi-tools/tarball/%s' % v,
    license='MIT',
    description='uwsgi tools: curl and reverse proxy',
    long_description='''
        Reverse proxy and curl for uWSGI server using `uwsgi` protocol
    ''',
    packages=['uwsgi_tools'],
    entry_points={
        'console_scripts': [
            'uwsgi_proxy = uwsgi_tools.proxy:cli',
            'uwsgi_curl = uwsgi_tools.curl:cli',
        ]
    },
    install_requires=[],
)
