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


@app.route('/patella/input')
def flask_scrape():
    return render_template('page.html')


''' 
TO-DO: 
1. Turn the Input boxes into variables in both files for easier upkeep
2. Before displaying graph, redirect to options page with table - axis labes, graph title, data columns, etc
'''

@app.route('/patella/url_result', methods=['POST', 'GET'])
def flask_scraped():
    file = ''
    url = ''
    if request.method == 'POST':
        result=request.form
        print(result.items())
        for key, value in result.items():
            if key == 'Local File':
                file = value
                print(file)
            elif key == 'Data Scrape URL':
                url = value
        filepath = '/home/sbrandi/Desktop/patella/patella/data/indicator-4-2-0-4-1.transfer' + file
        df = pd.read_table(filepath, ',', header=0, engine='python')
        return htmlparser.compare(df, htmlparser.get_fe(), 3, '', '', '')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4444)
