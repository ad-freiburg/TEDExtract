# -*- coding: utf-8 -*-
'''
Copyright 2018, University of Freiburg.
Chair of Algorithms and Data Structures.
Markus Näther <naetherm@informatik.uni-freiburg.de>
'''

'''
Simple script for looping through many csv Files and concatenating their 
columns.
'''

import os
import sys
import glob
import argparse

import pandas as pd

def combine_csvs(input_dir, outname):
  '''
  '''
  csv_files = glob.glob(os.path.join(args.input_dir, '*.csv'))

  dff = pd.DataFrame()

  for file in csv_files:
    # Fetch the content
    temp = pd.read_csv(file, sep='\t', encoding='utf-8')
    # Concatenate
    dff = pd.concat([dff, temp])
  # Save the final result
  dff.to_csv(args.outname + '.csv', sep='\t', encoding='utf-8')

  # Also save all other information
  num_columns = len(dff.columns)

  for cIdx in range(1, num_columns):
    # Slice out the column
    ddff = dff[dff.columns[cIdx]].copy()

    # Remove all NaN values
    ddff = ddff.dropna(axis=0, how='all')

    # Save. Thereby get the correct column name
    col_name = list(dff.columns.values)
    col_name = col_name[cIdx]

    # And save as csv
    ddff.to_csv(
      args.outname + '.' + col_name + '.csv',
      sep='\t',
      encoding='utf-8')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--input_dir',
    type=str,
    help='The directory containing all csv files.'
  )
  parser.add_argument(
    '--outname',
    type=str,
    help='The name of the output file (can include a directionry name'
  )

  args = parser.parse_args()

  combine_csvs(args.input_dir, args.outname)
