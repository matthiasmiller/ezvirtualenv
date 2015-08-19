#!/usr/bin/env python
# vim: sw=4 ts=4 et
import os.path
import subprocess
import sys

__version__ = '0.1.1'

MODULE_NAME = 'ezvirtualenv'

def virtualize():
    script_path = os.path.abspath(sys.modules['__main__'].__file__)
    script_args = sys.argv[1:]

    venv = _VirtualEnvironment(script_path, script_args)
    if not venv.in_virtual_env:
        venv.auto_create()
        venv.run_script()


class _VirtualEnvironment(object):
    """ This class is intentionally private.
        Breaking changes may appear in the future.
    """

    # Used for sanity-check to protect against infinite loops.
    _check_environ_name = '__EXPECT_VIRTUAL_ENV'

    def __init__(self, script_path, script_args):
        self._script_dir = os.path.dirname(script_path)
        self._script_path = script_path
        self._script_args = script_args
        self._requirements_path = os.path.join(self._script_dir, 'requirements.txt')

        self._venv_dir = os.path.join(self._script_dir, '.venv')
        self._venv_cache_path = os.path.join(self._venv_dir, '%s.cache' % MODULE_NAME)
        self._venv_python = os.path.join(self._venv_dir, 'Scripts', os.path.basename(sys.executable))
        self._venv_pip = os.path.join(self._venv_dir, 'Scripts', 'pip')
        self._in_virtual_env = os.path.normcase(self._venv_python) == os.path.normcase(sys.executable)

        # Make sure this is the *right* virtual environment!
        assert self._in_virtual_env == bool(os.environ.get(self._check_environ_name)), \
            'Error detecting virtual environment!'

    @property
    def in_virtual_env(self):
        return self._in_virtual_env

    def run_script(self):
        assert not self._in_virtual_env

        print 'Relaunching in virtual environment...'

        env = os.environ.copy()
        env[self._check_environ_name] = 'yes'

        # Relaunch main script with same arguments.
        proc = subprocess.Popen([self._venv_python, self._script_path] + self._script_args, env=env)
        sys.exit(proc.wait())

    def auto_create(self):
        assert not self._in_virtual_env

        # Only import outside of the virtual environment.
        import virtualenv

        if not os.path.isdir(self._venv_dir):
            print 'Creating virtual environment...'
            virtualenv.create_environment(self._venv_dir)

        # Skip if the requirements and ezvirtualenv files are unchanged.
        cache_key = self._get_cache_key()
        if os.path.isfile(self._venv_cache_path):
            with open(self._venv_cache_path) as f:
                if cache_key == f.read().strip():
                    return

        self._refresh_requirements()
        self._copy_ezvirtualenv()

        # Update the cache
        with open(self._venv_cache_path, 'w') as f:
            f.write(cache_key)
            
    def _get_cache_key(self):
        # Based on modified time + size.
        cache_key = ''
        for path in (self._requirements_path, os.path.abspath(__file__)):
            cache_key += ','
            if os.path.isfile(path):
                si = os.stat(path)
                cache_key += '%s-%s' % (si.st_mtime, si.st_size)
        return cache_key

    def _refresh_requirements(self):
        if os.path.isfile(self._requirements_path):
            # Note that we use the pip executable instead of the module to correctly detect dependencies.
            print 'Checking requirements...'
            subprocess.check_call([self._venv_pip, 'install', '-r', self._requirements_path])

    def _copy_ezvirtualenv(self):
        print 'Updating %s in virtual environment...' % MODULE_NAME
        import virtualenv
        home_dir, lib_dir, inc_dir, bin_dir = virtualenv.path_locations(self._venv_dir)
        target_path = os.path.join(lib_dir, 'site-packages', os.path.basename(__file__))
        virtualenv.copyfile(os.path.abspath(__file__), target_path)
