from glob import glob
from copy import deepcopy
import pandas as pd
from tqdm import tqdm
import pickle
import os
from json import load as jload

def get_extension(filepath):
    ext = filepath.split(".")[-1]
    return ext

def get_valid_filepaths(base_dir):
    allowed_filetypes = ['csv','xlsx','pkl','json']
    if base_dir[-1] != "/":
        lookup_dir = "".join(base_dir,"/")
    else:
        lookup_dir = base_dir
    all_paths = [path for path in glob(f'{lookup_dir}**/*', recursive=True)]
    valid_file_paths = [path for path in all_paths if "$RECYCLE.BIN" not in path and "." in path and get_extension(path) in allowed_filetypes]
    return valid_file_paths

def get_column_info(filepath):
    file_type = filepath.split(".")[-1]
    if file_type == "csv":
        info = get_csv_info(filepath)
    elif file_type == "xlsx":
        info = get_xlsx_info(filepath)
    elif file_type == "pkl":
        info = get_pkl_info(filepath)
    elif file_type == "json":
        info = get_json_info(filepath)
    else:
        raise ValueError("The provided filetype is not supported.")
    return info

def get_encoding(filepath):
    with open(filepath) as f:
        enc = f.encoding
    return enc.lower()

def return_df_info(df):
    column_info = {}
    columns = df.columns.to_list()
    for column in df.columns.to_list():
        has_missing = df[column].isnull().any()
        dtype = df[column].dtype
        column_info[column] = {'has_missing': has_missing, 'dtype': dtype}
    return column_info

def get_csv_info(filepath):
    filesize = get_filesize(filepath)
    if filesize < 500000:
        try:
            enc = get_encoding(filepath)
            df = pd.read_csv(filepath, encoding=enc, engine='python', low_memory=False)
            info = return_df_info(df)
        except Exception as e:
            info = get_csv_info_from_chunks(filepath)
    else:
        info = get_csv_info_from_chunks(filepath)
    return info    

def get_xlsx_info(filepath):
    df = pd.read_excel(filepath)
    info = return_df_info(df)
    return info

def get_pkl_info(filepath):
    filesize = get_filesize(filepath)
    if filesize > 100000:
        pass
    else:
        with open(filepath, 'rb') as f:
            df = pickle.load(f)
        info = return_df_info(df)
        return info

def get_json_info(filepath):
    with open(filepath) as f:
        json_str = jload(f)
    df = pd.read_json(json_str)
    info = return_df_info(df)
    return info

def get_filesize(filepath):
    return int(os.path.getsize(filepath)/1000)

def get_csv_info_from_chunks(filepath):
    info = {}
    chunksize = 10 ** 4
    enc = get_encoding(filepath)
    with pd.read_csv(filepath, chunksize=chunksize, encoding=enc, low_memory=False) as reader:
        for chunk in reader:
            chunk_info = return_df_info(chunk)
            info = update_dict(info, chunk_info)
    return info
    

def update_dict(base_dict, input_dict):
    if base_dict != {}:
        res_dict = deepcopy(base_dict)
        for key in base_dict:
            new_col_info = input_dict[key]
            for sec_key in new_col_info:
                if (sec_key != "has_missing") or (res_dict[key]["has_missing"] != True):
                    res_dict[key][sec_key] == input_dict[key][sec_key]
        return res_dict
    else:
        return input_dict