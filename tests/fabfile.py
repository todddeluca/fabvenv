'''
A basic test of using fabric and fabvenv to create a virtual environment,
install a package, upgrade a package, and remove the virtual environment.

To run this test, you must have fabric installed, and you must be able to
do passwordless (keypair) ssh into localhost as $USER.

Run the tests as follows:

    cd tests/
    fab test_fabvenv

'''

import os
import shutil
import sys
import tempfile

# The location of fabvenv.py relative to this test file.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print sys.path

import fabvenv
from fabric.api import (env, execute, require, task)


TD = None
TEST_PACKAGES = ['nose==1.2.1']


@task
def local():
    env.hosts = ['localhost']
    env.configured = True


##############
# FABRIC TASKS

@task
def venv_create():
    require('configured')
    venv = fabvenv.Venv(venv_dir(), requirements_file())
    if not venv.exists():
        venv.create()


@task
def venv_install():
    require('configured')
    fabvenv.Venv(venv_dir(), requirements_file()).install()


@task
def venv_upgrade():
    require('configured')
    fabvenv.Venv(venv_dir(), requirements_file()).upgrade()


@task
def venv_freeze():
    require('configured')
    fabvenv.Venv(venv_dir(), requirements_file()).freeze()


@task
def venv_remove():
    require('configured')
    venv = fabvenv.Venv(venv_dir(), requirements_file())
    if venv.exists():
        venv.remove()


@task
def venv_pth():
    '''
    Add a code directory to the virtualenv sys.path.
    '''
    require('configured')
    fabvenv.Venv(venv_dir(), requirements_file()).venv_pth([os.path.abspath('.')])


####################
# TEST CONFIGURATION

def setup():
    '''
    Create the temporary directory used for testing.

    This is ran once before the first test (global setup).
    '''
    sys.stderr.write('module setup()\n')
    global TD
    TD = tempfile.mkdtemp()
    sys.stderr.write('test temp dir: {}\n'.format(TD))


def teardown():
    '''
    Removes the directory created in setup.

    This is run once after the last test.
    '''
    sys.stderr.write('module teardown()\n')
    if TD is not None:
        shutil.rmtree(TD)


def venv_dir():
    return os.path.join(TD, 'venv')


def requirements_file():
    return os.path.join(TD, 'requirements.txt')


def write_requirements(packages):
    '''
    Write a requirements.txt file for use with pip.

    :param pacakges: list.  A list of pip-compatible package strings.
    '''
    with open(requirements_file(), 'w') as fh:
        fh.write(''.join(p + '\n' for p in packages))


#######
# TESTS

@task
def test_fabvenv():

    try:
        setup()
        write_requirements(['nose==1.2.1'])
        execute(local)
        execute(venv_create)
        execute(venv_install)
        execute(venv_pth)
        write_requirements(['nose'])
        execute(venv_upgrade)
        execute(venv_remove)
    finally:
        teardown()
