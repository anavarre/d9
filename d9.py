#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drupal 9 installer"""

from shutil import which, rmtree
from subprocess import call
from time import sleep
import sys, os, argparse

parser = argparse.ArgumentParser(description="Drupal 9 installer")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    "--install", action="store_true", help="Spin up a new Lando app and install Drupal"
)
group.add_argument(
    "--wipe", action="store_true", help="Reset Git repo and destroy Lando app"
)

args = parser.parse_args()
install = args.install
wipe = args.wipe


def check_requirements():
    """Check that all executables we need for this script are installed on the system."""

    executables = ["sudo", "docker", "lando", "composer"]

    for executable in executables:
        if not which(executable):
            print(f"ERROR: {executable} is required to run this application. Aborting.")
            sys.exit()


def check_drupal_version():
    """Check we're indeed installing Drupal 9."""

    drupal_version = os.getcwd() + "/core/lib/Drupal.php"

    try:
        with open(drupal_version) as f:
            "const VERSION = '9.0.0-dev';" in f.read()
            print("===> Drupal 9 codebase detected")
    except:
        print("ERROR: This doesn't seem to be a Drupal 9 codebase. Aborting.")
        sys.exit()


def check_git_repo():
    """Only continue if we're working against a Git repository."""

    git_repo = os.getcwd() + "/.git"

    if os.path.isdir(git_repo):
        print("===> Git repository detected")
    else:
        print("ERROR: This doesn't seem to be a Git repository. Aborting.")
        sys.exit()


def pull_dependencies():
    """Pull Composer dependencies."""

    path = os.getcwd() + "/composer.json"

    if os.path.isfile(path):
        print("===> composer.json detected")
    else:
        print("ERROR: There doesn't seem to be a composer.json file. Aborting.")
        sys.exit()

    print("===> Pulling Composer dependencies")
    call(["composer", "install", "-q"])

    print("===> Installing the latest Drush")
    call(["composer", "require", "drush/drush", "-q"])


def create_lando_file():
    """Create a Lando configuration file optimized for Drupal 9."""

    path = os.getcwd() + "/.lando.yml"
    contents = """name: drupal9
recipe: drupal8
config:
  webroot: .
  php: 7.3
  mysql: 5.7
"""

    if not os.path.isfile(path):
        print("===> Creating Lando configuration file (PHP 7.3 / MySQL 5.7)")
        with open(path, "w") as f:
            f.write(contents)
    else:
        print("===> Lando configuration file already exists")


def start_app():
    """Start Lando app."""

    print("===> Starting app")
    call(["lando", "start"])

    # Wait a few seconds before installing Drupal, otherwise the database connection might fail.
    sleep(5)


def install_drupal():
    """Install Drupal automatically and log in admin user."""

    profile = "standard"
    creds = "drupal8"
    port = "3306"
    uri = "https://drupal9.lndo.site"

    print("===> Installing Drupal")
    call(
        [
            "lando",
            "drush",
            "site-install",
            profile,
            f"--db-url=mysql://{creds}:{creds}@database:{port}/{creds}",
            "--account-name=admin",
            "--account-pass=admin",
            "-y",
        ]
    )
    call(["lando", "drush", "user:login", f"--uri={uri}"])


def user_input():
    """Force user to agree to destructive operations."""

    print("ERROR: You must enter y/n (Yes or No).")


def delete_app():
    """Delete Lando app."""

    warning = input(
        "WARNING: This will completely destroy the Lando app. Are you sure? (y/n) "
    )

    if not warning:
        user_input()
        sys.exit()
    elif warning == "y":
        print("===> Deleting app")
        call(["lando", "destroy", "-y"])
    else:
        user_input()
        sys.exit()


def drupal_cleanup():
    """Delete vendor and sites/default directories."""

    vendor = os.getcwd() + "/vendor"
    default = os.getcwd() + "/sites/default"

    if os.path.isdir(vendor):
        print(f"===> Delete {vendor} directory")
        rmtree(os.getcwd() + "/vendor")
    else:
        print(f"INFO: The {vendor} path doesn't exist. Skipping.")

    if os.path.isdir(default):
        print(f"===> Delete {default} directory")
        # We can't use rmtree here because of read-only permissions.
        call(["sudo", "rm", "-Rf", default])
    else:
        print(f"INFO: The {default} path doesn't exist. Skipping.")


def git_cleanup():
    """Ensure the Git repo is entirely cleaned up with the latest commit in HEAD."""

    print("===> Pulling latest changes")
    call(["git", "clean", "-fdx"])
    call(["git", "reset", "--hard"])
    call(["git", "pull"])


def cleanup_operations():
    """Come back to a clean Git repository."""

    warning = input(
        "WARNING: This will reset your Git repo and pull the latest commit in HEAD. Are you sure? (y/n) "
    )

    if not warning:
        user_input()
        sys.exit()
    elif warning == "n":
        print("INFO: Operation cancelled by user.")
        sys.exit()
    elif warning == "y":
        drupal_cleanup()
    else:
        user_input()
        sys.exit()

    git_cleanup()


if install:
    check_requirements()
    check_drupal_version()
    check_git_repo()
    pull_dependencies()
    create_lando_file()
    start_app()
    install_drupal()
elif wipe:
    delete_app()
    cleanup_operations()
