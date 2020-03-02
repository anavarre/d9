# Drupal 9 installer

## Prerequisites

Make sure the following executables are available in your system:

* `docker`
* `lando`
* `composer`
* `sudo`

Make sure you're only running this script against a compatible Drupal 9 branch (e.g. `9.0.x`). In doubt, clone the preferred branch like so:

```
git clone --branch 9.0.x https://git.drupalcode.org/project/drupal.git
```

## Setup

### Method 1: Add the script to your PATH

Copy the `d9.py` file under e.g. `/usr/local/bin/d9` to invoke it from anywhere.

### Method 2: create an alias in your .bash_aliases file

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

The site is accessible at https://drupal9.lndo.site and the credentials you need are `admin`/`admin`.

Your browser will warn of an untrusted SSL certificate. This is normal and expected as we don't have a self-signed certificate here. Just approve the exception.
