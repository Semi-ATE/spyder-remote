1. On a fresh RPi4b add the user `conda`

<details>

```sh
nerohmot@RPi4b:~ $ sudo adduser conda
Adding user `conda' ...
Adding new group `conda' (1002) ...
Adding new user `conda' (1002) with group `conda' ...
Creating home directory `/home/conda' ...
Copying files from `/etc/skel' ...
New password: 
Retype new password: 
passwd: password updated successfully
Changing the user information for conda
Enter the new value, or press ENTER for the default
	Full Name []: conda
	Room Number []: 
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] y
nerohmot@RPi4b:~ $
```

</details>

TODO: maybe change to a `system` user, but then we need to do some extra steps (/etc/skel, ...)

2. Switch to the new `conda` user

```sh
nerohmot@RPi4b:~$ su - conda
Password: 
conda@RPi4b:~$
```

3. Download the appropriate `miniforge`

```sh
conda@RPi4b:~$ curl -SL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-4.8.3-4-Linux-aarch64.sh --output Miniforge3-4.8.3-4-Linux-aarch64.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   168  100   168    0     0    636      0 --:--:-- --:--:-- --:--:--   638
100   648  100   648    0     0   1163      0 --:--:-- --:--:-- --:--:--  1163
100 51.0M  100 51.0M    0     0  3138k      0  0:00:16  0:00:16 --:--:-- 5746k
conda@RPi4b:~$
```

4. Download the accompanying sha256 checksum

```sh
conda@RPi4b:~$ curl -SL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-4.8.3-4-Linux-aarch64.sh.sha256 --output Miniforge3-4.8.3-4-Linux-aarch64.sh.sha256
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   175  100   175    0     0    629      0 --:--:-- --:--:-- --:--:--   627
100   655  100   655    0     0   1233      0 --:--:-- --:--:-- --:--:--  1233
100   104  100   104    0     0     96      0  0:00:01  0:00:01 --:--:--    96
conda@RPi4b:~$ 
```

5. Check the checksum

```sh
conda@RPi4b:~$ sha256sum -c Miniforge3-4.8.3-4-Linux-aarch64.sh.sha256 2>&1 | grep OK
./Miniforge3-4.8.3-4-Linux-aarch64.sh: OK
conda@RPi4b:~$ 
```

6. Make the installer executable

<details>

```sh
conda@RPi4b:~$ chmod +x Miniforge3-4.8.3-4-Linux-aarch64.sh
conda@RPi4b:~$ ls -la
total 52320
drwxr-xr-x 2 conda conda     4096 Jul 27 22:56 .
drwxr-xr-x 5 root  root      4096 Jul 27 22:50 ..
-rw-r--r-- 1 conda conda      220 Jul 27 22:50 .bash_logout
-rw-r--r-- 1 conda conda     3771 Jul 27 22:50 .bashrc
-rw-r--r-- 1 conda conda      807 Jul 27 22:50 .profile
-rwxrwxr-x 1 conda conda 53550342 Jul 27 22:55 Miniforge3-4.8.3-4-Linux-aarch64.sh
-rw-rw-r-- 1 conda conda      104 Jul 27 22:56 Miniforge3-4.8.3-4-Linux-aarch64.sh.sha256
conda@RPi4b:~$ 
```

</details>

7. Run the installer script **with the appropriate prefix!**

<details>

```sh
conda@RPi4b:~$ ./Miniforge3-4.8.3-4-Linux-aarch64.sh -p /home/conda/forge

Welcome to Miniforge3 4.8.3-4

In order to continue the installation process, please review the license
agreement.
Please, press ENTER to continue
>>> 
BSD 3-clause license
Copyright (c) 2019, conda-forge
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Do you accept the license terms? [yes|no]
[no] >>> yes

Miniforge3 will now be installed into this location:
/home/conda/forge

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

[/home/conda/forge] >>> 
PREFIX=/home/conda/forge
Unpacking payload ...
Collecting package metadata (current_repodata.json): done                                                                                                                                                                                                     
Solving environment: done

## Package Plan ##

  environment location: /home/conda/forge

  added / updated specs:
    - _openmp_mutex==4.5=0_gnu
    - brotlipy==0.7.0=py37h8f50634_1000
    - bzip2==1.0.8=h516909a_2
    - ca-certificates==2020.4.5.1=hecc5488_0
    - certifi==2020.4.5.1=py37hc8dfbb8_0
    - cffi==1.13.2=py37h8022711_0
    - chardet==3.0.4=py37hc8dfbb8_1006
    - conda-package-handling==1.6.0=py37h8f50634_2
    - conda==4.8.3=py37hc8dfbb8_1
    - cryptography==2.9.2=py37hb09aad4_0
    - idna==2.9=py_1
    - ld_impl_linux-aarch64==2.34=h326052a_4
    - libffi==3.2.1=h4c5d2ac_1007
    - libgcc-ng==7.5.0=h8e86211_6
    - libgomp==7.5.0=h8e86211_6
    - libstdcxx-ng==7.5.0=hca8aa85_6
    - ncurses==6.1=hf484d3e_1002
    - openssl==1.1.1g=h516909a_0
    - pip==20.1.1=py_1
    - pycosat==0.6.3=py37h8f50634_1004
    - pycparser==2.20=py_0
    - pyopenssl==19.1.0=py_1
    - pysocks==1.7.1=py37hc8dfbb8_1
    - python==3.7.6=h89ca082_5_cpython
    - python_abi==3.7=1_cp37m
    - readline==8.0=h75b48e3_0
    - requests==2.23.0=pyh8c360ce_2
    - ruamel_yaml==0.15.80=py37h8f50634_1001
    - setuptools==46.4.0=py37hc8dfbb8_0
    - six==1.15.0=pyh9f0ad1d_0
    - sqlite==3.30.1=h283c62a_0
    - tk==8.6.10=hed695b0_0
    - tqdm==4.46.0=pyh9f0ad1d_0
    - urllib3==1.25.9=py_0
    - wheel==0.34.2=py_1
    - xz==5.2.5=h6dd45c4_0
    - yaml==0.2.4=h516909a_0
    - zlib==1.2.11=h516909a_1006


The following NEW packages will be INSTALLED:

  _openmp_mutex      conda-forge/linux-aarch64::_openmp_mutex-4.5-0_gnu
  brotlipy           conda-forge/linux-aarch64::brotlipy-0.7.0-py37h8f50634_1000
  bzip2              conda-forge/linux-aarch64::bzip2-1.0.8-h516909a_2
  ca-certificates    conda-forge/linux-aarch64::ca-certificates-2020.4.5.1-hecc5488_0
  certifi            conda-forge/linux-aarch64::certifi-2020.4.5.1-py37hc8dfbb8_0
  cffi               conda-forge/linux-aarch64::cffi-1.13.2-py37h8022711_0
  chardet            conda-forge/linux-aarch64::chardet-3.0.4-py37hc8dfbb8_1006
  conda              conda-forge/linux-aarch64::conda-4.8.3-py37hc8dfbb8_1
  conda-package-han~ conda-forge/linux-aarch64::conda-package-handling-1.6.0-py37h8f50634_2
  cryptography       conda-forge/linux-aarch64::cryptography-2.9.2-py37hb09aad4_0
  idna               conda-forge/noarch::idna-2.9-py_1
  ld_impl_linux-aar~ conda-forge/linux-aarch64::ld_impl_linux-aarch64-2.34-h326052a_4
  libffi             conda-forge/linux-aarch64::libffi-3.2.1-h4c5d2ac_1007
  libgcc-ng          conda-forge/linux-aarch64::libgcc-ng-7.5.0-h8e86211_6
  libgomp            conda-forge/linux-aarch64::libgomp-7.5.0-h8e86211_6
  libstdcxx-ng       conda-forge/linux-aarch64::libstdcxx-ng-7.5.0-hca8aa85_6
  ncurses            conda-forge/linux-aarch64::ncurses-6.1-hf484d3e_1002
  openssl            conda-forge/linux-aarch64::openssl-1.1.1g-h516909a_0
  pip                conda-forge/noarch::pip-20.1.1-py_1
  pycosat            conda-forge/linux-aarch64::pycosat-0.6.3-py37h8f50634_1004
  pycparser          conda-forge/noarch::pycparser-2.20-py_0
  pyopenssl          conda-forge/noarch::pyopenssl-19.1.0-py_1
  pysocks            conda-forge/linux-aarch64::pysocks-1.7.1-py37hc8dfbb8_1
  python             conda-forge/linux-aarch64::python-3.7.6-h89ca082_5_cpython
  python_abi         conda-forge/linux-aarch64::python_abi-3.7-1_cp37m
  readline           conda-forge/linux-aarch64::readline-8.0-h75b48e3_0
  requests           conda-forge/noarch::requests-2.23.0-pyh8c360ce_2
  ruamel_yaml        conda-forge/linux-aarch64::ruamel_yaml-0.15.80-py37h8f50634_1001
  setuptools         conda-forge/linux-aarch64::setuptools-46.4.0-py37hc8dfbb8_0
  six                conda-forge/noarch::six-1.15.0-pyh9f0ad1d_0
  sqlite             conda-forge/linux-aarch64::sqlite-3.30.1-h283c62a_0
  tk                 conda-forge/linux-aarch64::tk-8.6.10-hed695b0_0
  tqdm               conda-forge/noarch::tqdm-4.46.0-pyh9f0ad1d_0
  urllib3            conda-forge/noarch::urllib3-1.25.9-py_0
  wheel              conda-forge/noarch::wheel-0.34.2-py_1
  xz                 conda-forge/linux-aarch64::xz-5.2.5-h6dd45c4_0
  yaml               conda-forge/linux-aarch64::yaml-0.2.4-h516909a_0
  zlib               conda-forge/linux-aarch64::zlib-1.2.11-h516909a_1006


Preparing transaction: done
Executing transaction: done
installation finished.
Do you wish the installer to initialize Miniforge3
by running conda init? [yes|no]
[no] >>> yes
./Miniforge3-4.8.3-4-Linux-aarch64.sh: 404: [[: not found
no change     /home/conda/forge/condabin/conda
no change     /home/conda/forge/bin/conda
no change     /home/conda/forge/bin/conda-env
no change     /home/conda/forge/bin/activate
no change     /home/conda/forge/bin/deactivate
no change     /home/conda/forge/etc/profile.d/conda.sh
no change     /home/conda/forge/etc/fish/conf.d/conda.fish
no change     /home/conda/forge/shell/condabin/Conda.psm1
no change     /home/conda/forge/shell/condabin/conda-hook.ps1
no change     /home/conda/forge/lib/python3.7/site-packages/xontrib/conda.xsh
no change     /home/conda/forge/etc/profile.d/conda.csh
modified      /home/conda/.bashrc

==> For changes to take effect, close and re-open your current shell. <==

If you'd prefer that conda's base environment not be activated on startup, 
   set the auto_activate_base parameter to false: 

conda config --set auto_activate_base false

Thank you for installing Miniforge3!
conda@RPi4b:~$ 
```

</details>

8. Exit the shell and re-enter and verify that the `base` conda environment is active.

```sh
conda@RPi4b:~$ exit
logout
nerohmot@RPi4b:~$ su - conda
Password: 
(base) conda@RPi4b:~$
```

9. Look where `conda` itself is installed and:
  - set the uid bit for `conda`
  - remove execution bit 'others'
  - make a hard link to `/usr/bin`

```sh
(base) conda@RPi4b:~$ which conda
/home/conda/forge/bin/conda
(base) conda@RPi4b:~$ exit
logout
nerohmot@RPi4b:~$ sudo chmod u+s /home/conda/forge/bin/conda
[sudo] password for nerohmot:
nerohmot@RPi4b:~$ sudo chmod o-x /home/conda/forge/bin/conda
nerohmot@RPi4b:~$ sudo ln /home/conda/forge/bin/conda /usr/bin/conda
nerohmot@RPi4b:~$
```

Notes:
  - the `conda` user is **NOT** (and shall **NEVER** be) a `sudo-er`!
  - uninstalling means : `sudo deluser --remove-home --remove-all-files conda`


10. Install `mamba` in the `base` environment

<details>

```sh
nerohmot@RPi4b:~$ su - conda
Password:
(base) conda@RPi4b:~$ conda install mamba
Collecting package metadata (current_repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/conda/forge

  added / updated specs:
    - mamba


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    ca-certificates-2020.6.20  |       hecda079_0         146 KB  conda-forge
    certifi-2020.6.20          |   py37hc8dfbb8_0         151 KB  conda-forge
    icu-67.1                   |       h4c5d2ac_0        13.2 MB  conda-forge
    krb5-1.17.1                |       h09dc549_1         1.5 MB  conda-forge
    libarchive-3.3.3           |    h3a8160c_1008         1.8 MB  conda-forge
    libcurl-7.71.1             |       hcdd3856_3         321 KB  conda-forge
    libedit-3.1.20191231       |       h46ee950_1         132 KB  conda-forge
    libiconv-1.15              |    h6dd45c4_1006         2.0 MB  conda-forge
    libsolv-0.7.14             |       h8b12597_3         453 KB  conda-forge
    libssh2-1.9.0              |       hab1572f_4         227 KB  conda-forge
    libxml2-2.9.10             |       h8b8c825_2         1.4 MB  conda-forge
    lz4-c-1.9.2                |       he1b5a44_1         245 KB  conda-forge
    lzo-2.10                   |    h14c3975_1000         317 KB  conda-forge
    mamba-0.4.3                |   py37h782c684_0         630 KB  conda-forge
    zstd-1.4.5                 |       h6597ccf_2         811 KB  conda-forge
    ------------------------------------------------------------
                                           Total:        23.3 MB

The following NEW packages will be INSTALLED:

  icu                conda-forge/linux-aarch64::icu-67.1-h4c5d2ac_0
  krb5               conda-forge/linux-aarch64::krb5-1.17.1-h09dc549_1
  libarchive         conda-forge/linux-aarch64::libarchive-3.3.3-h3a8160c_1008
  libcurl            conda-forge/linux-aarch64::libcurl-7.71.1-hcdd3856_3
  libedit            conda-forge/linux-aarch64::libedit-3.1.20191231-h46ee950_1
  libiconv           conda-forge/linux-aarch64::libiconv-1.15-h6dd45c4_1006
  libsolv            conda-forge/linux-aarch64::libsolv-0.7.14-h8b12597_3
  libssh2            conda-forge/linux-aarch64::libssh2-1.9.0-hab1572f_4
  libxml2            conda-forge/linux-aarch64::libxml2-2.9.10-h8b8c825_2
  lz4-c              conda-forge/linux-aarch64::lz4-c-1.9.2-he1b5a44_1
  lzo                conda-forge/linux-aarch64::lzo-2.10-h14c3975_1000
  mamba              conda-forge/linux-aarch64::mamba-0.4.3-py37h782c684_0
  zstd               conda-forge/linux-aarch64::zstd-1.4.5-h6597ccf_2

The following packages will be UPDATED:

  ca-certificates                     2020.4.5.1-hecc5488_0 --> 2020.6.20-hecda079_0
  certifi                         2020.4.5.1-py37hc8dfbb8_0 --> 2020.6.20-py37hc8dfbb8_0


Proceed ([y]/n)? y

ncurses-6.2          | 1015 KB   | #################################################### | 100% 

Downloading and Extracting Packages
zstd-1.4.5           | 811 KB    | #################################################### | 100% 
libarchive-3.3.3     | 1.8 MB    | #################################################### | 100% 
ca-certificates-2020 | 146 KB    | #################################################### | 100% 
mamba-0.4.3          | 630 KB    | #################################################### | 100% 
libxml2-2.9.10       | 1.4 MB    | #################################################### | 100% 
lz4-c-1.9.2          | 245 KB    | #################################################### | 100% 
libiconv-1.15        | 2.0 MB    | #################################################### | 100% 
libedit-3.1.20191231 | 132 KB    | #################################################### | 100% 
libssh2-1.9.0        | 227 KB    | #################################################### | 100% 
libcurl-7.71.1       | 321 KB    | #################################################### | 100% 
certifi-2020.6.20    | 151 KB    | #################################################### | 100% 
libsolv-0.7.14       | 453 KB    | #################################################### | 100% 
icu-67.1             | 13.2 MB   | #################################################### | 100% 
lzo-2.10             | 317 KB    | #################################################### | 100% 
krb5-1.17.1          | 1.5 MB    | #################################################### | 100% 
Preparing transaction: done
Verifying transaction: done
Executing transaction: done
(base) conda@RPi4b:~$ 
```

</details>

11. Exit the `conda` user shell and add all users that will use the `base` installation to the `conda` group.

```sh
(base) conda@RPi4b:~$ exit
logout
nerohmot@RPi4b:~$ sudo adduser nerohmot conda
[sudo] password for nerohmot: 
Adding user `nerohmot' to group `conda' ...
Adding user nerohmot to group conda
Done.
nerohmot@RPi4b:~$ sudo adduser goofy conda
Adding user `goofy' to group `conda' ...
Adding user nerohmot to group conda
Done.
nerohmot@RPi4b:~$
```

12. The users in the `conda` group can now initialize conda (from their path, as `/usr/bin` holda a hardlink to `conda`)

```sh
nerohmot@RPi4b:~$ conda init
no change     /home/conda/forge/condabin/conda
no change     /home/conda/forge/bin/conda
no change     /home/conda/forge/bin/conda-env
no change     /home/conda/forge/bin/activate
no change     /home/conda/forge/bin/deactivate
no change     /home/conda/forge/etc/profile.d/conda.sh
no change     /home/conda/forge/etc/fish/conf.d/conda.fish
no change     /home/conda/forge/shell/condabin/Conda.psm1
no change     /home/conda/forge/shell/condabin/conda-hook.ps1
no change     /home/conda/forge/lib/python3.7/site-packages/xontrib/conda.xsh
no change     /home/conda/forge/etc/profile.d/conda.csh
modified      /home/nerohmot/.bashrc

==> For changes to take effect, close and re-open your current shell. <==

nerohmot@RPi4b:~$ source ~/.bashrc
(base) nerohmot@RPi4b:~$ 
```

