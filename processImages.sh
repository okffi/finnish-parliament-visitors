#! /bin/bash
 
# This script runs through all folders that have the following structure
#
#           BuildingRegister#date#HadBeenExpected

# BuildingRegister : There are two separate registers for different buildings
# (g or b)          Blue folder is for the temporary use of the Sibelius Academy -> b
#                   Green folder for the parliament itself  -> g            

# Date            : Date of the page register. This is hard to retrieve from individual pages
# (YYYY-MM-DD)     and therefore has to be inputed in the folder as an extra metadata.

# HadBeenExpected : Register of people who had notified were coming (“Ilmoittautuneet”) -> e
#  (ne or e)       Register of people who had not been notified (“Ei ilmoittautuneet”) -> ne
#


# Exports: A folder called 'processed_photos' in each of the above where the 
# images found are color balanced and rotated if they are portraits. 

# *** The rotation is not guaranteed since it is but default clockwise ** 
# *** But the files have a check_ tag so it is enough to look at them to see if they 
# *** are readable.

# Run with ./cleanLobbyPhotos and input the folder to process
# errors appear with '_' in front of the erronous folder names
  
    echo Which folder \do you want to process?
    read parentFolder
    cd $parentFolder

    # parentFolder=$PWD
    echo $parentFolder

    page_id=1
    dir_id=1

    # run this for every folder
    for d in */; do

        # echo "$d"
        cd $d

        #get the name of the current directory which contains metadata on the information
        currentDir=${PWD##*/} 
        echo "Trying to process folder: " $currentDir

        IFS='#' read -r -a params <<< "$currentDir"

        BuildingRegister=${params[0]} # folder g or b
        Date=${params[1]} # date YYYY-MM-DD 
        HadBeenExpected=${params[2]}  # ne or e expected or not

        # echo $BuildingRegister
        # echo $Date
        # echo "$HadBeenExpected"

        if [[ -z "$HadBeenExpected" ]]
        then
            echo $currentDir' is missing HadBeenExpected param .. skipping..'
            mv "$parentFolder/$d" "$parentFolder/_$d"
        elif [[  -z "$Date" ]]; then
            echo $currentDir' is missing Date param .. skipping..'
            mv "$parentFolder/$d" "$parentFolder/_$d"
        elif [[  -z "$BuildingRegister" ]]; then
            echo $currentDir' is missing BuildingRegister param .. skipping..'
            mv "$parentFolder/$d" "$parentFolder/_$d"
        else 
            mkdir -p processed_photos

            for img in *.jpg ; do
                identify=$(identify "$img")
                [[ $identify =~ ([0-9]+)x([0-9]+) ]] || \
                    { echo Cannot get size >&2 ; continue ; }
                width=${BASH_REMATCH[1]}
                height=${BASH_REMATCH[2]}

                # Generate new name for the image file
                rr="${Date}#${BuildingRegister}#${HadBeenExpected}#$dir_id-$page_id.jpg"
                echo $rr
                page_id=$((page_id+1))

                # Convert the quality so deep shadows leave
                convert $img \
                     \( +clone -blur 0x20 \) \
                     -compose Divide_Src -composite $rr

                # move it to new folder
                mv -f -i "$parentFolder/$d/$rr" "$parentFolder/$d/processed_photos/"

                # Check if it needs to be rotated
                if (( width < height )) ; then
                    echo "$img is portrait, turning it clockwise but check it "
                     rr_rot="check_$rr"
                     convert "$parentFolder/$d/processed_photos/$rr" -rotate 270 "$parentFolder/$d/processed_photos/$rr"  
                     
                     mv -f -i "$parentFolder/$d/processed_photos/$rr" "$parentFolder/$d/processed_photos/$rr_rot"

                fi
            done
        fi

        cd $parentFolder
        dir_id=$((dir_id+1))
    done
    # IMAGE PROCESSING FINISHED NOW TO OCR STUFF
