import os
import subprocess

from pkg_resources import resource_filename


__all__ = 'Spidermonkey',

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


def maybe_iterable(val):
    if isinstance(val, basestring):
        return val,
    elif val is None:
        return ()
    return val


class Spidermonkey(subprocess.Popen):

    def __init__(self, code=None, early_script_file=None, script_file=None,
                 compile_only=False, strict=False, warnings=None,
                 script_args=(), extra_flags=(),
                 stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE, **kw):

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

        for script in maybe_iterable(code):
            cmd.extend(('-e', script))

        for script in maybe_iterable(early_script_file):
            cmd.extend(('-f', script))

        if extra_flags:
            cmd.extend(extra_flags)

        if script_file:
            cmd.append(script_file)
        elif script_args:
            # Arguments come after the script name, so if we have args without
            # an explicit script, we need a fake script.
            cmd.append('/dev/null')

        if script_args:
            cmd.extend(script_args)

        super(Spidermonkey, self).__init__(cmd, stdin=stdin, stdout=stdout,
                                           stderr=stderr, **kw)
