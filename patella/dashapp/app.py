# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from htmlparser import compare, get_fe
import os
import pandas as pd

app = dash.Dash()

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

path = '/home/sbrandi/Desktop/patella/patella/indicator-4-2-0-4-1.transfer'
df = pd.read_table(path, ',', header=0)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
    Dash: A webb app framework for python
    '''),

    generate_table(compare(df, get_fe(), 3, '', '', ''))
])


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=4444)