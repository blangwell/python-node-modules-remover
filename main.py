import os
from datetime import datetime
from dateutil import relativedelta

CWD = os.getcwd()
ROOT_PATH = os.path.abspath(CWD)
SUB_DIRS = [sub for sub in os.listdir(CWD) if os.path.isdir(sub)]
TODAY = datetime.now()

def find_old_projects(weeks):
    recents = []
    for directory in SUB_DIRS:
        dir_date_time = datetime.fromtimestamp(os.stat(directory).st_atime)
        if dir_date_time < TODAY - relativedelta.relativedelta(weeks=weeks):
            recents.append(directory)
    return recents

def get_nm_paths(directory):
    results = []
    for dirpath, dirnames, filenames in os.walk(directory):
        if 'node_modules' in dirnames:
            results.append(os.path.join(dirpath, 'node_modules'))
    print(ROOT_PATH + '/' + results[0] if len(results) > 0 else 'no node modules found')
    if len(results) > 0:
        return ROOT_PATH + '/' + results[0]

nm_paths = []
old_projects = find_old_projects(12)

# loop through old projects and populate nm_paths with nm paths
for project in old_projects:
    nm = get_nm_paths(project)
    if nm: nm_paths.append(nm)

print(nm_paths)

# alt method to recursively get all subdirectories inside of old project
# maybe_dirs = [x[0] for x in os.walk(old_projects[0])]
# print(maybe_dirs)