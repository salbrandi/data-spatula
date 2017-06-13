#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import os, sys
from flask import *

'''

---NO DEVELOPMENT AS OF NOW---

    ---NOT IMPLEMENTED---

      ---NEVER USED---

'''


app = Flask(__name__)

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
