#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os, sys
from bs4 import BeautifulSoup
import urllib.request
import re

# Add problem you are trying to solve in DocString


''' TO DO
Check for invalid file type (also check if it's a string)
check for invalid url
check for existing files
If multiple, list and let the user choose
'''

def find_download_links(url, filetype, output_name):
    error = 'none'
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    for link in soup.find_all('a', string=True):
        #no_tags = re.sub(r'<.*?>', "", link.get('href')) # What is this???
        no_tags = link.get('href')
        if no_tags != None:
            print(str(no_tags))
            if filetype in str(no_tags):
                urllib.request.urlretrieve(no_tags, output_name + filetype)
                print("file downloaded succesfully as " + output_name + filetype)
                error = "None"
                break
            elif filetype not in str(no_tags):
                error = 'No file found for that extension'
    return error


def read_tsv(file_path, delim):  # Read the .tsv into the Dataframe
    data = pd.read_table(file_path, delimiter=delim) # Read the data out of the .tsv and store it in data
    return data # Return the Dataframe


def set_df_names(df, names):
    df.columns(names)


def get_df_column(arg):  # Getter for entire columns of the Dataframe
    return fl.iloc[arg, :]


def get_df_row(arg):  # Getter for entire rows of the Dataframe
    return fl.iloc[: , arg]


def get_df_cell(col, row):  # Getter for cells of the Dataframe
    return fl.iloc(col, row)
