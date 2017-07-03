#!/usr/bin/env python
'''Html parsing and dataframe utility'''

''' \/ Third-Party Imports \/ '''
# import matplotlib.pyplot as plt
# import matplotlib
import pandas as pd
import os, sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import logging

# Add problem you are trying to solve in DocString


''' TO DO, ! = importance
!! Check for invalid file type (also check if it's a string) [ ]
!! check for invalid url [ ]
!! check for existing files [ ]
!!! If multiple hrefs, list and let the user choose - fig 1 [ ]
!!! add http:// at the beggining if missing [*]
! be more flexible with format [ ]
'''

'''fig 1
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
'''



logging.basicConfig(filename='debug', filemode='w', level=logging.DEBUG)

def find_download_links(url, filetype, output_name):
    error = 'none'
    p_url = urlparse(url)
    domain = '{urm.scheme}://{urm.netloc}'.format(urm=p_url)
    dl_name = output_name                          #
    if filetype == output_name[-4:]:               # Format the file name so user input is flexible
        dl_name = output_name[:len(output_name)-4] # Can include file extension or none
    if url[-4:] == filetype:    # Before anything, check if the url entered IS a dl link
        urllib.request.urlretrieve(url, dl_name + filetype)
        print("file downloaded succesfully as " + dl_name)
        error = "None"
        return
    else:
        r = urllib.request.urlopen(url)
        soup = BeautifulSoup(r, "html.parser")
        ext_length = len(filetype)
        for link in soup.find_all('a', string=True): #look through the link tags as strings
            no_tags = link.get('href')
            if no_tags != None: # Null check
                logging.info(str(no_tags))
                if filetype == str(no_tags)[-ext_length:]: # Check the three letter file extension
                    if 'http://' not in no_tags: # If no first part of the url, add it
                        no_tags = domain + no_tags
                    urllib.request.urlretrieve(no_tags, dl_name + filetype)
                    print("file downloaded succesfully as " + dl_name)
                    error = "None"
                    break
                elif filetype not in str(no_tags):
                    error = 'No file found for that extension (' + filetype + ')'
    return error

def compare(df1, df2, moments):
    if df.get_df_column(df1, 0) == df.get_df_column(df2, 0):
        pd.set_index

    pass




''' useless besides not having to import pandas into other files
def read_tsv(file_path, delim):  # Read the .tsv into the Dataframe
    data = pd.read_table(file_path, delimiter=delim)  # Read the data out of the .tsv and store it in data
    return data  # Return the Dataframe
'''

def set_df_names(df, names):
    df.columns(names)


def set_index(df, index):  # Sets a new index and drops that column
    df.set_index(index, drop=true)


def get_df_column(df, arg):  # Getter for entire columns of the Dataframe
    return df.iloc[arg, :]


def get_df_row(df, arg):  # Getter for entire rows of the Dataframe
    return df.iloc[: , arg]


def get_df_cell(df, col, row):  # Getter for cells of the Dataframe
    return df.iloc(col, row)
