#!/usr/bin/env python
import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib
import os, sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

# Add problem you are trying to solve in DocString


''' TO DO
Check for invalid file type (also check if it's a string)
check for invalid url
check for existing files
If multiple, list and let the user choose
add http:// at the beggining if missing
'''

def find_download_links(url, filetype, output_name):
    error = 'none'
    p_url = urlparse(url)
    domain = '{urm.scheme}://{urm.netloc}'.format(urm=p_url)
    dl_name = output_name                          #
    if filetype == output_name[-4:]:               # Format the file name so user input is flexible
        dl_name = output_name[:len(output_name)-4] #
    r = urllib.request.urlopen(url)
    soup = BeautifulSoup(r, "html.parser")
    for link in soup.find_all('a', string=True): #look through the link tags as strings
        no_tags = link.get('href')
        if no_tags != None:
            print(str(no_tags))
            if filetype == str(no_tags)[-4:]: # Check the three letter file extension
                if 'http://' not in no_tags: # If no first part of the url, add it
                    no_tags = domain + no_tags
                urllib.request.urlretrieve(no_tags, dl_name + filetype)
                print("file downloaded succesfully as " + dl_name)
                error = "None"
                break
            elif filetype not in str(no_tags):
                error = 'No file found for that extension'
    return error


def read_tsv(file_path, delim):  # Read the .tsv into the Dataframe
    data = pd.read_table(file_path, delimiter=delim)  # Read the data out of the .tsv and store it in data
    return data  # Return the Dataframe


def set_df_names(df, names):
    df.columns(names)


def get_df_column(arg):  # Getter for entire columns of the Dataframe
    return fl.iloc[arg, :]


def get_df_row(arg):  # Getter for entire rows of the Dataframe
    return fl.iloc[: , arg]


def get_df_cell(col, row):  # Getter for cells of the Dataframe
    return fl.iloc(col, row)
