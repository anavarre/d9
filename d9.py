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
    "--wipe", action="store_true", help="Reset the Git repo and destroy all Lando containers"
)

args = parser.parse_args()
install = args.install
wipe = args.wipe


def check_requirements():
    """Check that all executables we need for this script are installed on the system."""

    executables = ["sudo", "docker", "lando"]

    for executable in executables:
        if not which(executable):
            print(f"ERROR: {executable} is required to run this application. Aborting.")
            sys.exit()


def check_git_branch():
    """Make extra sure we're running the script against an allowed branch."""

    head = os.getcwd() + "/.git/HEAD"

    if os.path.isfile(head):
      with open(head) as f:
          if "refs/heads/9" in f.read():
              print("===> Drupal 9 branch detected")
          else:
              print("ERROR: This doesn't seem to be a compatible Drupal 9 branch. Aborting.")
              sys.exit()
    else:
        print(f"ERROR: We cannot determine the Git branch. Aborting.")
        sys.exit()

def check_git_repo():
    """Check that we're working against a Git repository."""

    git_repo = os.getcwd() + "/.git"

    if os.path.isdir(git_repo):
        print("===> Git repository detected")
    else:
        print("ERROR: This doesn't seem to be a Git repository. Aborting.")
        sys.exit()

    check_git_branch()


def check_drupal_version():
    """Check we're indeed installing Drupal 9."""

    drupal_version = os.getcwd() + "/core/lib/Drupal.php"

    if os.path.isfile(drupal_version):
      with open(drupal_version) as f:
          if "const VERSION = '9" in f.read():
              print("===> Drupal 9 codebase detected")
          else:
              print("ERROR: This doesn't seem to be a Drupal 9 codebase. Aborting.")
              sys.exit()
    else:
        print(f"ERROR: The /core/lib/Drupal.php file doesn't seem to exist. Aborting.")
        sys.exit()


def create_lando_file():
    """Create a Lando configuration file optimized for Drupal 9."""

    lando_yml = os.getcwd() + "/.lando.yml"
    contents = """name: drupal9
recipe: drupal8
config:
  webroot: .
  php: 7.3
  mysql: 5.7
"""

    if not os.path.isfile(lando_yml):
        print("===> Creating Lando configuration file (PHP 7.3 / MySQL 5.7)")
        with open(lando_yml, "w") as f:
            f.write(contents)
    else:
        print("===> Lando configuration file already exists")


def start_app():
    """Start Lando app."""

    print("===> Starting app")
    call(["lando", "start"])

    # Wait a few seconds before installing Drupal, otherwise the database connection might fail.
    sleep(5)


def pull_dependencies():
    """Pull Composer dependencies."""

    composer_json = os.getcwd() + "/composer.json"

    if os.path.isfile(composer_json):
        print("===> composer.json detected")
    else:
        print("ERROR: There doesn't seem to be a composer.json file. Aborting.")
        sys.exit()

    print("===> Pulling Composer dependencies")
    call(["lando", "composer", "install", "-q"])

    print("===> Installing the latest Drush")
    call(["lando", "composer", "require", "drush/drush", "-q"])


def install_drupal():
    """Install Drupal automatically and log in admin user."""

    profile = "standard"
    creds = "drupal8"
    port = "3306"
    uri = "http://drupal9.lndo.site:8000"

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
            "--site-name=Drupal 9",
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
        print(f"===> Delete {os.path.basename(vendor)} directory")
        rmtree(os.getcwd() + "/vendor")
    else:
        print(f"INFO: The {os.path.basename(vendor)} directory doesn't exist. Skipping.")

    if os.path.isdir(default):
        print(f"===> Delete {os.path.basename(default)} directory")
        # We can't use rmtree here because of read-only permissions.
        call(["sudo", "rm", "-Rf", default])
    else:
        print(f"INFO: The {os.path.basename(default)} directory doesn't exist. Skipping.")


def git_cleanup():
    """Ensure the Git repo is entirely cleaned up and we're at the tip of the branch."""

    print("===> Pulling latest changes")
    call(["git", "clean", "-fdx"])
    call(["git", "reset", "--hard"])
    call(["git", "pull"])


def cleanup_operations():
    """Ensure we're back to a clean repo and there's no leftover from our app."""

    warning = input(
        "WARNING: This will reset your Git repo and pull the latest commit at the tip of your branch. Are you sure? (y/n) "
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
    check_git_repo()
    check_drupal_version()
    create_lando_file()
    start_app()
    pull_dependencies()
    install_drupal()
elif wipe:
    delete_app()
    cleanup_operations()
