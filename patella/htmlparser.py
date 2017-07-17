#!/usr/bin/env python
"""Html parsing and dataframe utility"""

''' \/ Third-Party Imports \/ '''

# import matplotlib
import pandas as pd
import os, sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import logging
# import dateparser
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Add problem you are trying to solve in DocString


''' TO DO, ! = importance
!! Check for invalid file type (also check if it's a string) [ ]
!! check for invalid url [ ]
!! check for existing files [ ]
!!! If multiple hrefs, list and let the user choose - fig 1 [ ]
!!! add http:// at the beginning if missing [*]
! be more flexible with format [ ]
'''

'''Some useful data frame commands'''


def set_df_names(df, names):
    df.columns(names)


def get_df_column(df, arg):  # Getter for entire columns of the Dataframe
    return df.iloc[arg, :]


def get_df_row(df, arg):  # Getter for entire rows of the Dataframe
    return df.iloc[: , arg]


def get_df_cell(df, col, row):  # Getter for cells of the Dataframe
    return df.iloc(col, row)

logging.basicConfig(filename='debug', filemode='w', level=logging.DEBUG)
fe_url = 'http://www.enchantedlearning.com/history/us/pres/list.shtml'
fe_table = pd.read_html(fe_url, match='Vice-President', flavor='bs4', header=0, index_col=2, parse_dates=True)[0]

''' cleaning up the indices, for later
for idx, item in enumerate(get_df_row(fe_table, 0)):
    fe_name = ''
    for char in item:
        if char != '(':
            if char != '/':
                fe_name = fe_name + char
        else:
            # print(fe_table.iloc[idx, 0])
            break
    fe_table.iloc[]
    print(fe_table)
    # print(get_df_row(fe_table, 0))
    # just reindex como asi 
    # fe_table['year'] = year_list
    # fe_table.set_index('year', drop=True, inplace=True)
'''


index_list = fe_table.index.get_level_values(0).values.tolist()
year_list = []
for idx, item in enumerate(index_list):
    term_num = item.split('-')[0]
    # term_length = int(item.split('-')[0]) - int(item.split('-')[1])
    year_list.append(term_num)

fe_table['year'] = year_list
fe_table.set_index('year', drop=True, inplace=True)
# print(fe_table) debugging


logging.basicConfig(filename='debug', filemode='w', level=logging.DEBUG)

def get_fe():
    return(fe_table)

def find_download_links(url, filetype, output_name):
    error = 'none'
    p_url = urlparse(url)
    domain = '{urm.scheme}://{urm.netloc}'.format(urm=p_url)
    dl_name = output_name                          #
    if filetype == output_name[-4:]:               # Format the file name so user input is flexible
        dl_name = output_name[:len(output_name)-4]  # Can include file extension or none
    if url[-4:] == filetype:    # Before anything, check if the url entered IS a dl link
        urllib.request.urlretrieve(url, dl_name + filetype)
        print('file downloaded successfully as ' + dl_name)
        error = 'None'
        return
    else:
        r = urllib.request.urlopen(url)
        soup = BeautifulSoup(r, 'html.parser')
        ext_length = len(filetype)
        link_list = []
        for link in soup.find_all('a', string=True):  # look through the link tags as strings
            no_tags = link.get('href')
            logging.info(str(no_tags))
            if filetype == str(no_tags)[-ext_length:]:  # Check the three letter file extension
                if 'http://' not in no_tags:  # If no first part of the url, add it
                    no_tags = domain + no_tags
                link_list.append(no_tags)
            if no_tags != None:  # Null check
                if len(link_list)==1:
                        urllib.request.urlretrieve(no_tags, dl_name + filetype)
                        print('file downloaded successfully as ' + dl_name)
                        error = 'None'
                else:
                    for idx, item in enumerate(link_list):
                        print(str(idx) + '. ' + item)
                    in_number = input('Which link is desired? (by number)')
                    if int(in_number) <= len(link_list):
                        no_tags = link_list[int(in_number)]
                        urllib.request.urlretrieve(no_tags, dl_name + filetype)
                        print('file downloaded succesfully as ' + dl_name)
                        error = 'None'
                    else:
                        error = 'No link found with that number (' + str(in_number) + ')'

            elif filetype not in str(no_tags):
                error = 'No file found for that extension (' + filetype + ')'
    return error


def compare(df1, df2):
    print(df1)
    df1.set_index('Year', drop=True, inplace=True)
    ind_list = df1.index.get_level_values(0).values.tolist()
    years_list = []
    interval = 0
    total_chg = []
    cov_list = []
    party_list = []
    fe_list = []
    foo = 0
    for idx, item in enumerate(ind_list):
        if idx > 1 and ind_list[idx-1] != ind_list[idx]:
            years_list.append(ind_list[idx-1])
            if interval == 0:
                interval = idx
    for idx, item in enumerate(years_list):
        begin = interval*(idx+1) - interval
        end = interval*idx+1
        total_chg.append(df1.iloc[begin, 3] - df1.iloc[end, 3])
    print(total_chg)
    for idx, item in enumerate(years_list):
        cov = total_chg[idx]/total_chg[idx-1]*100
        cov_list.append(cov)
        print(str(cov) + "%")
    for idx, item in enumerate(df2.index.get_level_values(0)):
        print(item)
        if idx > 1:
            if int(item) > int(years_list[0]) and int(item) < int(years_list[len(years_list)-1]):
                for val in range(int(item)-foo):
                    party_list.append(df2.iloc[idx, 1])
                    fe_list.append(df2.iloc[idx, 0])
            elif int(item) > int(years_list[len(years_list)-1]):
                difference = int(item) - years_list[len(years_list)-1]
                for val in range(difference):
                    party_list.append(df2.iloc[idx, 1])
                    fe_list.append(df2.iloc[idx, 0])
        foo = int(item)
    print(party_list)

    # find first common year and start there. color data based on party
    plotframe = pd.DataFrame({'foo' : []})
    plotframe['Total Change'] = total_chg
    plotframe['% Change'] = cov_list
    plotframe['Years'] = years_list
    plotframe['Party'] = party_list
    plotframe['President'] = fe_list
    print(plotframe)
    plt.figure()
    plotframe.plot(x='Years', y='% Change', kind='line')#, color='Party')
    plt.show()

def plot(df):
    print(fe_table)
    pass




''' useless besides not having to import pandas into other files
def read_tsv(file_path, delim):  # Read the .tsv into the Dataframe
    data = pd.read_table(file_path, delimiter=delim)  # Read the data out of the .tsv and store it in data
    return data  # Return the Dataframe
'''