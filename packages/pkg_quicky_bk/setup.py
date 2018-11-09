from setuptools import setup
from quicky import versions
setup(
    name='quicky',
    version=versions.get_version(),
    packages=['quicky', 'quicky.db', 'quicky.JSON', 'quicky.backends', 'quicky.middleware', 'quicky.qvideo_stream'],
    url='',
    license='MIT',
    author='nttlong',
    author_email='zugeliang2000@gmail.com',
    description='Lib support for django'
)
