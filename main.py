import os
from datetime import datetime
from dateutil import relativedelta

CWD = os.getcwd()
ROOT_PATH = os.path.abspath(CWD)
SUB_DIRS = [name for name in os.listdir(CWD) if os.path.isdir(name)]
TODAY = datetime.now()

def find_old_projects(weeks):
    recents = []
    for directory in SUB_DIRS:
        dir_date_time = datetime.fromtimestamp(os.stat(directory).st_atime)
        if dir_date_time < TODAY - relativedelta.relativedelta(weeks=weeks):
            recents.append(directory)
    return recents


print(find_old_projects(12))

# for directory in recents:
    #     subdir_path = ROOT_PATH + '/' + directory
    #     print([dirname for dirname in os.listdir(directory) if dirname == "node_modules"])
    # for directory in recents:
    #     subdir_path = ROOT_PATH + '/' + directory
    #     f=[]
    #     for dirpath, dirnames, filenames in os.walk(subdir_path):
    #         f.extend(dirnames)
    #         break
    #     print(f, '📝')