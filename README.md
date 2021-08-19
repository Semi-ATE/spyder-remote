# spyder-remote

[![GitHub](https://img.shields.io/github/license/Semi-ATE/spyder-remote?color=black)](https://github.com/Semi-ATE/spyder-remote/blob/main/LICENSE) 
![Conda](https://img.shields.io/conda/pn/conda-forge/starz?color=black)
![Supported Python versions](https://img.shields.io/badge/python-%3E%3D3.7-black)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/spyder-remote?color=blue&label=GitHub)](https://github.com/Semi-ATE/spyder-remote/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/spyder-remote/latest)](https://github.com/Semi-ATE/spyder-remote)
[![CI](https://github.com/Semi-ATE/spyder-remote/workflows/CI/badge.svg)](https://github.com/Semi-ATE/spyder-remote/actions?query=workflow%3ACI)
[![CD](https://github.com/Semi-ATE/spyder-remote/workflows/CD/badge.svg)](https://github.com/Semi-ATE/spyder-remote/actions?query=workflow%3ACD)
[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/spyder-remote)](https://github.com/Semi-ATE/spyder-remote/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/spyder-remote)](https://github.com/Semi-ATE/spyder-remote/pulls)

![Client package](https://img.shields.io/badge/Package-spyder--remote--client-black)
[![Client on PyPI](https://img.shields.io/pypi/v/spyder-remote-client?color=blue&label=PyPI)](https://pypi.org/project/spyder-remote-client/)
[![Client on Conda](https://img.shields.io/conda/vn/conda-forge/spyder-remote-client?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/spyder-remote-client)
[![client feedstock](https://img.shields.io/github/issues-pr/conda-forge/spyder-remote-client-feedstock?label=feedstock)](https://github.com/conda-forge/spyder-remote-client-feedstock)
![Client Downloads PyPI](https://img.shields.io/pypi/dm/spyder-remote-client?color=g&label=PyPI%20Downloads)
![Client Downloads Conda](https://img.shields.io/conda/dn/conda-forge/spyder-remote-client?color=g&label=conda-forge%20Downloads)

![Server package](https://img.shields.io/badge/Package-spyder--remote--server-black)
[![Server on PyPI](https://img.shields.io/pypi/v/spyder-remote-server?color=blue&label=PyPI)](https://pypi.org/project/spyder-remote-server/)
[![Server on Conda](https://img.shields.io/conda/vn/conda-forge/spyder-remote-server?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/spyder-remote-client)
[![server feedstock](https://img.shields.io/github/issues-pr/conda-forge/spyder-remote-server-feedstock?label=feedstock)](https://github.com/conda-forge/spyder-remote-server-feedstock)
![Server Downloads PyPI](https://img.shields.io/pypi/dm/spyder-remote-server?color=g&label=PyPI%20Downloads)
![Server Downloads Conda](https://img.shields.io/conda/dn/conda-forge/spyder-remote-server?color=g&label=conda-forge%20Downloads)


`spyder-remote` is a project to add the ability to spyder to recognize (over [zeroconf](https://github.com/jstasiak/python-zeroconf)) what machines are in the local network that can start a `spyder-kernel` to which `spyder` can then (automatically) connect.

Bundeled with this capability there is also the capability to manage conda environment on the remote host.

Eventhough `spyder-remote` is one project, it consists out of 2 parts (the `spyder-remote-server` and the `spyder-remote-client`) and thus also <ins>**2 packages**</ins> that are released together under the same version number.

## spyder-remote-client

### Installation

The `spyder-remote-client` is simply installed over `conda` like so:

```sh
(base) me@mybox:~$ conda activate spyder
(spyder) me@mybox:~$ conda install spyder-remote-client
```
Note that `spyder-remote-client` depends on `spyder` (>=5), it will pull in also `spyder` if not available!

### Description

This is a plugin to `spyder` (>=5), and it adds 2 entries in the `IPython Console` hamburger:

<p align="center">
  <img src="/docs/images/IPython_console_hamburger.jpg">
</p>

  - `spyder-remote console`

    Selecting this option will present us with a dialog like this:

    <p align="center">
      <img src="/docs/images/SpyderRemoteConnectionDialog.png">
    </p>

    In a first stage `Credentials` and `Conda` disabled, and only the `Remote Spyder Host` QComboBox is active, and filled with all 'machines' discovered on the zeroconf network. (Note: we display the pretty names that come from the zeroconf network, it is supposed to be 'talking' names ... in **UTF-8** !) Once a host is selected, the `Credentials` section will enable, proposing the local user name (in our usecase this is :thumbsup:), and by default the password comes from the keyring - placeholer text -) Once that is cleared (by default nothing needs to be done), one can select which `conda` environment for the user on the remote host will be used. This is a QComboBox because we know this info (from the remote host). The Requirements is the finishing touch, if your project (local) has a `requirements` directory in the project root, one can chose whech one (or none) of these to apply to the remote conda environment! :heart_eyes: The `feedback line` guides the user, but there is only very few use-cases for this one (for exemple when the user & password don't allow access to the remote host) Note that the remote host can have a `guest` account set up, in such case we need to be able to tell the user this ... maybe over the feedback line ?!?)

  - `spyder-remote management`

    Here the idea is that one can quickly create/configure a remote environment. Basically I am hoping to add this functionality to the above described Dialog (that is what the two `...` QToolButton's are doing there. In such a case we can get ride of this `spyder-remote management` entry as the funtionality is already in the `spyder-remote console` entry point. Note that if we do things over `requirements` we don't need an elaborate system for this (read: a library with all individual conda commands :stuck_out_tongue:)

This package is to be implemented in pure Python(iow: `noarch`), so bringing it to `Windows`, `macOS` **and** `Linux` will be straight forward.

## spyder-remote-server

### Installation

The `spyder-remote-server` is installed with `conda` like so:

```sh
(base) me@mybox:~$ conda install spyder-remote-server
(base) me@mybox:~$ sudo spyder-remote-server --install
```
Note that `spyder-remote-server` is to be installed in `base` (anything else should fail)

So the `spyder-remote-server` conda-package installs the `spyder-remote-server` (Python) script.
This script has the following arguments:
  - --install ➜ installs the daemon
  - --uninstall ➜ uninstalls the daemon
  - --guest [guest_account] ➜ only to be used with `--install`, and it will also add a guest account to the system (with the same password as the account) and add this info also to the `/etc/spyder-remote.conf` file.
  - --cores [#] ➜ only to be used with `install`, and it will set the maximum numbers of consoles this machine will provide. (see section on `spyder-remote.conf`)

### Description

To begin with we will only implement the spyder-remote-server for Linux. (In a later stage we can add macOS and Windows)

The spyder-remote-server script will install/uninstall the 'publisher' in the systemd of the Linux system. (`/ect/spyder-remote.conf`, `systemctl`),
the install script thus need to check if the user is 'root' **and** if the conda
