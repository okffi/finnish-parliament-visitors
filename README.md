# lobbyist-register
Finnish Parliament visitor register

## Description

This repo describes the process of digitalising the FOI responses from the Finnish Parliament visitor register.
The requests are currently replied to with printed copies of the original spreadsheets.

So to transform them to usable digital format, the are photographed periodically, and apply image processing, OCR, and pdf table extraction (Tabula) to get CSVs to be processed. These scripts are provided below.

## How

In short (1) ImageMagick (for cleaning ) (2) Tesseract ( for OCR to searchable PDFs ) (3) Tabula ( for PDF to csv )


## Script Documentation

- processImages  
 *Depends On* : ImageMagick -> https://www.imagemagick.org
 *Run*        :     ./cleanLobbyPhotos
 *Asks for*   : main folder of folders (full path)
 *Exports*    : A folder called 'processed_photos' in each of the above where the 
                  images found are color balanced and rotated if they are portraits. 
 *Replies*    : Each subfolder has a 'processed_photos' with the results of the procesing
                * If there is an issue with the name of the folder: 
                    -> it gets renamed with a trailing '_'
                * If the photo processed is in portrait it moves it clockwise (270deg)
                   -> this is arbitrary so it also adds a trailing 'check_' to the name
                * If the photos are upside down (landscape) you need to turn them manually.


- ocrImages
 *Depends On* : Tabula-Java -> a working .jar version is included but make sure you have java 1.7+
                https://github.com/tabulapdf/tabula-java/releases

                Tesseract (3.05+) with FIN, SWE language packages,   
                in short *brew install tesseract* and *brew install tesseract-<langcode>*
                https://github.com/tesseract-ocr/tesseract/ 
 *Run*        : ./jpgToCsv
 *Asks for*   : main folder of folders (full path) give the same as the one before!
 *Exports*    : A common folder named 'CSV' with all the exported csv from the processed photos
 *Replies*    : * If there is no 'processed_photos' folder 
                   -> then it ignores it completely! so make sure its ok cause you ll miss files.
                * If the resulting CSV is total gibberish chanche is the file was not in reading direction...
                   -> turn the original photo, put the folders in a 'fixing' folder and run the 2 scripts on that folder.


## Current Data structure 

The above is optimsed for the following data structure:


## Folder Structure
 
 These 2 scripts runs through all folders that have the following structure

           BuildingRegister#date#HadBeenExpected

 BuildingRegister : There are two separate registers for different buildings
 (g or b)          Blue folder is for the temporary use of the Sibelius Academy -> b
                   Green folder for the parliament itself  -> g            

 Date            : Date of the page register. This is hard to retrieve from individual pages
(YYYY-MM-DD)     and therefore has to be inputed in the folder as an extra metadata.

 HadBeenExpected : Register of people who had notified were coming (“Ilmoittautuneet”) -> e
 (ne or e)       Register of people who had not been notified (“Ei ilmoittautuneet”) -> ne
