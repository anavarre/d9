# Drupal 9 installer

## Setup

### Method 1: Add it to your PATH

Copy the `d9.py` file under e.g. `/usr/local/bin/d9` to invoke it from anywhere.

### Method 2: use your .bash_aliases file

Alternatively, simply create the following Bash alias in your `.bash_aliases` file to invoke the script from anywhere.

```
alias d9='path/to/d9.py'
```

Do not forget to enable those changes immediately, so you can avoid to logout or reboot.

```
source ~/.bash_aliases
```

## Usage

Just type `d9 [--install|--wipe]` in a terminal.

```
usage: d9.py [-h] (--install | --wipe)

Drupal 9 installer

optional arguments:
-h, --help  show this help message and exit
--install   Spin up a new Lando app and install Drupal
--wipe      Reset the Git repo and destroy all Lando containers
```

Note: `sudo` is required for the `--wipe` parameter.

## Useful info

The site is accessible at https://drupal9.lndo.site and the credentials you need are admin/admin.

Your browser will warn of an untrusted SSL certificate. This is normal and expected. Just approve an exception.
