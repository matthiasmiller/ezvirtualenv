#!/usr/bin/env python
# vim: sw=4 ts=4 et
import argparse
import os.path
import subprocess
import sys

def ensure_in_venv():
    script_path = os.path.abspath(sys.modules['__main__'].__file__)
    script_args = sys.argv[1:]

    venv = VirtualEnvironment(os.path.dirname(script_path))
    venv.ensure_in_venv(script_path, script_args)

def main():
    parser = argparse.ArgumentParser('ezvirtualenv')
    parser.add_argument('project_dir', nargs='?', default='.', help='root project directory')
    args = parser.parse_args()

    venv = VirtualEnvironment(os.path.abspath(args.project_dir))
    venv.create_if_missing()
    venv.install_requirements()

class VirtualEnvironment(object):

    _check_environ_name = '__EXPECT_VIRTUAL_ENV'

    def __init__(self, project_dir):
        self._project_dir = project_dir
        self._requirements_path = os.path.join(self._project_dir, 'requirements.txt')

        self._venv_dir = os.path.join(self._project_dir, '.venv')
        self._venv_python = os.path.join(self._venv_dir, 'Scripts', os.path.basename(sys.executable))
        self._venv_pip = os.path.join(self._venv_dir, 'Scripts', 'pip')
        self._in_virtual_env = os.path.normcase(self._venv_python) == os.path.normcase(sys.executable)

    def ensure_in_venv(self, script_path, script_args):
        # Resolve the script path.
        if not os.path.isdir(self._venv_dir):
            sys.stderr.write('You must create a virtual environment by running:\n' + \
                             '$ python -m ezvirtualenv\n')
            sys.exit(1)

        if not self._in_virtual_env:
            print 'Relaunching in virtual environment...'

            # Sanity-check to protect against infinite loops.
            env = os.environ.copy()
            assert not env.get(self._check_environ_name), 'Error detecting virtual environment!'
            env[self._check_environ_name] = 'yes'

            # Relaunch main script with same arguments.
            proc = subprocess.Popen([self._venv_python, script_path] + script_args, env=env)
            sys.exit(proc.wait())

    def create_if_missing(self):
        if not os.path.isfile(self._requirements_path):
            sys.stderr.write('The requirements.txt file must exist.')
            sys.exit(1)

        if not os.path.isdir(self._venv_dir):
            print 'Creating virtual environment...'

            # Only import outside of the actual virtual environment.
            import virtualenv
            virtualenv.create_environment(self._venv_dir)

            home_dir, lib_dir, inc_dir, bin_dir = virtualenv.path_locations(self._venv_dir)
            virtualenv.copyfile(os.path.abspath(__file__),
                                os.path.join(lib_dir, 'site-packages', os.path.basename(__file__)))

    def install_requirements(self):
        # Relaunch into the virtual environment to install requirements.
        self.ensure_in_venv(os.path.abspath(__file__), [self._project_dir])

        print 'Checking requirements...'
        subprocess.check_call([self._venv_pip, 'install', '-r', self._requirements_path])


if __name__ == '__main__':
    main()
