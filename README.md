# spyder-remote

`spyder-remote` is a system that enables the [spyder IDE (>=5)](https://github.com/spyder-ide/spyder) to connect to a remote machine and work on the remote machine.

This project hold **BOTH** the client- and server-side of the equation.

# Client-side

The client-side is a plug-in for spyder (>=5) that adds 2 entries to the console 'hamburger':
  - `connect to remote `
  
    blah blah blah
  
  - `administer remote ...`

# Server-side



Plugin for spyder (>=5) that adds remote capabilities to spyder.

## Preample

Up to now, in spyder, there is some 'buttox pains' when it comes to:
  1. **Detecting what 'machines' are available in your network**, this is prior to 'connecting' to them, and currently not available.
  2. **Connecting to remote spyder-kernels**, this is available, but it is very manual. (actually almost un-usable for head-less devices).
  3. **Environment(s)** ... If ther is any, they are not controllable from `Spyder`. (Or better yet : the application you are coding for!)

`spyder-remote` solves these issues transparantly both remote **and local** hosts!

## Description

`spyder-remote` holds:
- [Client-side](/spyder_remote/client/) : as a plugin for Spyder (V5 and above)
- [Server-side](/spyder_remote/server/) : daemon/service per OS (Linux, MacOS & Windows)

The `spyder-remote` server-side uses [zeroconf](https://github.com/jstasiak/python-zeroconf) to announce it's presence to the zeroconf network.

[Spyder](https://github.com/spyder-ide/spyder) (by means of the client-side plugin) can now easily 'discover' what machines are available (including the local machine)!

When the user identifies the desired target, Spyder contacts the `ssd` (more correctly `ssp`). We need however to suply a `username` and `password`.
It is clear that we don't send the password as clear text, we instead use TSL (standare Python [ssl](https://docs.python.org/3.8/library/ssl.html) library or [pyopenssl](https://www.pyopenssl.org/en/stable/)) to communicate with an `ssd`. TLS from his side needs 'certificates', so the `ssd installer` will create a [self-signed certificate](https://stackoverflow.com/questions/10175812/how-to-create-a-self-signed-certificate-with-openssl) when installing `ssd`.

If more security is desirable, the IT department needs to replace the self-signed certificates by certificates signed by a certified autority.

Spyder can now ask the connected `ssd` to spin up a `cpp` (<ins>**C**</ins>onda <ins>**P**</ins>roxy <ins>**P**</ins>rocess) as the `user` used to connect to `ssd` itself.
`ssd` will do so, and report back the connection info to the just spinned up `cpp`. Spyder connects to the `cpp` and can figure out the avialable environments (for `user`), and, if so desired and configured, administer the conda environment. In the minimal use-case, spyder uses `cpp` to obtain a list of available conda environments for `user`.

Having the available conda environments, Spyder can now ask the connected `ssd` to spin up a `skp` (<ins>**S**</ins>pyder <ins>**K**</ins>ernel <ins>**P**</ins>rocess) as a `user` in a specific `conda environment`. `ssd` will do so and report back the connection data (= the infamous .json file) so that `spyder` can sub-sequently connect auto-magically to the freshley spinned spyder-kernel.

# installation

The installer will ask what needs to be installed if one does `$conda install ssd`.

For the installation of the server side, one needs to supply the root/Administrator password at the command line.

If one does `$conda install -y ssd` it is presumed that both client- and server-side need installation, however as conda is started as non-root/administrator, the installation script thus **will** prompt to supply the root/administrator password even though the '-y' option was provided.

If one does `$sudo conda install -y ssd` or `#conda install -y ssd` (Linux/MacOS only), the installation is truely 'silent'. (Note that the <ins>client side</ins> will only be installed
in those environments that hold `spyder`)

The server side will install `ssd` in his own 'application environment' with the name `_ssd_` ofcourse accessable by root/Administrator.

[anaconda](https://www.anaconda.com/products/individual), [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [miniforge](https://github.com/conda-forge/miniforge) is thus best installed on systems as ['multi-user'](
https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/admin-multi-user-install.html).

We give `ssd` it's own 'application environment' so that:
1. Testing only needs to cover the [requirements](/requirements) set forward by `ssd` itself. 
2. `ssd` will **never** clutter any of the other environments!

In any case, the `ssd` is started in the following manner:

```sh
conda run -n _ssd_ python ssd
```

# Releases & Assets

The whole `ssd` project is in principle a 'noarch' (read: pure python) implementation, however different OS-es need different things to deal with the daemon thing. 

Each release of `ssd` will have 8 assets (given a release as Major.minor.patch-Build = 'M.m.p-B') :

- ssd-M.m.p-B-Linux
- ssd-M.m.p-B-Linux.sha256
- ssd-M.m.p-B-Win
- ssd-M.m.p-B-Win.sha256
- ssd-M.m.p-B-MacOS
- ssd-M.m.p-B-MacOS.sha256
- Source code (zip)
- Source code (tar.gz)
