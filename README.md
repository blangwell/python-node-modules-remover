# Python Unused Node Module Remover  

## Usage
Clone this repository. `cd` into the directory and install dependencies: 
```
$ pip install -r requirements.txt
``` 
then make the script executable with:
```
$ chmod -x module_remover.py
```

The script is built to be run from within a directory containing npm project subdirectories. Specify how many weeks of node_modules you want to save. The script will gather old projects' `node_module/` directories and prepare them to be sent to the trash. 