from colorama import init as colorama_init
from datetime import datetime
from dateutil import relativedelta
import math
import os
from send2trash import send2trash
from termcolor import colored

CWD = os.getcwd()
ROOT_PATH = os.path.abspath(CWD)
SUB_DIRS = [sub for sub in os.listdir(CWD) if os.path.isdir(sub)]
TODAY = datetime.now()

colorama_init()
# print(colored('hello', 'green'))

"""
TODO: error handling for no node modules packages found
"""

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
    # print(ROOT_PATH + "/" + results[0] if len(results) > 0 else "no node modules found")
    # if node modules found
    if len(results) > 0:
        # results[0] will be root node_modules dir
        return ROOT_PATH + "/" + results[0]

def agg_nm_paths():
    old_projects = find_old_projects(12)
    nm_paths = []
    # loop through old projects and populate nm_paths with nm paths
    for project in old_projects:
        nm = get_nm_path(project)
        if nm: nm_paths.append(nm)
    # print(nm_paths)
    return nm_paths

# loop through the nm_filepaths and send each directory to the trash
def trash_nms(nm_paths):
    for path in nm_paths:
        print(f"### Sending {path} to trash ###")
        send2trash(path)

hash_hr  = "\n######################################################\n"
welcome = "\n" + colored("Welcome to the node_module spring cleaner ", "yellow") + colored("v0.1", "blue", attrs=["underline"]) + "\n"
def main():
    print(hash_hr + welcome + hash_hr)
    weeks = input("How many weeks of node modules do you want to keep? (Default 12)\n> ")
    try:
        weeks = int(weeks)
    except ValueError:
        print(colored("Unrecognized input, defaulting to 12 weeks.", "red"))
        weeks=12
    print("Searching for old node_modules...")
    old_projects = find_old_projects(weeks)
    nm_paths = []
    for project in old_projects:
        nm = get_nm_path(project)
        if nm: 
            # print(f"Found {nm}")
            nm_paths.append(nm)
    if len(nm_paths) == 0:
        raise SystemExit(colored('No node_modules directories found! Exiting...', 'red'))
    print(f"\n##### Found " + colored(str(len(nm_paths)), 'blue', attrs=["bold"]) + " old node_modules directories #####")
    for nm in nm_paths:
        print(nm)
    response = input(f"Send {len(nm_paths)} directories to the trash? y/n \n> ")
    if response.lower().strip() in ("y", "yes"):
        # trash_nms(nm_paths) 
        print("This is where trash_nms runs")
        raise SystemExit(f"{len(nm_paths)} directories successfully moved to trash\n Exiting...")
    else: 
        raise SystemExit("Exiting...")


if __name__ == "__main__":
    main()