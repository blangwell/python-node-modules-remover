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
    if len(results) > 0:
        # results[0] will be root node_modules dir
        return ROOT_PATH + "/" + results[0]

def find_nm_dirs(dirs):
    print("Searching for old node_modules...")
    nm_paths = []
    for folder in dirs:
        nm = get_nm_path(folder)
        if nm: 
            nm_paths.append(nm)
    if len(nm_paths) == 0:
        raise SystemExit(colored('No node_modules directories found! Exiting...', 'red'))
    print(f"\n##### Found " + colored(str(len(nm_paths)), 'blue', attrs=["bold"]) + " old node_modules directories #####")
    for nm in nm_paths:
        print(nm)
    return nm_paths

def get_weeks():
    weeks = input("How many weeks of node modules do you want to keep? (Default 12)\n> ")
    try:
        weeks = int(weeks)
    except ValueError:
        print(colored("Unrecognized input, defaulting to 12 weeks.", "red"))
        weeks=12
    return weeks

# loop through the nm_filepaths and send each directory to the trash
def trash_nms(nm_paths):
    for path in nm_paths:
        print(f"### Sending {path} to trash ###")
        send2trash(path)

def trash_yn(dirs):
    response = input(f"Send {len(dirs)} directories to the trash? y/n \n> ")
    if response.lower().strip() in ("y", "yes"):
        # trash_nms(dirs) 
        print("This is where trash_nms runs")
        raise SystemExit(f"{len(dirs)} directories successfully moved to trash\nExiting...")
    else: 
        raise SystemExit("Exiting...")

def welcome():
    hash_hr  = colored("\n######################################################\n", "blue")
    welcome = "\n" + colored("Welcome to the node_module spring cleaner ", "green") + colored("v0.1", "cyan", attrs=["underline"]) + "\n"
    print(hash_hr + welcome + hash_hr)

def main():
    welcome()
    weeks = get_weeks()
    old_projects = find_old_projects(weeks)
    nm_paths = find_nm_dirs(old_projects)
    trash_yn(nm_paths)


if __name__ == "__main__":
    main()