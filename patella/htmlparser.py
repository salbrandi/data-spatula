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
import re
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Add problem you are trying to solve in DocString


''' TO DO, ! = importance
!! Check for invalid file type (also check if it's a string) [*]
!! check for invalid url [ ]
!! check for existing files [ ]
!!! If multiple hrefs, list and let the user choose - fig 1 [~]
!!! add http:// at the beginning if missing [*]
! be more flexible with format [*]
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
fe_names = []


index_list = fe_table.index.get_level_values(0).values.tolist()
year_list = []
for item in index_list:
    term_num = item.split('-')[0]
    # term_length = int(item.split('-')[0]) - int(item.split('-')[1])
    year_list.append(term_num)
fe_table['year'] = year_list

fe_table.set_index('President', drop=False, inplace=True)
for idx, item in enumerate(fe_table.index.get_level_values(0).values.tolist()):
    fe_name = ''
    for char in item:
        if char.isalpha() or char == ' ':
            fe_name = fe_name + char
    fe_names.append(fe_name)
fe_table['President'] = fe_names
print(fe_table)
fe_table.set_index('year', drop=True, inplace=True)
# print(fe_table) debugging


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


def compare(df1, df2, col, title, x_lb, y_lb):
    #### V Some Global variables V ####
    data_col = int(col)
    df1.set_index('Year', drop=True, inplace=True)
    ind_list = df1.index.get_level_values(0).values.tolist()
    years_list = []
    interval = 0
    total_chg = []
    cov_list = []
    party_list = []
    fe_list = []
    office_yr_list = []
    party_office_list = []
    foo = 0
    year_num = 1
    year_num_of = 1
    for idx, item in enumerate(ind_list): # loop through the index of the data frame
        if idx >= 1 and ind_list[idx-1] != ind_list[idx]: # After at least one loop (to avoid oob error) and if the index changes
            years_list.append(ind_list[idx-1])  # append that value that changed
            if interval == 0: # if its the first time setting the interval
                interval = idx # set the interval
    for idx, item in enumerate(years_list): # loop through the list of years
        begin = interval*(idx+1) - interval # set the beginning of the years
        end = interval*idx+1 # and the end
        total_chg.append(df1.iloc[begin, data_col] - df1.iloc[end, data_col]) # calculate total change across the year
    # print(total_chg) DEBUG
    for idx, item in enumerate(years_list):
        cov = total_chg[idx]/total_chg[idx-1]*100 # calculate change from year to year
        cov_list.append(cov) # add it to a list for the dataframe
    for idx, item in enumerate(df2.index.get_level_values(0)): # loop  through the fe_table
        yr = int(item)
        lowdiff = years_list[0] - yr
        highdiff = yr - years_list[len(years_list)-1]
        if idx >= 1: # after one iteration
            if yr > int(years_list[0]) and yr < int(years_list[len(years_list)-1]): # if  the term year is inside the year list
                for val in range(yr-foo):
                    party_list.append(df2.iloc[idx, 1]) #
                    fe_list.append(df2.iloc[idx, 0])    # Add the relevant cells to the list for the df col
            elif lowdiff < 4: # if the starting year of the term is lower
                for val in range(lowdiff): # still get the rest
                    party_list.append(df2.iloc[idx, 1]) # and
                    fe_list.append(df2.iloc[idx, 0])    # Add the relevant cells
        foo = yr
    # Make the 'years in office' and 'party in office'
    for idx, item in enumerate(fe_list):
        if idx >= 1 and fe_list[idx - 1] == fe_list[idx]:  # After at least one loop (to avoid oob error) and if the index doesnt change
            year_num += 1
        else:
            year_num = 1
        office_yr_list.append(year_num)  # append the year number
    for idx, item in enumerate(party_list):
        if idx >= 1 and party_list[idx - 1] == party_list[idx]: # After at least one loop (to avoid oob error) and if the index doesnt change
            year_num_of += 1
        else:
            year_num_of = 1
        party_office_list.append(year_num_of)  # append the year number
    # find first common year and start there. color data based on party
    plotframe = pd.DataFrame({'foo' : []})
    plotframe['Total Change'] = total_chg
    plotframe['% Change'] = cov_list
    plotframe['Years'] = years_list
    plotframe['Party'] = party_list
    plotframe['First Executive'] = fe_list
    plotframe['Years in Office'] = office_yr_list
    plotframe['Years Party in Office'] = party_office_list
    plotframe.set_index('foo', drop=True, inplace=True)
    plotframe.set_index('Years', drop=False, inplace=True)
    print(plotframe)
    styles = ['r.-', 'bo-', 'y^-']
    fig, ax = plt.subplots(figsize=(15, 15))
    grouped = plotframe.groupby('First Executive')
    grouped.plot(x='Years in Office', y='% Change', kind='line', ax=ax, title=title)
    plt.xlabel(x_lb)
    plt.ylabel(y_lb)
    ax.legend(grouped.groups.keys())
    plt.show()