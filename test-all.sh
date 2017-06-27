#! /bin/bash

scriptFolder=$PWD

echo Which folder \do you want to process?
read parentFolder
cd $parentFolder


find . -name \*.csv | while read fn; do
  python $scriptFolder/test-csv.py $fn | while read fn2; do
    basename=`basename $fn2`
    dirname=`dirname $fn2`
    newname="check_$basename"
    echo mv "$fn2" "$dirname/$newname"
  done
done
