#!/usr/bin/env python
from flask import Flask, render_template, request
import patella.htmlparser as htmlparser
import pandas as pd
import os

app = Flask(__name__)
# DATA_DIR = os.environ('DATA_DIR')  # update the directory path to use env variables

app.config['UPLOAD_FOLDER'] = 'uploads/'

urlpath = 'patella'



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/patella/input', methods =['POST', 'GET'])
def flask_scrape():
    return render_template('input.html')


@app.route('/patella/scrape_results', methods =['POST', 'GET'])
def scraped():
    linklist = []
    return render_template('plot.html')


'''
TO-DO:
1. Turn the Input boxes into variables in both files for easier upkeep
2. Before displaying graph, redirect to options page with table - axis labes, graph title, data columns, etc
'''



@app.route('/' + urlpath + '/options', methods=['POST', 'GET'])
def options():
    if request.method == 'POST':
        url = request.form['url']
        filetype = request.form['filetype']
        parseobj = htmlparser.find_download_links(url, filetype, 'datafile.csv', download=False)
        result = parseobj['href_list']
        return render_template('options.html', result=result, ftype=filetype)


@app.route('/' + urlpath + '/table', methods=['POST', 'GET'])
def table():
    if request.method == 'POST':
        dlname = request.form['dlink']
        outname = request.form['outname']
        print(outname)
        parseobj = htmlparser.find_download_links(dlname[:-1], '.csv', outname, download=True)
        result = parseobj['href_list']
        table = htmlparser.file_to_htmltable(os.getcwd() + '/data/' + outname)
        return render_template('table.html', linkname=dlname, table=table)#['template']

test_data = ['https://data.cityofnewyork.us/api/views/5t4n-d72c/rows.csv',
'http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python',
'http://www.sample-videos.com/download-sample-csv.php']


@app.route('/'+ urlpath + '/plotlocal', methods=['POST', 'GET'])
def plotted():
    filename = ''
    url = ''
    data_column = 0
    if request.method == 'POST':
        data_column = request.form['datacol']  # Get the data column input from html form
        result = request.form
        print(result.items())
        filename = result['filepath']
        filepath = filename
        df = pd.read_table(filepath, ',', header=0, engine='python')
        return htmlparser.compare(df, htmlparser.get_fe(), data_column, '', '', '')#['template']  # Return compare() which returns a render_template() object

@app.route('/' + urlpath +' /plot', methods=['POST', 'GET'])
def plot_from_df():
    if request.method == 'POST':
        data_column = request.form['datacol'] # get the data column from html form
        result = request.form
        filepath = os.getcwd() + '/data/' + 'datafile.csv'
        df = pd.read_table(filepath, ',', header=0, engine='python')
        return htmlparser.compare(df, htmlparser.get_fe(), data_column, '', '', '')#['template'] # Return compare() which returns a render_template() object


def startserver(path):
    urlpath = path
    app.run(debug=True, host='0.0.0.0', port=4444)


if __name__ == '__main__':
    startserver('patella')
