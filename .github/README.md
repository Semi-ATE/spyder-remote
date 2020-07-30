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

This is a plugin to `spyder` (>=5), and it adds 2 entries in the `IPython Console` hamburger:

<p align="center">
  <img src="/docs/pictures/IPython_console_hamburger.jpg">
</p>

  - `spyder-remote console`
  
    Selecting this option will present us with a dialog like this:
  
    <p align="center">
      <img src="/docs/pictures/SpyderRemoteConnectionDialog.png">
    </p>
    
    In a first stage `Credentials` and `Conda` disabled, and only the `Remote Spyder Host` QComboBox is active, and filled with all 'machines' discovered on the zeroconf network. (Note: we display the pretty names that come from the zeroconf network, it is supposed to be 'talking' names ... in **UTF-8** !) Once a host is selected, the `Credentials` section will enable, proposing the local user name (in our usecase this is :thumbsup:), and by default the password comes from the keyring - placeholer text -) Once that is cleared (by default nothing needs to be done), one can select which `conda` environment for the user on the remote host will be used. This is a QComboBox because we know this info (from the remote host). The Requirements is the finishing touch, if your project (local) has a `requirements` directory in the project root, one can chose whech one (or none) of these to apply to the remote conda environment! :heart_eyes: The `feedback line` guides the user, but there is only very few use-cases for this one (for exemple when the user & password don't allow access to the remote host) Note that the remote host can have a `guest` account set up, in such case we need to be able to tell the user this ... maybe over the feedback line ?!?)

  - `spyder-remote management`
  
    Here the idea is that one can quickly create/configure a remote environment. Basically I am hoping to add this functionality to the above described Dialog (that is what the two `...` QToolButton's are doing there. In such a case we can get ride of this `spyder-remote management` entry as the funtionality is already in the `spyder-remote console` entry point. Note that if we do things over `requirements` we don't need an elaborate system for this (read: a library with all individual conda commands :stuck_out_tongue:)
  
This package is to be implemented in pure Python(iow: `noarch`), so bringing it to `Windows`, `macOS` **and** `Linux` will be straight forward.

## spyder-remote-server


