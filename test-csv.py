# -*- coding: utf-8 -*-

# You can run the script with a CSV filename as an argument.
#
# python test-ocr.py IMG_20170602_120428.jpg.csv

from __future__ import print_function
import sys
import re, csv, datetime, os
import pdb

#def check_number_of_columns(rows, **kwargs):
def check_number_of_columns(rows):
  for row in rows:
    if(len(row) != 5):
      return False
  return True


#def get_filename_args(filename):
#  fn = os.path.basename(filename)
#  fn = fn.split('#')
#  date = fn[0]
#  location_id = fn[1]
#  notified = fn[2]
#  page_id = fn[3]
#  return {'location_id': location_id, 'date': date, 'notified': notified, 'page_id': page_id}


#def test_file(rows, **kwargs):
def test_file(rows):
  functions = [check_number_of_columns]
  for fn in functions:
    if not fn(rows):
      return False
  return True

# this gets called if you run the script (as opposed to e.g. importing)
if __name__ == '__main__':
  file = sys.argv[1]
  with open(file, 'rb') as csvfile:
#    args = get_filename_args(csvfile.name)
    rs = csv.reader(csvfile, delimiter=',')
#    if not test_file(list(rs), page_id=args['page_id'], date=args['date'], notified=args['notified'], location_id=args['location_id']):
    if not test_file(list(rs)):
      print(csvfile.name)
