# Drupal 9 installer

## Prerequisites

Make sure the following executables are available in your system:

* `docker`
* `lando`
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

### Accessing the site

The site is accessible at http://drupal9.lndo.site - If you're running Apache or any other app binding to port 80, then Lando will try to bind to another port (e.g. `8000` or `8080`). Your options are thus to either free up port 80 (see below to find out how), use the automatically-assigned port or try one of the other Lando URLs such as https://drupal9.lndo.site (to prevent your browser from throwing a SSL warning, follow [this procedure](https://docs.lando.dev/config/security.html#trusting-the-ca))

#### How to find out if port 80 is already in use?

On Linux, try and use the `lsof` command to check if port 80 is already in use. Here's an example with a local Apache server (`apache2` service) that will conflict with Lando's attempt to bind on port 80 by default.

```
sudo lsof -n -i :80 | grep LISTEN
apache2 20953     root    4u  IPv6 28849622      0t0  TCP *:http (LISTEN)
apache2 20958 www-data    4u  IPv6 28849622      0t0  TCP *:http (LISTEN)
apache2 20959 www-data    4u  IPv6 28849622      0t0  TCP *:http (LISTEN)
apache2 20960 www-data    4u  IPv6 28849622      0t0  TCP *:http (LISTEN)
apache2 20962 www-data    4u  IPv6 28849622      0t0  TCP *:http (LISTEN)
apache2 20965 www-data    4u  IPv6 28849622      0t0  TCP *:http (LISTEN)
```

When Lando binds successfully to port 80 (via Docker), you should see something like this instead:

```
sudo lsof -n -i :80 | grep LISTEN
docker-pr 25050     root    4u  IPv6 28900587      0t0  TCP *:http (LISTEN)
```

### Credentials

Use `admin` for username and `admin` for password.
