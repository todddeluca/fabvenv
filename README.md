# fabvenv

A fabric utility for creating remote virtual environments, and installing and
updating packages.

The basic use case this covers is logging into a remote host, downloading
virtualenv.py, using it to create a virtual environment for a project,
including installing `pip`, and then installing packages, based on a
"requirements.txt" file.

## Installation

```
pip install fabvenv
```

## Usage

Here is how I define Fabric tasks to create a virtual environment, install
packages, add a directory to the `sys.path` of the python executable, etc.:

```
@task
def venv_create():
    require('configured')
    venv = fabvenv.Venv(config.venv, config.requirements)
    if not venv.exists():
        venv.create(config.system_python)


@task
def venv_install():
    require('configured')
    fabvenv.Venv(config.venv, config.requirements).install()


@task
def venv_upgrade():
    require('configured')
    fabvenv.Venv(config.venv, config.requirements).upgrade()


@task
def venv_freeze():
    require('configured')
    fabvenv.Venv(config.venv, config.requirements).freeze()


@task
def venv_remove():
    require('configured')
    venv = fabvenv.Venv(config.venv, config.requirements)
    if venv.exists():
        venv.remove()


@task
def venv_pth():
    '''
    Add the code directory to the virtualenv sys.path.
    '''
    require('configured')
    fabvenv.Venv(config.venv, config.requirements).venv_pth([config.code])
```

## Contribute

Pull requests and issues are welcomed.

## Testing

The file `tests/fabfile.py` is a basic test of using fabric and fabvenv to
create a virtual environment, install a package, upgrade a package, and remove
the virtual environment.

This tests uses an installed version of `fabric` and `fabvenv`.  To avoid
having the test conflict with any other installation of `fabvenv`, use a
virtual environment for testing.

Clone fabvenv:

    git clone git@github.com:todddeluca/fabvenv.git
    cd fabvenv

Install fabric and fabvenv into a virtual environment:

    virtualenv ~/tmp/venv
    ~/tmp/venv/bin/pip install fabric
    ~/tmp/venv/bin/pip install -e .

The test also assumes that you can do passwordless (keypair) ssh into localhost
as `$USER`.

Run the tests as follows:

    cd tests/
    ~/tmp/venv/bin/fab test_fabvenv


