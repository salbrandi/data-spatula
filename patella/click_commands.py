# -*- coding: utf-8 -*-
"""Controls command line operations"""

''' \/ Third-Party Packages \/ '''
import click
import pandas as pd
import os, sys
import os.path


''' \/ Local Packages \/ '''
import patella.htmlparser
import patella.flaskapp.app as flaskapp

''' \/ Variables \/ '''


'''Class test'''
class fileo():
    pass
file1 = fileo()
file2 = fileo()
file1.df = file2.df = pd.DataFrame({'foo' : []})
file1.path = file2.path = ''
file1.name = file2.name = ''
''''''

''' TO DO
Check for invalid file type (also check if it's a string)
Make function for setting both data frames at once - improves readability.
Add downloaded file names and paths to a text file for easy retrieval
Update load() method to save the files names to a text file that the other functions auto load - clobber each time
'''


@click.group()
def patella():
    pass

@click.command()
@click.argument('url')
@click.option('--filename', default='datafile', help='specify the name of the local file that will be downloaded to the current directory')
@click.option('--filetype', default='.csv', help='specify the file type the scraper will look for')
def scrape_url(url, filetype, filename):
    # htmlparser.find_download_links(url, filetype, filename)
    parseobj = htmlparser.find_download_links(url, filetype, filename, download=True)
    if type(parseobj) != 'NoneType':
        click.echo('ERROR: ' + parseobj['error'])  # Error reporting


# In webservice: Give index and relevant data options
@click.command()
@click.argument('file_one')
# @click.argument('file_two')
@click.option('--delimiters', default=',:,', help='Specify file type delimiters in format <DELIM>:<DELIM2>')
def load_data(file_one, delimiters):
    file1.path = os.getcwd() + '/' + file_one
    # file2.path = os.getcwd() + '/' + file_two
    # print(file1.path + ', ' + file2.path)

    if os.path.exists(file1.path): # and os.path.exists(file2.path):
        file1.name = file_one
        list_delims = delimiters.split(':')
        if len(list_delims) == 2:
            file1.df = pd.read_table(file1.path, list_delims[0], header=0)
            file2.df = htmlparser.get_fe()
            os.environ['LOCAL_FILE_PATH'] = file1.path
            # file2.df = pd.read_table(file2.path, list_delims[1])
            # click.echo(file1.name + ' table: ' + str(file1.df))
            # click.echo(file2.name + ' table: ' + str(file2.df))
            click.echo('file successfully loaded into Dataframes')
        # elif len(list_delims) > 2:
            # click.echo('too many arguments in list for option: --delimiters')
    else:
        if not os.path.exists(file1.path):
            click.echo('no files found with the name ' + file_one + ' in path ' + file1.path)
        # if not os.path.exists(file2.path):
            # click.echo('no files found with the name ' + file_two + ' in path ' + file1.path)



@click.command()
@click.argument('column')
@click.argument('filename')
def change_index(filename, column):
    if filename == file1:
        file1.df.set_index(column)
    else:
        click.echo('no file found with that name')


@click.command()
@click.argument('column_names')
@click.argument('file')
def change_names(file, column_names):
    pass


@click.command()
@click.argument('path')
def startserver(path):
    flaskapp.startserver(path)


@click.command()
@click.argument('file')
@click.argument('col')
@click.option('--title', default=' ', help='specify the plot title')
@click.option('--x_title', default=' ', help='specify the X axis title')
@click.option('--y_title', default=' ', help='specify the Y axis title')
def plot(file, col, title, x_title, y_title):
    file1.path = os.getcwd() + '/data/' + file
    file1.df = pd.read_table(file1.path, ',', header=0)
    htmlparser.compare(file1.df, htmlparser.get_fe(), col, title, x_title, y_title)


@click.command()
@click.argument('foo')
def testme(foo):
    pass


patella.add_command(scrape_url, name='scrape')
patella.add_command(testme, name='test')
patella.add_command(plot)
patella.add_command(load_data, name='load')
patella.add_command(startserver, name='startup')