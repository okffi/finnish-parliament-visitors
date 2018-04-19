#! /bin/bash

scriptFolder=$PWD

echo Which folder \do you want to process?
read parentFolder
cd $parentFolder

echo $parentFolder

#find . -name \*.compiled.csv | while read fn; do
ls */*.compiled.csv | while read fn; do
  target_file=`echo $fn|sed -e 's/compiled.csv/processed.csv/'`
  echo target $target_file
  python $scriptFolder/post-ocr.py $fn > $target_file
done
