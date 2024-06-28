# dataDirAnalyser


Set of functions to retrieve information about structured data in a directory.
Supported file types: .csv, .pkl, .json, .xlsx

**in active development**

## Usage

1. clone repository and create virtual environment using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) 
```
git clone https://github.com/LKSeiling/dataDirAnalyser.git
cd dataDirAnalyser
pyenv virtualenv 3.10.10 diralyzer
pyenv local diralyzer
python3 -m pip install -r requirements.txt
```

2. use, for example
- to get all valid files
```
valid_paths = get_valid_filepaths("/your/file/path/")
```
- to get information about the data in a specific file
```
file_path = "/your/file/path/"
info = get_column_info(filepath)
print(info)
```
- to get an overview of the existing data structures and the files that have them
```
result = {}

pbar = tqdm(all_paths, total=len(all_paths))
for filepath in pbar:
    try:
        pbar.set_description("Processing %s" % filepath)
        col_info = get_column_info(filepath)
        colnames = frozenset(col_info.keys())
        if colnames in result:
            result[colnames] = result[colnames] + [filepath]
        else:
            result[colnames] = [filepath]
    except Exception as e:
        print(f"Error: {e}, File: {filepath}")
```