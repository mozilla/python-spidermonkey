import setuptools
from setuptools import setup


package_data = [
    'lib/linux/js', 'lib/linux/*.so', 'lib/os-x/js', 'lib/os-x/*.dylib'
]


class Distribution(setuptools.Distribution):
    def is_pure(self):
        # setuptools can't detect on its own that we're bundling binaries.
        return False


setup(
    name='spidermonkey',
    version='55.0a1.post2',
    author='Mozilla Corporation',
    author_email='addons-team@mozilla.com',
    description='A standalone executable Spidermonkey JavaScript shell, '
                'and a Python utility module to run it.',
    url='https://github.com/mozilla/python-spidermonkey/',
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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
