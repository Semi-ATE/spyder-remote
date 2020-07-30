# spyder-remote

`spyder-remote` is a project to add the ability to spyder to recognize (over [zeroconf](https://github.com/jstasiak/python-zeroconf)) what machines are in the local network that can start a `spyder` `console` to which `spyder` can then (automatically) connect.

Bundeled with this capability there is also the capability to manage conda environment on the remote host.

Eventhough `spyder-remote` is one project, it consists out of 2 parts (the `spyder-remote-server` and the `spyder-remote-client`) and thus also <ins>**2 packages**</ins>!

## spyder-remote-client

### Installation

The `spyder-remote-client` is simply installed over `conda` like so:

```sh
(base) me@mybox:~$ conda activate spyder
(spyder) me@mybox:~$ conda install spyder-remote-client
```
Note that `spyder-remote-client` depends on `spyder` (>=5), it will pull in also `spyder` if not available!

### Description

This is a plugin to `spyder` (>=5), and it adds 2 entries in the ... hamburger:

 ![New Ipython Console Hamburger](docs/pictures/IPython_console_hamburger.jpg)

  - `spyder-remote console`
  
  blah blah blah
  
  - `spyder-remote management`
  
  blah blah blah
  
This package must work for:
  - `Windows`
  - `macOS`
  - `Linux`
but there as it is implemented as pure Python (iow: the package is a `noarch` one) that should not be such a big issue.

## spyder-remote-server

