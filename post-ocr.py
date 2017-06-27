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
    if not row[2]: eprint('Removing potentially empty line: '+",".join(row))
  return [row for row in rows if row[2]]

# remove the header line that is printed on photographed pages
def remove_header_line(rows, **kwargs):
#  if 'VIERAILIJAN NIMI' in rows[0][1]: del rows[0]
#  return rows
  return [row for row in rows if not 'VIERAILIJAN NIMI' in row[2]]


# in beginning, string with name actually starts with card number - this column
# to be split
def add_card_number(rows, **kwargs):
  for row in rows:
    # if string starts with number or Xs, then it's a card number
    st = re.search('([0-9]+|[xX]+) (.*)', row[2])
    if st:
      card_number = st.group(1)
      row[2] = st.group(2)
    else:
      card_number = ''
    # add card_number as last element in list
    row.append(card_number)
  return rows

def add_group_id(rows, **kwargs):
  current_host_name = ''
  current_group_count = 0
  # default group id
  current_group_id = rows[0][0] + '-' + str(current_group_count)
  for row in rows:
    if row[3] and row[3] != current_host_name:
      current_host_name = row[3]
      current_group_count += 1
      current_group_id = row[0] + '-' + str(current_group_count)
    # add group_id as last element in list
    row.append(current_group_id)
  return rows

def add_index(rows, **kwargs):
  index = 0
  for row in rows:
    row.insert(0, row[0] + '-' + str(index))
    index += 1
  return rows

# time is often garbled, let's try to convert it into standard format HH:MM
def fix_time(rows, **kwargs):
  for row in rows:
    orig_time = row[2]
    hour = ''
    if row[2]:
      st = re.search('(\d{1,2})[^\d](\d{2})', row[2])
      if st:
        hour = st.group(1)
        minute = st.group(2)
      if re.search('\d{4}', row[2]):
        hour = row[2][:2]
        minute = row[2][2:4]
      elif re.search('\d{3}', row[2]):
        hour = row[2][:1]
        minute = row[2][1:3]
    if hour:
      row[2] = hour+':'+minute
    row.append(orig_time)
  return rows

# fill in time on rows where it's undefined, check time and date format
def fill_time(rows, **kwargs):
  dt = datetime.datetime.strptime(kwargs['date'], '%Y-%m-%d')
  # default time
  current_time = dt.strftime('%Y-%m-%d %H:%M')
  for row in rows:
    if row[2]:
      if re.search('\d{1,2}:\d{1,2}', row[2]):
        date_string = '{} {}'.format(kwargs['date'], row[2])
        try:
          dt = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
          current_time = dt.strftime('%Y-%m-%d %H:%M')
        except:
          # current_time remains previously set value
          eprint('Invalid time format encountered: '+",".join(row))
    # overwrite column
    row[2] = current_time
  return rows

# fill in host information
def fill_host(rows, **kwargs):
  current_host = ''
  for row in rows:
    if row[4]: current_host = row[4]
    row[4] = current_host
  return rows

def fill_additional_info(rows, **kwargs):
  current_info = ''
  for row in rows:
    if row[5]: current_info = row[5]
    row[5] = current_info
  return rows

def add_affiliation(rows, **kwargs):
  for row in rows:
    # some text separated with either "/ or ","
    st = re.search('(.*?) ?[,\/] ?(.*)', row[3])
    if st:
      row[3] = st.group(1)
      row.append(st.group(2))
    else:
      row.append('')
  return rows

def add_contextual_columns(rows, **kwargs):
  for row in rows:
    row.append(kwargs['notified'])
    row.append(kwargs['location_id'])
  return rows

def add_header(rows, **kwargs):
  header = ['id','page_id','time','visitor name','host name','additional information','card number','group id','original time','affiliation','notified','location id']
  return [header] + rows


def get_filename_args(filename):
  fn = os.path.basename(filename)
  fn = fn.split('#')
  location_id = fn[0]
  date = fn[1]
  notified = fn[2]
  notified = notified.split('.')[0]
  return {'location_id': location_id, 'date': date, 'notified': notified}

def process_ocr_output(rows, **kwargs):
  functions = [remove_empty_lines, remove_header_line, add_card_number,
          add_group_id, add_index, fix_time, fill_time, fill_host, fill_additional_info,
          add_affiliation, add_contextual_columns, add_header]
  for fn in functions:
    rows = fn(rows, date=kwargs['date'], notified=kwargs['notified'], location_id=kwargs['location_id'])
  return rows

# this gets called if you run the script (as opposed to e.g. importing)
if __name__ == '__main__':
  file = sys.argv[1]
  with open(file, 'rb') as csvfile:
    args = get_filename_args(csvfile.name)
    rs = csv.reader(csvfile, delimiter=',')
    rows = process_ocr_output(list(rs), date=args['date'], notified=args['notified'], location_id=args['location_id'])
#  with open('csv.csv', 'a') as f:
#   writer = csv.writer(f)
  writer = csv.writer(sys.stdout)
  for row in rows:
    writer.writerow(row)
