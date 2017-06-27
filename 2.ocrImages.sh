#! /bin/bash

    scriptFolder=$PWD

    echo Which folder \do you want to process?
    read parentFolder
    cd $parentFolder

#    needed?
#    mkdir -p 'CSV'

    # run this for every folder of dates..?
    for d in */; do

        fn=`echo $d|sed -e 's/\/$//'`
        echo 'Starting to process subfolder: '$d

        if [ "$d" = "CSV/" ]
          then
          continue;
        elif [ ! -d "$d/processed_photos/" ]
          then
          echo  $d': Ignoring folder (no processed_photos) '
          continue;
        fi

        echo "$d"
        cd "$d/processed_photos/"

          for i in *.jpg ; do
              tesseract $i $i -l fin+swe pdf
          done

          java -jar $scriptFolder/tabula-jar/tabula-0.9.2-jar-with-dependencies.jar -b $parentFolder/$d/processed_photos/

          cat *.csv > ../$fn.csv

#          for j in *.csv ; do
#            mv -f $j $parentFolder/csv/$j
#          done

        cd $parentFolder
    done
