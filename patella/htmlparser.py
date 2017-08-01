#!/usr/bin/env python
"""Html parsing and dataframe utility"""

''' \/ Third-Party Imports \/ '''
from bokeh.plotting import figure, show
from bokeh.palettes import Plasma256
from bokeh.embed import components
from flask import render_template
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import os, sys
import urllib.request
import logging
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime

# Add problem you are trying to solve in DocString


''' TO DO, ! = importance
!! Check for invalid file type (also check if it's a string) [*]
!! catch invalid url [ ]
!! check for existing files [ ]
!!! If multiple hrefs, list and let the user choose - fig 1 [*]
!!! add http:// at the beginning if missing [*]
! be more flexible with format [*]
!!! clean code - no redundant setting, remove cruft[*]
'''

'''Some useful data frame commands'''


def set_df_names(df, names):
    df.columns(names)


def get_df_column(df, arg):   # Getter for entire columns of the Dataframe
    return df.iloc[arg, :]


def get_df_row(df, arg):   # Getter for entire rows of the Dataframe
    return df.iloc[:, arg]


def get_df_cell(df, col, row):   # Getter for cells of the Dataframe
    return df.iloc[col, row]

logging.basicConfig(filename='debug', filemode='w', level=logging.DEBUG)  # create a logging/print function for me
fe_url = 'http://www.enchantedlearning.com/history/us/pres/list.shtml'
fe_table = pd.read_html(fe_url, match='Vice-President', flavor='bs4', header=0, index_col=2, parse_dates=True)[0]
fe_names = []


index_list = fe_table.index.get_level_values(0).values.tolist()
year_list = []
for item in index_list:
    term_num = item.split('-')[0]
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
fe_table.set_index('year', drop=True, inplace=True)


def get_fe():
    return fe_table


def download_approved(ext, filep):
    approved_exts = ['.csv', '.tsv']
    delim = ''
    problem = 'none'
    for item in approved_exts:
        if ext == item:
            if item is '.csv':
                delim = ','
            elif item is '.tsv':
                delim = '\t'
            else:
                problem = 'some'
    try:
        filep.encode('utf-8').strip()
        pd.read_table(filep, delim, header=0, engine='python')
    except Exception as exc:
        logging.log(logging.DEBUG, msg=exc)
        problem = 'some'
    if problem == 'none':
        return True
    elif problem == 'some':
        return False


def find_download_links(url, filetype, output_name, in_number=0, download=False, clobber=True):

    """
    :param url: url to be scraped
    :param filetype: filetype to look for in the scraped url
    :param output_name: name of the file to be downloaded
    :param in_number: the number by order of the link in the url
    :param download: if the function should download a file or just return
    :param render: if the template should be rendered or the function should just return
    :param clobber: if files with the same name should be clobbered
    :return: a dictionary that returns an error as 'error', the outputname as 'filename' and the list of links in the url as 'href_list'
    """
    error = 'None'
    p_url = urlparse(url)
    domain = '{urm.scheme}://{urm.netloc}'.format(urm=p_url)
    dl_name = output_name
    link_list = []
    no_tags = ''
    ext_length = len(filetype)
    extension = url[-ext_length:]
    output_path = os.getcwd() + '/data/' + dl_name
    if filetype == output_name[-ext_length:]:   # Format the file name so user input is flexible
        dl_name = output_name[:len(output_name)-ext_length]   # Can include file extension or none
    # First and foremost, check if the user is entering a valid data format
    if extension == filetype:
        link_list.append(url)   # Before anything, check if the url entered IS a dl link
        if download:  # check if directory exists, check if file is parseable, check allowed file extensions
            urllib.request.urlretrieve(url, output_path)
            if not download_approved(extension, output_path):
                os.remove(output_path)
            else:
                print('file downloaded successfully as ' + dl_name)
    else:
        r = urllib.request.urlopen(url)
        soup = BeautifulSoup(r, 'html.parser')
        for link in soup.find_all('a', string=True):   # look through the link tags as strings
            no_tags = link.get('href')
            logging.info(str(no_tags))
            if filetype == str(no_tags)[-ext_length:]:   # Check the three letter file extension
                if 'http://' not in no_tags and 'https://' not in no_tags:   # If no first part of the url, add it
                    no_tags = domain + '/' + no_tags
                link_list.append(no_tags)
        if download:
            if no_tags != None:   # Null check
                if len(link_list) == 1:
                    print("One link found: " + no_tags)
                    urllib.request.urlretrieve(no_tags, output_path)
                    if not download_approved(extension, output_path):
                        os.remove(output_path)
                    else:
                        print('file downloaded successfully as ' + dl_name)
                elif len(link_list) > 1:
                    for idx, item in enumerate(link_list):
                        print(str(idx) + '. ' + item)
                    if int(in_number) <= len(link_list):
                        no_tags = link_list[int(in_number)]
                        urllib.request.urlretrieve(no_tags, output_path)
                        if not download_approved(extension, output_path):
                            os.remove(output_path)
                        else:
                            print('file downloaded succesfully as ' + dl_name)
                    else:
                        error = 'No link found with that number (' + str(in_number) + ')'
                else:
                    error = 'No links found!'
            elif filetype not in str(no_tags):
                error = 'No file found for that extension (' + filetype + ')'
    return { 'error':error, 'download_name':dl_name, 'href_list':link_list }


def file_to_htmltable(filepath):
        dataframe = pd.read_table(filepath, ',', header=0, engine='python')
        htmltable = dataframe.to_html(bold_rows=True, escape=True)
        return htmltable


def compare(df1, fedf, col, title, x_lb, y_lb, year_col='Year', html='plotlocal.html', render=True):
    """
    :param df1: the first data frame to be compared.
    :param fedf: the second dataframe to be compared, always fe_list.
    :param col: the data column of the first data frame which holds the dates needed to be compared.
    :param title: the title of the plot to be exported.
    :param x_lb: the title of the x axis for the exported plot.
    :param y_lb: the title of the y axis for the exported plot.
    :param html: the html page to be rendered.
    :return: a render_template object which sends a bokeh js/html/css plot to the page as well as a special div.
    """

    #### V Some Global variables V  ####
    data_col = int(col)
    df1.set_index(year_col, drop=True, inplace=True)
    ind_list = df1.index.get_level_values(0).values.tolist()
    office_yr_list = []
    party_office_list = []
    year_num = 1
    year_num_of = 1
    term_st_list = fedf.index.get_level_values(0)
    totalfe_list = []
    totalparty_list = []
    # populate a list with tuples of the year and the index where the year changes
    year_and_interval_list = [(i, ind_list[i-1]) for i, year in enumerate(ind_list) if i >=1 and ind_list[i-1] != ind_list[i]]
    interval = [tpl[0] for tpl in year_and_interval_list]
    years_list = [tpl[1] for tpl in year_and_interval_list]
    total_chg = [(df1.iloc[0, data_col]-df1.iloc[interval[i], data_col]) if i == 0
                 else (df1.iloc[interval[i-1], data_col] - df1.iloc[interval[i], data_col]) if interval[i] < len(ind_list)
                 else (df1.iloc[interval[i-1], data_col] - df1.iloc[(len(ind_list) - interval[i-1]), data_col])
                 for i, item in enumerate(years_list)]
    # A list of variation from year to year
    cov_list = [total_chg[i]/total_chg[i-1]*100 if total_chg[i-1] != 0 else 0 for i, n in enumerate(years_list)]
    for idx, item in enumerate(term_st_list):
        dist = 0
        if idx != len(term_st_list)-1:
            dist = int(term_st_list[idx+1]) - int(item)
        else:
            dist = datetime.datetime.now().year - int(item) + 1
        for n in range(dist):
            totalfe_list.append(fedf.iloc[idx, 0])
            totalparty_list.append(fedf.iloc[idx, 1])
    # A list of all years there have been presidents
    us_years = [yr+int(term_st_list[0]) for yr in range(int(term_st_list[-1]) - int(term_st_list[0]))]
    # A list of all the parties over every year of us presidency
    party_list = [totalparty_list[i] for i, item in enumerate(us_years) for years in years_list if years == item]
    # A list of all the fes over every year of us presidency
    fe_list = [totalfe_list[i] for i, item in enumerate(us_years) for years in years_list if years == item]

    # Make the 'years in office' and 'party in office' lists
    # list  comprehension possible?
    for idx, item in enumerate(fe_list):
        if idx >= 1 and fe_list[idx - 1] == fe_list[idx]:   # After at least one loop (to avoid oob error) and if the index doesnt change
            year_num += 1
        else:
            year_num = 1
        office_yr_list.append(year_num)   # append the year number
    for idx, item in enumerate(party_list):
        if idx >= 1 and party_list[idx - 1] == party_list[idx]:  # After at least one loop (to avoid oob error) and if the index doesnt change
            year_num_of += 1
        else:
            year_num_of = 1
        party_office_list.append(year_num_of)   # append the year number

    plotframe = pd.DataFrame({'foo': []})
    plotframe['Total Change'] = total_chg
    plotframe['Percent Change'] = cov_list
    plotframe['Years'] = years_list
    plotframe['Party'] = party_list
    plotframe['First Executive'] = fe_list
    plotframe['Years in Office'] = office_yr_list
    plotframe['Years Party in Office'] = party_office_list
    plotframe.set_index('foo', drop=True, inplace=True)
    plotframe.set_index('Years', drop=False, inplace=True)
    styles = ['r.-', 'bo-', 'y^-']
    fig, ax = plt.subplots(figsize=(15, 15))
    grouped = plotframe.groupby('First Executive')
    lineplot = grouped.plot(x='Years in Office', y='Percent Change', kind='line', ax=ax, title=title)
    plt.xlabel(x_lb)
    plt.ylabel(y_lb)
    ax.legend(grouped.groups.keys())
    p = figure(title=title, x_axis_label=x_lb, y_axis_label=y_lb, tools="pan,box_zoom,reset,save", toolbar_location='below', toolbar_sticky=False)
    palette = Plasma256 #[val for val in Plasma256.values()]
    imdex = -1
    for name, data in grouped:
        imdex += 1
        p.line(x=data['Years in Office'], y=data['Percent Change'], color=palette[imdex*10], legend=name) #palette[imdex]
    script, div = components(p) # make a bokeh graph out of the plot
    df_htmltable = plotframe.to_html(bold_rows=True, escape=True, classes='dftable') # convert the datframe to html for easy display\
    show(p)
    if render:
        return render_template(html, script=script, div=div, table=df_htmltable)
    else:
        return {'plot_frame':plotframe, 'input_frame':df1}