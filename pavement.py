# -*- coding: utf-8 -*-

import os
import sys
import subprocess

# Import parameters from the setup file.
sys.path.append('.')

from setup import (
    setup_dict, _lint, _test, _test_all, DOCS_DIRECTORY,
    CODE_DIRECTORY, TESTS_DIRECTORY, PYTEST_FLAGS, print_success_message,
    print_failure_message
)

# from setup import (
#     get_project_files, print_success_message,
#     print_failure_message, _lint, _test, _test_all,
#     CODE_DIRECTORY, TESTS_DIRECTORY, PYTEST_FLAGS)

from paver.easy import options, task, needs
from paver.setuputils import install_distutils_tasks

options(setup=setup_dict)

install_distutils_tasks()

# Helper functions


class cwd(object):
    """Class used for temporarily changing directories. Can be though of
    as a 'pushd /my/dir' then a 'popd' at the end.
    """
    def __init__(self, newcwd):
        """
        Args:
            newcwd (str): directory to make the cwd
        """
        self.newcwd = newcwd

    def __enter__(self):
        self.oldcwd = os.getcwd()
        os.chdir(self.newcwd)
        return os.getcwd()

    def __exit__(self, type_, value, traceback):
        # This acts like a `finally' clause: it will always be executed.
        os.chdir(self.oldcwd)

# Tasks


def print_passed():
    # generated on http://patorjk.com/software/taag/#p=display&f=Small&t=PASSED
    print_success_message(r''' __        __   __   ___  __
|__)  /\  /__` /__` |__  |  \
|    /~~\ .__/ .__/ |___ |__/ ''')


def print_failed():
    # generated on http://patorjk.com/software/taag/#p=display&f=Small&t=FAILED
    print_failure_message(r''' ___              ___  __
|__   /\  | |    |__  |  \
|    /~~\ | |___ |___ |__/ ''')


@task
def test():
    """Run the unit tests."""
    raise SystemExit(_test())


@task
def test_all():
    """Perform a style check and run all unit tests."""
    retcode = _test_all()
    if retcode == 0:
        print_passed()
    else:
        print_failed()
    raise SystemExit(retcode)


@task
def lint():
    # This refuses to format properly when running `paver help' unless
    # this ugliness is used.
    ('Perform PEP8 style check, run PyFlakes, and run McCabe complexity '
     'metrics on the code.')
    raise SystemExit(_lint())


@task
def coverage():
    """Run tests and show test coverage report."""
    try:
        import pytest_cov  # NOQA
    except ImportError:
        print_failure_message(
            'Install the pytest coverage plugin to use this task, '
            "i.e., `pip install pytest-cov'.")
        raise SystemExit(1)
    import pytest
    pytest.main(PYTEST_FLAGS + [
        '--cov', CODE_DIRECTORY,
        '--cov-report', 'term-missing',
        TESTS_DIRECTORY])


def _doc_make(*make_args):
    """Run make in sphinx' docs directory.

    Returns:
        exit code
    """
    if sys.platform == 'win32':
        # Windows
        make_cmd = ['make.bat']
    else:
        # Linux, Mac OS X, and others
        make_cmd = ['make']
    make_cmd.extend(make_args)

    # Account for a stupid Python "bug" on Windows:
    # <http://bugs.python.org/issue15533>
    with cwd(DOCS_DIRECTORY):
        retcode = subprocess.call(make_cmd)
    return retcode


@task
@needs('doc_html')
def doc_open():
    """Build the HTML docs and open them in a web browser."""
    doc_index = os.path.join(DOCS_DIRECTORY, 'build', 'html', 'index.html')
    if sys.platform == 'darwin':
        # Mac OS X
        subprocess.check_call(['open', doc_index])
    elif sys.platform == 'win32':
        # Windows
        subprocess.check_call(['start', doc_index], shell=True)
    elif sys.platform == 'linux2':
        # All freedesktop-compatible desktops
        subprocess.check_call(['xdg-open', doc_index])
    else:
        print_failure_message(
            "Unsupported platform. Please open `{0}' manually.".format(
                doc_index))


@task
def doc_html():
    """Build the HTML docs."""
    retcode = _doc_make('html')

    if retcode:
        raise SystemExit(retcode)


@task
def doc_clean():
    """Clean (delete) the built docs."""
    retcode = _doc_make('clean')

    if retcode:
        raise SystemExit(retcode)