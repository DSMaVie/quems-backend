# quems-backend
This is the backend of the quems project. It implements a sqlite3 database and publishes via a flask/python api.

## setup
The server is hosted by a flask api so to execute you'll need a python environment.
Python environments are easily set up with anaconda. If you know what you're doing
you should use [Miniconda][https://docs.conda.io/en/latest/miniconda.html] to avoid clutter. If you're
new to python and python development use [the normal Anaconda installation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).
In any way navigate to the project folder with a shell and execute `conda create -n <environment-name> --file requirements.txt`.
Substitute `<environment-name>` with a suitable name for your environment, e.g. `quems`.

Of course, you can use any other python env manager. The build info is stored in `requirements.txt`.
## Starting Dev Server
if your env is setup you can start the dev server with `python api/api.py`