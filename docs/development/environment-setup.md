# Environment Setup
Getting setup to develop for the CSX website backend is relatively simple. There are just a few
basic requirements.

* [Python 3.6+](#python)
* [An IDE/Editor to write code in](#the-editor)
* [Postgres](#postgres)
  * This can be locally hosted, or can be on Google Cloud SQL. We will include documentation for both.

## Python
The CSX website backend is a Django project, which means it is written almost exclusively in Python. So
in order to be able to contribute to the project you will need to make sure you have Python 3.6 or greater
installed.

### Installing Python
#### Windows
To install python on windows you will want to download the installer for any compatible version (anything >3.6)
from [the python website](https://python.org). (Or, if you are using Windows 10, you can install it from the Windows
store, just search for Python)

When you run the installer you should see a window like this:
![Python Installer Window Screenshot](../_static/development/environment/python_installer.png)

```eval_rst
.. note::
    Keep `Install launcher for all users (recommended)` selected. This will make managing your python versions much easier should you ever need to install other versions.
```

Just hit `Install Now` and keep any recommended
settings on subsequent screens.

Congratulations! Python is now installed on your machine!

To verify the installation, open up a command prompt window and run the command `py` or `py -3`.

#### Linux
There are many different linux distributions, and many of them handle packages differently. The most
popular distribution of linux is by far Ubuntu, so these we will focus on that. 

If you are running Ubuntu 18.xx or 19.xx, put your feet up, and relax! You already have a compatible version of
python installed. To verify this, open up a terminal window and run the `python3` command. 
If you are running 19.xx you should see `Python 3.7.x` and if you are running 18.xx you should see `Python 3.6.x` (Release versions may vary slightly depending on exact Ubuntu version)

If you are on any version before 18.04, you will need to check to make sure that the package `python3.7` is available for your
version of Ubuntu. To do this run the following command 
```
$ apt search ^python3.[0-9]$
```
 This command will search the package repositories and return all the python version packages that are available for you to install.
 If to install one of the available packages just run `apt-get install ` followed by the package name. You can then verify the installation 
 by running `python3.x` where `x` represents the compatible minor version that you installed.
 
 ```eval_rst
.. note::
    Ubuntu 17.10 may have a compatible version of python3 installed by default. 
```

#### macOS
_Chad please complete_

### Setting Up a Python Virtual Environment
```eval_rst
.. admonition:: What is a Virtual Environment?

    A virtual environment is an isolated working copy of python, which allows you to work on a specific project without affecting other projects that you might be working on.
```
Before we create a virtual environment, it is a good idea to create a folder in which to put our virtual 
environment folders. This can be anywhere you like, and called what ever you like. Just make sure you know
what it is called, and that it is in a convenient place for you to access. 

Now that we have a folder to hold out virtual environments, lets create one!
1. First, open a terminal window (or Command Prompt for those on Windows), and navigate to the folder 
that you made to hold your virtual environments.
2. Run the following command `python -m venv NAME` where `NAME` is the name of your virtual environment.
3. To check that the virtual environment was created, you can check to see if there is a folder that now matches
what you called the virtual environment you created.

```eval_rst
.. warning::
    * `python` is used to be generic, on windows you may have to use `py` or `py -3` in order to run python commands from the command line. Linux and mac users may need to use `python3`
    * In somecases `venv` does not work, you can instead try replacing it with `virtualenv`
    * Linux users may need to install `python3-venv` (or `python3.x-venv` if you had to install your python version after the fact)
```

### Using a Python Virtual Environment
To use a venv (virtual environment) you must first activate. When you activate a venv you are telling
your terminal to use it for anything python related, rather than your system-wide installation.

Like many things, activating your venv is slightly different on Windows than it is on Linux or macOS. Luckily, once
activated, all the commands are the same going forward.
* Windows: Navigate to `PATH\TO\VENV\Scripts\` and run `activate.bat`
* Linux/macOS: Run the command `source /path/to/venv/lib/activate`

You will know you that the venv is active when you see `(NAME)` (where `NAME` is the name fo your venv) at the beginning
of every prompt.

While the venv is active, you can run python using the `python` command, regardless of OS or python version.

To deactivate the venv, simply run the command `deactivate`.

## The Editor
The two most common editors you will likely come across for python are VSCode and PyCharm, though you can
use anything you want to write python code.

### VSCode
_Coming Soon_

### PyCharm
PyCharm is a Python IDE made by the same people that make the popular Java IDE IntelliJ. In fact, 
PyCharm runs on the same code base as IntelliJ, meaning if you are familiar with the layout and 
workings of IntelliJ, you will be right at home with PyCharm.

There are three versions of PyCharm available. Community, Pro, and Edu.

Both Community and Edu are free, however Pro is a paid product. 

```eval_rst
+------------------------------------------+-------------+-------+-------+
| Feature                                  | Community   | Edu   | Pro   |
+==========================================+=============+=======+=======+
| IntelliJ Based Editor                    | Y           | Y     | Y     |
+------------------------------------------+-------------+-------+-------+
| Built in Debugger and Test runner        | Y           | Y     | Y     |
+------------------------------------------+-------------+-------+-------+
| Intelligent Refactoring and Navigation   | Y           | Y     | Y     |
+------------------------------------------+-------------+-------+-------+
| Code Inspection                          | Y           | Y     | Y     |
+------------------------------------------+-------------+-------+-------+
| VCS (Git) Support                        | Y           | Y     | Y     |
+------------------------------------------+-------------+-------+-------+
| Scientific Tools                         | N           | N     | Y     |
+------------------------------------------+-------------+-------+-------+
| Web Dev (WebStorm Features Bundled)      | N           | N     | Y     |
+------------------------------------------+-------------+-------+-------+
| Python Web Frameworks                    | N           | N     | Y     |
+------------------------------------------+-------------+-------+-------+
| Python Performance Profiler              | N           | N     | Y     |
+------------------------------------------+-------------+-------+-------+
| Remote Development                       | N           | N     | Y     |
+------------------------------------------+-------------+-------+-------+
| Database & SQL Support                   | N           | N     | Y     |
+------------------------------------------+-------------+-------+-------+
```

Though PyCharm Pro is a paid product, you can apply for a Student license for free [here](https://www.jetbrains.com/student/).
If you plan to use PyCharm it is a good idea to get the free license to have access to the extra features that Pro provides, however
the community or Edu versions would work just fine.

#### Configuring your PyCharm Installation
_Coming Soon_


## Postgres
_Coming Soon_
