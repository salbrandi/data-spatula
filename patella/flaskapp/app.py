#!/usr/bin/env python
from flask import Flask, render_template, request
import patella.htmlparser as htmlparser
import pandas as pd
import os

app = Flask(__name__)
# DATA_DIR = os.environ('DATA_DIR')   # update the directory path to use env variables

app.config['UPLOAD_FOLDER'] = 'uploads/'
urlpath = 'patella'

def startserver(path):
    global urlpath
    urlpath = path
    app.run(debug=True, host='0.0.0.0', port=4444)

@app.route('/')
def index():
    return render_template('index.html', name=urlpath)


@app.route('/<string:var>/input', methods =['POST', 'GET'])
def flask_scrape(var):
    return render_template('input.html', var=var)


@app.route('/<string:var>/scrape_results', methods =['POST', 'GET'])
def scraped(var):
    return render_template('plot.html', var=var)


'''
TO-DO:
1. Turn the Input boxes into variables in both files for easier upkeep
2. Before displaying graph, redirect to options page with table - axis labes, graph title, data columns, etc
'''



@app.route('/<string:var>/options', methods=['POST', 'GET'])
def options(var):
    if request.method == 'POST':
        url = request.form['url']
        filetype = request.form['filetype']
        parseobj = htmlparser.find_download_links(url, filetype, 'datafile.csv', download=False)
        result = parseobj['href_list']
        return render_template('options.html', result=result, ftype=filetype, var=var)


@app.route('/<string:var>/table', methods=['POST', 'GET'])
def table(var):
    if request.method == 'POST':
        dlname = request.form['dlink']
        outname = request.form['outname']
        print(outname)
        parseobj = htmlparser.find_download_links(dlname[:-1], '.csv', outname, download=True)
        print('got here')
        table = htmlparser.file_to_htmltable(os.getcwd() + '/data/' + outname)
        return render_template('table.html', linkname=dlname, table=table, var=var)#['template']

test_data = [
'https://data.cityofnewyork.us/api/views/5t4n-d72c/rows.csv',
'http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python',
'http://www.sample-videos.com/download-sample-csv.php',
'http://www.ehp.qld.gov.au/data-sets/soe2015/indicator-4-2-0-4-1.csv',
'https://vincentarelbundock.github.io/Rdatasets/datasets.html']


@app.route('/<string:var>/plotlocal', methods=['POST', 'GET'])
def plotted(var):
    if request.method == 'POST':
        data_column = request.form['datacol']   # Get the data column input from html form
        result = request.form
        print(result.items())
        filename = result['filepath']
        filepath = filename
        df = pd.read_table(filepath, ',', header=0, engine='python')
        return htmlparser.compare(df, htmlparser.get_fe(), data_column, '', '', '')  # Return compare() which returns a render_template() object

@app.route('/<string:var>/plot', methods=['POST', 'GET'])
def plot_from_df(var):
    if request.method == 'POST':
        result = request.form # store the form results as result
        data_column = result['datacol']  # get the data column from html form
        year_column = result['yearcol'] # get the year column from the html form
        filepath = os.getcwd() + '/data/' + 'datafile.csv'
        if os.path.isfile(filepath):
            df = pd.read_table(filepath, ',', header=0, engine='python')
            return htmlparser.compare(df, htmlparser.get_fe(), data_column, '', '', '', year_col=year_column)  # Return compare() which returns a render_template() object
        else:
            return render_template('input.html')
    




# if __name__ == '__main__':
#    startserver('patella')
