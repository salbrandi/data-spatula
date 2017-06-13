# -*- coding: utf-8 -*-
'''Controls command line operations'''

''' \/ Third-Party Packages \/ '''
import click
import pandas as pd
import os, sys
import os.path

''' \/ Local Packages \/ '''
import htmlparser

''' \/ Variables \/ '''


'''Class test'''
class fileo():
    pass
file1 = fileo()
file2 = fileo()
file1.df = file2.df = 0
file1.path = file2.path = ''
file1.name = file2.name = ''
''''''

''' TO DO
Check for invalid file type (also check if it's a string)
'''


@click.group()
def patella():
    pass

@click.command()
@click.argument('url')
@click.option('--filename', default='dlfile', help='specify the name of the local file that will be downloaded to the current directory')
@click.option('--filetype', default='.csv', help='specify the file type the scraper will look for')
def scrape_url(url, filetype, filename):
    htmlparser.find_download_links(url, filetype, filename)
    click.echo('ERROR: ' + htmlparser.find_download_links(url, filetype, filename))  # Error reporting


@click.command()
@click.argument('file_one')
@click.argument('file_two')
@click.option('--delimiters', default=',:,', help='Specify file type delimiters in format <DELIM>:<DELIM2>')
def load_data(file_one, file_two, delimiters):
    file1.path = os.getcwd() + '/' + file_one
    file2.path = os.getcwd() + '/' + file_two
    print(file1.path + ', ' + file2.path)
    if os.path.exists(file1.path) and os.path.exists(file2.path):
        file1.name = file_one
        file2.name = file_two
        list_delims = delimiters.split(':')
        if len(list_delims) == 2:
            file1.df = pd.read_table(file1.path, list_delims[0])
            file2.df = pd.read_table(file2.path, list_delims[1])
            click.echo(file1 + ' table: ' + str(file1.df))
            click.echo(file2 + ' table: ' + str(file2.df))
            click.echo('files successfully loaded into Dataframes')
        elif len(list_delims) < 2:
            click.echo('too few arguments in list: delimiters')
        elif len(list_delims) > 2:
            click.echo('too many arguments in list: delimiters')
    else:
        if not os.path.exists(file1.path):
            click.echo('no files found with the name ' + file_one)
        if not os.path.exists(file2.path):
            click.echo('no files found with the name ' + file_two)



@click.command()
@click.argument('column')
@click.argument('filename')
def change_index(filename, column):
    if filename == file1:
        file1_df.set_index(column)
    else:
        click.echo('no file found with that name')
    pass


@click.command()
@click.argument('column_names')
@click.argument('file')
def change_names(file, column_names):
    pass


@click.command()
@click.argument('title')
@click.option('--x_title', default=' ', help='specify the X axis title')
@click.option('--y_title', default=' ', help='specify the Y axis title')
def plot():
    pass


@click.command()
@click.argument('url')
@click.argument('fltp')
def testme(url, fltp):
    click.echo(url, fltp)
    pass

patella.add_command(scrape_url, name='scrape')
patella.add_command(testme, name='test')
patella.add_command(plot)
patella.add_command(load_data, name='load')
