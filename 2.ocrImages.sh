#! /bin/bash

    scriptFolder=$PWD

    echo Which folder \do you want to process?
    read parentFolder
    cd $parentFolder

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

          # Use tesseract to extract fin and swe text
          for i in *.jpg ; do
              tesseract $i $i -l fin+swe pdf
          done

          # Run tabula to export a tabular (table) style file as csv
          java -jar $scriptFolder/tabula-jar/tabula-0.9.2-jar-with-dependencies.jar -b $parentFolder/$d/processed_photos/

          cat *.csv > ../$fn.csv

        cd $parentFolder
    done
