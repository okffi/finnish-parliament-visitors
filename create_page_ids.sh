dir_id=1
page_id=1

for dir in *; do
  cd $dir
  # jpg?
  for file in *csv; do
    currentDir=${PWD##*/}

    IFS='#' read -r -a params <<< "$currentDir"

    BuildingRegister=${params[0]} # folder g or b
    Date=${params[1]} # date YYYY-MM-DD
    HadBeenExpected=${params[2]}  # ne or e expected or not

    echo "mv $file $BuildingRegister#$Date#$HadBeenExpected#$dir_id-$page_id".csv
    page_id=$((page_id+1))
  done
  cd ..
  dir_id=$((dir_id+1))
  page_id=1
done
