# -*- coding: utf-8 -*-

# You can run the script with a CSV filename as an argument.
#
# python post-ocr.py IMG_20170602_120428.jpg.csv

from __future__ import print_function
import sys
import re, csv, datetime, os
import pdb

# print errors
def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)


def remove_empty_lines(rows, **kwargs):
  # second column defines name, which is defined in all valid rows
  for row in rows:
    if not row[1]: eprint('Removing potentially empty line: '+",".join(row))
  return [row for row in rows if row[1]]

# remove the header line that is printed on photographed pages
def remove_header_line(rows, **kwargs):
  if 'VIERAILIJAN NIMI' in rows[0][1]: del rows[0]
  return rows

# in beginning, string with name actually starts with card number - this column
# to be split
def add_card_number(rows, **kwargs):
  for row in rows:
    # if string starts with number or Xs, then it's a card number
    st = re.search('([0-9]+|[xX]+) (.*)', row[1])
    if st:
      card_number = st.group(1)
      row[1] = st.group(2)
    else:
      card_number = ''
    # add card_number as last element in list
    row.append(card_number)
  return rows

def add_group_id(rows, **kwargs):
  current_host_name = ''
  current_group_count = 0
  # default group id
  current_group_id = kwargs['page_id'] + '-' + str(current_group_count)
  for row in rows:
    if row[2] and row[2] != current_host_name:
      current_host_name = row[2]
      current_group_count += 1
      current_group_id = kwargs['page_id'] + '-' + str(current_group_count)
    # add group_id as last element in list
    row.append(current_group_id)
  return rows

def add_index(rows, **kwargs):
  index = 0
  for row in rows:
    row.insert(0, kwargs['page_id'] + '-' + str(index))
    index += 1
  return rows

# fill in time on rows where it's undefined, check time and date format
def fill_time(rows, **kwargs):
  pdb.set_trace()
  dt = datetime.datetime.strptime(kwargs['date'], '%Y-%m-%d')
  # default time
  current_time = dt.strftime('%Y-%m-%d %H:%M')
  for row in rows:
    if row[1]:
      if re.search('\d{1,2}:\d{1,2}', row[1]):
        date_string = '{} {}'.format(kwargs['date'], row[1])
        try:
          dt = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
          current_time = dt.strftime('%Y-%m-%d %H:%M')
        except:
          # current_time remains previously set value
          eprint('Invalid time format encountered: '+",".join(row))
    # overwrite column
    row[1] = current_time
  return rows

# fill in host information
def fill_host(rows, **kwargs):
  current_host = ''
  for row in rows:
    if row[3]: current_host = row[3]
    row[3] = current_host
  return rows

def fill_additional_info(rows, **kwargs):
  current_info = ''
  for row in rows:
    if row[4]: current_info = row[4]
    row[4] = current_info
  return rows

def add_affiliation(rows, **kwargs):
  for row in rows:
    # some text separated with either "/ or ","
    st = re.search('(.*?) ?[,\/] ?(.*)', row[2])
    if st:
      row[2] = st.group(1)
      row.append(st.group(2))
    else:
      row.append('')
  return rows

def add_contextual_columns(rows, **kwargs):
  for row in rows:
    row.append(kwargs['notified'])
    row.append(kwargs['location_id'])
    row.append(kwargs['page_id'])
  return rows

def add_header(rows, **kwargs):
  header = ['id','time','visitor name','host name','additional information','card number','group id','affiliation','notified','location id','page id']
  return [header] + rows


def get_filename_args(filename):
  fn = os.path.basename(filename)
  fn = fn.split('#')
  location_id = fn[0]
  date = fn[1]
  notified = fn[2]
  page_id = fn[3]
  return {'location_id': location_id, 'date': date, 'notified': notified, 'page_id': page_id}

def process_ocr_output(rows, **kwargs):
  functions = [remove_empty_lines, remove_header_line, add_card_number,
          add_group_id, add_index, fill_time, fill_host, fill_additional_info,
          add_affiliation, add_contextual_columns, add_header]
  for fn in functions:
    rows = fn(rows, page_id=kwargs['page_id'], date=kwargs['date'], notified=kwargs['notified'], location_id=kwargs['location_id'])
  return rows

# this gets called if you run the script (as opposed to e.g. importing)
if __name__ == '__main__':
  file = sys.argv[1]
  with open(file, 'rb') as csvfile:
    args = get_filename_args(csvfile.name)
    rs = csv.reader(csvfile, delimiter=',')
    rows = process_ocr_output(list(rs), page_id=args['page_id'], date=args['date'], notified=args['notified'], location_id=args['location_id'])
  writer = csv.writer(sys.stdout)
  for row in rows:
    writer.writerow(row)
