# ezvirtualenv
This is an easy tool to run Python applications in virtual environments.

## Installation
Installation is as easy as:

    pip install git+https://github.com/matthiasmiller/ezvirtualenv.git

## Usage

To create a virtual environment for your project, simply modify your main
Python script to automatically launch the virtual environment:

    import ezvirtualenv
    if __name__ == '__main__':
        ezvirtualenv.virtualize()

That's it! Whenever you run your main Python script, it will automatically
run in your virtual environment. If your virtual environment is missing
or out of date, it will automatically create and update it for you.

## Custom Requirements

ezvirtualenv will automatically install packages that are defined in
a file called `requirements.txt` in your project root.

See the [pip requirement specifiers](https://pip.pypa.io/en/latest/reference/pip_install.html#requirement-specifiers)
for more details.
