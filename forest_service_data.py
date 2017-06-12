#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os, sys

# Add problem you are trying to solve in DocString

yr = int(sys.argv[1])  # need to check type of this
prior_year = yr-1
two_years_ago = yr-2
path = os.getcwd()
file = path + '/data/tabula-' + str(yr) + '.tsv' # name of the files
col_names=['Categories', two_years_ago, prior_year, yr, 'Total']

def read_tsv(file_path, year):  # Read the .tsv into the Dataframe
    data = pd.read_table(file_path) # Read the data out of the .tsv and store it in data
    return data # Return the Dataframe


def set_df_names(df, names):
    df.columns(names)


 fl = read_tsv(file, yr) # Call the function
 set_df_names(fl, col_names)

def get_df_column(arg):  # Getter for entire columns of the Dataframe
    return fl.iloc[arg, :]

def get_df_row(arg):  # Getter for entire rows of the Dataframe
    return fl.iloc[: , arg]

def get_df_cell(col, row):  # Getter for cells of the Dataframe
    return fl.iloc(col, row)


''' Debugging
 print(fl) # Print the Dataframe
 print(fl.info());
'''
fl.plot(x= 'Categories', y= yr, kind= 'bar')  # Plot the Dataframe
plt.gcf().subplots_adjust(bottom=0.5)
plt.ylabel('Thousands of Dollars (USD)')
plt.show()
plt.savefig('NationalForestServiceBudget' + str(yr) + ".svg", format="svg")
