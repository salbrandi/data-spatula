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
# import dateparser

# Add problem you are trying to solve in DocString


''' TO DO, ! = importance
!! Check for invalid file type (also check if it's a string) [ ]
!! check for invalid url [ ]
!! check for existing files [ ]
!!! If multiple hrefs, list and let the user choose - fig 1 [ ]
!!! add http:// at the beginning if missing [*]
! be more flexible with format [ ]
'''

'''fig 1
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
'''
fe_url = 'http://www.enchantedlearning.com/history/us/pres/list.shtml'
fe_table = pd.read_html(fe_url, match='Vice-President', flavor='bs4', header=0, index_col=0)
for idx, item in enumerate(get_df_column(fe_table, 0)):
    fe_name = ''
    # fe_name_list = []
    for char in item:
        if char != '(':
            fe_name = fe_name + char
    fe_table.setcell(fe_name, 0, idx) # find the actual command please

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
        print('file downloaded succesfully as ' + dl_name)
        error = 'None'
        return
    else:
        r = urllib.request.urlopen(url)
        soup = BeautifulSoup(r, 'html.parser')
        ext_length = len(filetype)
        link_list = []
        for link in soup.find_all('a', string=True): #look through the link tags as strings
            no_tags = link.get('href')
            logging.info(str(no_tags))
            if filetype == str(no_tags)[-ext_length:]: # Check the three letter file extension
                if 'http://' not in no_tags: # If no first part of the url, add it
                    no_tags = domain + no_tagslink_list.append(no_tags)
                link_list.append(no_tags)
        if no_tags != None: # Null check
            if len(link_list=1):
                    urllib.request.urlretrieve(no_tags, dl_name + filetype)
                    print('file downloaded succesfully as ' + dl_name)
                    error = 'None'
            else:
                for idx, item in enumerable(link_list):
                    print(idx + '. ' + item)
                in_num = input('Which link is desired? (by number)')
                if len(in_number) <= len(link_list) and type(in_number) == int:
                    no_tags = link_list[in_num]
                    urllib.request.urlretrieve(no_tags, dl_name + filetype)
                    print('file downloaded succesfully as ' + dl_name)
                    error = 'None'
                else:
                    print('No link found with that number (' + in_number + ')')


        elif filetype not in str(no_tags):
                error = 'No file found for that extension (' + filetype + ')'
    return error

def compare(df1, df2, moments):
    if df.get_df_column(df1, 0) == df.get_df_column(df2, 0):
        pass
        # merge dataframes at the date column
    else:
        pass
        # Iterate through the rows of the index column and dateparse the dates,
        # then merge

        # take this resulting data fram and use its data to calculate moments


def plot(df):
    print(fe_table)
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
