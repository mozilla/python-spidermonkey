import os
import subprocess

from pkg_resources import resource_filename


platform = os.uname()[0].lower()
if platform.startswith('linux'):
    PLATFORM = 'linux'
elif platform.startswith('darwin'):
    PLATFORM = 'os-x'
else:
    raise ImportError('Unsupported platform')


SPIDERMONKEY_LIB = os.path.abspath(
    resource_filename('spidermonkey', os.path.join('lib', PLATFORM)))

SPIDERMONKEY = os.path.join(SPIDERMONKEY_LIB, 'js')


# Make sure that the required libraries are available to Spidermonkey.
LIB_PATH = ':'.join((SPIDERMONKEY_LIB,
                     os.environ.get('LD_LIBRARY_PATH', ''))).strip(':')
os.environ['LD_LIBRARY_PATH'] = LIB_PATH


def spidermonkey(code=None, script_file=None, strict=False, warnings=None,
                 compile_only=False):

    cmd = [SPIDERMONKEY]

    if warnings is True:
        cmd.append('--warnings')
    elif warnings is False:
        cmd.append('--nowarnings')

    if strict:
        cmd.append('--strict')

    if compile_only:
        assert code is None, '`compile_only` may not be used with `code`'
        cmd.append('--compileonly')

    if code is not None:
        cmd.extend(('-e', code))
    if script_file is not None:
        cmd.extend(('-f', script_file))

    proc = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return proc
