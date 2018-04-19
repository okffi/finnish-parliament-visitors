#! /bin/bash

    scriptFolder=$PWD

    echo Which folder \do you want to process?
    read parentFolder
    cd $parentFolder

    # run this for every folder of dates..?
    for d in */; do

        echo 'Starting to process subfolder: '$d

        if [ "$d" = "CSV/" ]
          then
          continue;
        elif [ ! -d "$d/processed_photos/" ]
          then
          echo  $d': Ignoring folder (no processed_photos) '
          continue;
        fi

        cd "$d/processed_photos/"

          target_file=../`echo $d|sed -e 's/\/$//'`.compiled.csv

          for csvfn in *.csv; do
            page_id=`echo $csvfn | cut -d. -f 1 | cut -d# -f 4`
            cat $csvfn | while read line ; do
              echo $page_id,$line
            done
          done > $target_file

#          for j in *.csv ; do
#            mv -f $j $parentFolder/csv/$j
#          done

        cd $parentFolder
    done