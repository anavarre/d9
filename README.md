# Drupal 9 installer

## Setup

Simply create the following Bash alias to invoke the script from anywhere.

```
alias d9='path/to/d9.py'
```

Do not forget to enable those changes immediately, so you can avoid to logout or reboot.

```
source ~/.bash_aliases
```

## Usage

```
usage: d9.py [-h] (--install | --wipe)

Drupal 9 installer

optional arguments:
-h, --help  show this help message and exit
--install   Spin up a new Lando app and install Drupal
--wipe      Reset Git repo and destroy Lando app
```

Note: we require the use of `sudo` for the `--wipe` parameter.
