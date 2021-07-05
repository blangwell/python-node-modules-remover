#!/usr/bin/env python3

from colorama import init as colorama_init
from datetime import datetime
from dateutil import relativedelta
import math
import os
from progress.spinner import Spinner
from send2trash import send2trash
import sys
from termcolor import colored, cprint
import time
import threading

CWD = os.getcwd()
ROOT_PATH = os.path.abspath(CWD)
SUB_DIRS = [sub for sub in os.listdir(CWD) if os.path.isdir(sub)]
TODAY = datetime.now()
HASH_HR = "\n######################################################\n"

colorama_init()  # windows term color compatibility


def main():
    welcome()
    weeks = get_weeks()
    old_projects = find_old_projects(weeks)
    nm_paths = find_nm_dirs(old_projects)
    trash_yn(nm_paths)


def find_old_projects(weeks):
    recents = []
    for directory in SUB_DIRS:
        dir_date_time = datetime.fromtimestamp(os.stat(directory).st_atime)
        if dir_date_time < TODAY - relativedelta.relativedelta(weeks=weeks):
            recents.append(directory)
    return recents


def get_nm_path(directory):
    results = []
    for dirpath, dirnames, filenames in os.walk(directory):
        if "node_modules" in dirnames:
            results.append(os.path.join(dirpath, "node_modules"))
    if len(results) > 0:
        # results[0] will be root node_modules dir
        return ROOT_PATH + "/" + results[0]


def find_nm_dirs(dirs):
    loading = True

    def spinner():
        spinner = Spinner("Searching for old node module dirs ")
        while loading:
            time.sleep(.2)
            spinner.next()
    spin_thread = threading.Thread(target=spinner)
    spin_thread.start()

    nm_paths = []
    for folder in dirs:
        nm = get_nm_path(folder)
        if nm:
            nm_paths.append(nm)

    loading = False
    spin_thread.join()
    if len(nm_paths) == 0:
        cprint("\nNo node_modules found!", "red", file=sys.stderr)
        print("Make sure you are running this script in a directory that contains npm project subdirectories.\nExiting...")
        sys.exit(1)

    count = colored(str(len(nm_paths)), 'cyan', attrs=["bold"])
    found = f"Found {colored(count, 'cyan')} old node_modules directories"
    print(f"\n{HASH_HR}\n{found}\n")
    for nm in nm_paths:
        print(">" + nm)
    print(HASH_HR)
    return nm_paths


def get_weeks():
    weeks = input(
        "How many weeks of node modules do you want to keep? (Default 12)\n> ")
    try:
        weeks = int(weeks)
        return weeks
    except ValueError:
        print(colored("Defaulting to 12 weeks...", "cyan"))
        return 12

# loop through the nm_filepaths and send each directory to the trash


def trash_nms(nm_paths):
    for path in nm_paths:
        print(colored(f"Trashing {path}", "cyan"))
        send2trash(path)


def trash_yn(dirs):
    response = input(
        colored(f"Send {len(dirs)} directories to the trash? y/n \n", "yellow") + "> ")
    if response.lower().strip() in ("y", "yes"):
        trash_nms(dirs)
        raise SystemExit(colored(
            f"{len(dirs)} directories successfully moved to trash\n", "green") + "Exiting...")
    else:
        raise SystemExit(
            colored("No directories moved to trash. \n", "cyan") + "Exiting...")


def welcome():
    hash_hr = "\n######################################################\n"
    welcome = "\n Welcome to the node_module remover tool v0.2 \n"
    print(hash_hr + welcome + hash_hr)


if __name__ == "__main__":
    main()
