# Python Unused Node Module Remover  

## Usage
Clone this repository. `cd` into the directory and install dependencies: 
```
$ pip install -r requirements.txt
``` 
Then make the script executable with:
```
$ chmod -x module_remover.py
```
Navigate to the parent directory that contains your Node projects and run the script with:
```
$ path/to/module_remover.py
```
The script checks your project directories to determine when they were last accessed. Projects that haven't been accessed within the timeframe you specify will have their `node_modules` directories prepared to be moved to the trash. 