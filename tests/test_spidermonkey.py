import pytest

from spidermonkey import Spidermonkey


def test_command_line_code():
    """Test that command line code is executed."""

    proc = Spidermonkey(code='print("Hello")')
    stdout, stderr = proc.communicate()

    assert (stdout, stderr) == ('Hello\n', '')
    assert proc.returncode == 0


def test_script_file():
    """Test that a script file is executed as expected."""

    proc = Spidermonkey(script_file='-')
    stdout, stderr = proc.communicate('print("World")')

    assert (stdout, stderr) == ('World\n', '')
    assert proc.returncode == 0


def test_compileonly():
    """Test that compileonly returns a status but no output."""

    # Valid code: no output, returns 0.
    proc = Spidermonkey(compile_only=True, script_file='-')
    stdout, stderr = proc.communicate('print("Hello")')

    assert not stdout
    assert not stderr
    assert proc.returncode == 0

    # Invalid code: only stderr output, returns > 0.
    proc = Spidermonkey(compile_only=True, script_file='-')
    stdout, stderr = proc.communicate('print("Hello"')

    assert stdout == ''
    assert stderr != ''
    assert proc.returncode > 0

    # The compile-only flag is not applied to code passed on the
    # command line, so it should not be accepted.
    with pytest.raises(AssertionError):
        Spidermonkey(compile_only=True, code="print('Hello')")
