#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import os, sys
from flask import *


yr = 2017  # need to check type of this
path = 'C:/users/power/Desktop/Forest Service Data' # The Directory of the file needed, later change to current path os.getcwd()
file = path + '/tabula-' + str(yr) + '.tsv' # name of the files '''
app = Flask(__name__)


def read_tsv(file_path):  # Read the .tsv into the Dataframe
    data = pd.read_table(file_path) # Read the data out of the .tsv and store it in data
    return data # Return the Dataframe




fl = read_tsv(file, yr) # Call the function

@app.route("/tables")
def show_tables():
    data = pd.read_excel('dummy_data.xlsx')
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    females = data.loc[data.Gender=='f']
    males = data.loc[data.Gender=='m']
    return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    titles = ['na', 'Female surfers', 'Male surfers'])

if __name__ == "__main__":
    app.run(debug=True)
