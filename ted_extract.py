# -*- coding: utf-8 -*-
'''
Copyright 2018, University of Freiburg.
Chair of Algorithms and Data Structures.
Markus Näther <naetherm@informatik.uni-freiburg.de>
'''

import argparse

from TEDExtract import TEDExtract

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--output',
    type=str,
    help='The directory where to save all information'
  )
  parser.add_argument(
    '--max_pages',
    type=int,
    default=76,
    help='The number of pages to extract'
  )

  args = parser.parse_args()

  extractor = TEDExtract(args)

  extractor.run()

if __name__ == '__main__':
  main()
