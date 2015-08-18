# ezvirtualenv
This is easy tool to run Python applications in virtual environments.

## Installation
Installation is as easy as:

    pip install git+https://github.com/matthiasmiller/ezvirtualenv.git

## Usage

Creating a virtual environment for your project is simple.

* Create a file called `requirements.txt` in your project root using the [pip requirement specifiers](https://pip.pypa.io/en/latest/reference/pip_install.html#requirement-specifiers).

* Run the following command from your project root to create your virtual environment:

        python -m ezvirtualenv

* Modify your main Python script to automatically launch the virtual environment:

        import ezvirtualenv
        if __name__ == '__main__':
            ezvirtualenv.run_as_virtual()

That's it! Whenever you run your main Python script, it will automatically run in your virtual environment.
