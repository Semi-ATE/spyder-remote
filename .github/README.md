# spyder-remote

`spyder-remote` is a project to add the ability to spyder to recognize (over [zeroconf](https://github.com/jstasiak/python-zeroconf)) what machines are in the local network that can start a `spyder` `console`, and that `spyder` then can (automatically) connect to.

Bundeled with this capability there is also the capability to manage conda environment on the remote host.

Eventhough `spyder-remote` is one project, it consists out of 2 parts (the `spyder-remote-server` and the `spyder-remote-client`) and thus also <ins>**2 packages**</ins>!

## spyder-remote-client

This is a plugin to `spyder` (>=5), and it adds 2 entries in the ... hamburger:

  - `spyder-remote console`
  
  blah blah blah
  
  - `spyder-remote management`
  
  blah blah blah

## spyder-remote-server

