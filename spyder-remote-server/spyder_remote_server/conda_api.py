# Copyright (c) Semi-ATE
# Distributed under the terms of the MIT License
"""
Conda API.
"""

import os
import json
import subprocess
import sys

from spyder_remote_server.utils import get_conda_info


class CondaManager:

    def __init__(self):
        # Conda config values
        self.CONDA_PREFIX = None
        self.ROOT_PREFIX = None
        self._envs_dirs = None
        self._pkgs_dirs = None
        self._user_agent = None
        self._proxy_servers = None
        self._conda_version = None

        # Process
        self._process = None
        self._stdout = None
        self._stderr = None

        self.set_conda_prefix(info=get_conda_info())
        self.user_rc_path = os.path.abspath(os.path.expanduser('~/.condarc'))
        self.sys_rc_path = os.path.join(self.ROOT_PREFIX, '.condarc')

    def _call_conda(
        self,
        extra_args,
        abspath=True,
        parse=False,
        callback=None,
        environ=None
    ):
        """
        Call conda with the list of extra arguments, and return the worker.

        The result can be force by calling worker.communicate(), which returns
        the tuple (stdout, stderr).
        """
        if abspath:
            if sys.platform == 'win32':
                python = os.path.join(self.ROOT_PREFIX, 'python.exe')
                conda = os.path.join(self.ROOT_PREFIX, 'Scripts', 'conda-script.py')
            else:
                python = os.path.join(self.ROOT_PREFIX, 'bin/python')
                conda = os.path.join(self.ROOT_PREFIX, 'bin/conda')
            cmd_list = [python, conda]
        else:
            # Just use whatever conda is on the path
            cmd_list = ['conda']

        cmd_list.extend(extra_args)
        process = subprocess.Popen(cmd_list, env=environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process

    def _call_and_parse(
        self, extra_args, abspath=True, callback=None, environ=None
    ):
        process = self._call_conda(
            extra_args,
            abspath=abspath,
            parse=True,
            callback=callback,
            environ=environ,
        )
        stdout, stderr = process.communicate()
        try:
            data = json.loads(stdout)
        except Exception:
            data = None

        return data

    def _set_environment_variables(self, prefix=None, no_default_python=False):
        """Set the right CONDA_PREFIX environment variable."""
        environ_copy = os.environ.copy()
        conda_prefix = self.ROOT_PREFIX
        if prefix:
            conda_prefix = prefix

        if conda_prefix:
            if conda_prefix == self.ROOT_PREFIX:
                name = 'root'
            else:
                name = os.path.basename(conda_prefix)
            environ_copy['CONDA_PREFIX'] = conda_prefix
            environ_copy['CONDA_DEFAULT_ENV'] = name

        if no_default_python:
            environ_copy['CONDA_DEFAULT_PYTHON'] = None

        return environ_copy

    def set_conda_prefix(self, info=None):
        """
        Set the prefix of the conda environment.

        This function should only be called once (right after importing
        conda_api).
        """
        if info is None:
            # Find some conda instance, and then use info to get 'root_prefix'
            worker = self.info(abspath=False)
            info = worker.communicate()[0]
        else:
            self.ROOT_PREFIX = info['root_prefix']
            self.CONDA_PREFIX = info['conda_prefix']
            self._envs_dirs = info['envs_dirs']
            self._pkgs_dirs = info['pkgs_dirs']
            self._user_agent = info['user_agent']

            version = []
            for part in info['conda_version'].split('.'):
                try:
                    new_part = int(part)
                except ValueError:
                    new_part = part

                version.append(new_part)

            self._conda_version = tuple(version)

    def environment_exists(
        self, name=None, prefix=None, abspath=True, log=True
    ):
        """Check if an environment exists by 'name' or by 'prefix'.

        If query is by 'name' only the default conda environments directory is
        searched.
        """
        if name and prefix or (name is None and prefix is None):
            raise TypeError("Exactly one of 'name' or 'prefix' is required.")

        if name:
            prefix = self.get_prefix_envname(name)

        if prefix is None:
            prefix = self.ROOT_PREFIX

        return os.path.isdir(os.path.join(prefix, 'conda-meta'))

    def info(
        self,
        prefix=None,
        abspath=True,
        unsafe_channels=False,
        all_=False,
    ):
        """Return a dictionary with configuration information."""
        environ = self._set_environment_variables(prefix)
        cmd_list = ['info', '--json']

        if unsafe_channels:
            cmd_list.extend(['--unsafe-channels'])

        if all_:
            cmd_list.extend(['--all'])

        return self._call_and_parse(
            cmd_list,
            abspath=abspath,
            environ=environ,
        )

    def list_packages(
        self,
        prefix=None,
        abspath=True,
        unsafe_channels=False,
    ):
        """Return a dictionary with configuration information."""
        environ = self._set_environment_variables(prefix)
        cmd_list = ['list', '-p', prefix, '--json']
        return self._call_and_parse(
            cmd_list,
            abspath=abspath,
            environ=environ,
        )

    @property
    def envs_dirs(self):
        """
        Conda environment directories.

        The first writable item should be used.
        """
        if self._envs_dirs:
            envs_dirs = self._envs_dirs
        else:
            # Legacy behavior
            envs_path = os.sep.join([self.ROOT_PREFIX, 'envs'])
            user_envs_path = os.sep.join([get_home_dir(), '.conda', 'envs'])
            envs_dirs = [envs_path, user_envs_path]

        return envs_dirs

    def get_envs(self):
        """Return environment list of absolute path to their prefixes."""
        all_envs = []
        for env in self.envs_dirs:
            if os.path.isdir(env):
                envs_names = os.listdir(env)
                all_envs += [os.sep.join([env, i]) for i in envs_names]

        valid_envs = [
            env for env in all_envs
            if os.path.isdir(env) and self.environment_exists(prefix=env)
        ]

        return valid_envs


if __name__ == "__main__":
    cm = CondaManager()
    print(cm.get_envs())
