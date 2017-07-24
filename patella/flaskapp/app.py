#!/usr/bin/env python
from flask import Flask, render_template, request
import htmlparser
import pandas as pd
import os

app = Flask(__name__)
# DATA_DIR = os.environ('DATA_DIR')  # update the directory path to use env variables


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

@app.route('/patella/plot', methods=['POST', 'GET'])
def plotted():
    filename = ''
    url = ''
    data_column = 0
    if request.method == 'POST':
        print("got here")
        data_column = request.form['datacol']
        filename = request.form['filepath']
        result = request.form
        print(result.items())
        for key, value in result.items():
            if key == 'Local File':
                filename = value
                print(filename)
            elif key == 'Data Scrape URL':
                url = value
        filepath =  filename
        df = pd.read_table(filepath, ',', header=0, engine='python')
        print(data_column)
        print(filename + ", " + url)
        return htmlparser.compare(df, htmlparser.get_fe(), data_column, '', '', '')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)
