# Drupal 9 installer

## Setup

### PATH

Copy the file under e.g. `/usr/local/bin/d9` to invoke it from anywhere.

### .bash_aliases

Alternatively, simply create the following Bash alias to invoke the script from anywhere.

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
--wipe      Reset Git repo and destroy Lando app
```

Note: `sudo` is required for the `--wipe` parameter.

## Useful info

The site is accessible at https://drupal9.lndo.site and the credentials you need are admin/admin.

Your browser will warn of an untrusted SSL certificate. This is normal and expected. Just approve an exception.