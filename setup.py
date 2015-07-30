import setuptools
from distutils.util import get_platform
from setuptools import setup


if get_platform() == 'linux-x86_64':
    package_data = ['lib/linux/js', 'lib/linux/*.so']
else:
    package_data = ['lib/os-x/js', 'lib/os-x/*.dylib']


class Distribution(setuptools.Distribution):
    def is_pure(self):
        # setuptools can't detect on its own that we're bundling binaries.
        return False


setup(
    name='spidermonkey',
    version='41.0a2.post1',
    author='Mozilla Corporation',
    author_email='addons-team@mozilla.com',
    description='A standalone executable Spidermonkey JavaScript shell, '
                'and a Python utility module to run it.',
    url='https://github.com/kmaglione/python-spidermonkey/',
    license='MPLv2',
    install_requires=[
        'setuptools',
    ],
    packages=['spidermonkey'],
    package_data={
        'spidermonkey': package_data,
    },
    distclass=Distribution,
    platforms=['linux-x86_64', 'macos-10.10-intel'],
    options={
        'build': {
            'build_base': 'build/build.%s' % get_platform(),
        },
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
