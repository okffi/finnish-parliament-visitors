# lobbyist-register
Finnish Parliament visitor register

## Description

This repo describes the process of digitalising the FOI responses from the Finnish Parliament visitor register.
The requests are currently replied to with printed copies of the original spreadsheets.

So to transform them to usable digital format, the are photographed periodically, and apply image processing, OCR, and pdf table extraction (Tabula) to get CSVs to be processed. These scripts are provided below.

## How

In short   
(1) ImageMagick (for cleaning ) 
(2) Tesseract ( for OCR to searchable PDFs )
(3) Tabula ( for PDF to csv )


## Script Documentation
Name folders as metnioned below and give as input the directory containing all those you want to process. To repeat process on only some mistaken files, copy them in a temporary 'fixing' folder and run the 2 scripts on that folder.

#### **processImages.sh**  
***Run***        :        ./processImages.sh   
***Depends On***: ImageMagick -> https://www.imagemagick.org   
***Exports***    : A folder called 'processed_photos' in each of the above where the images found are color balanced and rotated if they are portraits.    
                  
 ***Replies***    : Each subfolder has a 'processed_photos' with the results of the processing.

 -  If there is an issue with the name of the folder it gets renamed with a trailing '_'
 -  If the photo processed is in portrait it moves it clockwise (270deg arbitrary) it  adds a trailing 'check_' to the name
 - If the photos are upside down (landscape) you need to turn them manually.


#### **ocrImages.sh**  
 ***Run***       : ./ocrImages.sh   
 ***Depends On*** :   

 - *Tabula-Java* 
    A working .jar version is included but make sure you have java 1.7+. https://github.com/tabulapdf/tabula-java/releases

 - *Tesseract (3.05+)* with FIN, SWE language packages 
    In short `brew install tesseract` and `brew install tesseract-<langcode>`  
 https://github.com/tesseract-ocr/tesseract/ 

***Asks for***  : main folder of folders (full path) give the same as the one before!   

 ***Replies***    :    
 

 -  If there is no 'processed_photos' folder then it ignores it completely! Make sure the previous script worked..
 -  If the resulting CSV is total gibberish chanch is the file was not in correct reading orientation.. Turn the original photo.


## Current Data structure   

The above is optimised for the following data structure:


## Folder Structure
 
 These 2 scripts runs through all folders that have the following structure

           BuildingRegister#date#HadBeenExpected

*BuildingRegister* :   
There are two separate registers for different buildings
 (g or b) Blue folder is for the temporary use of the Sibelius Academy (b), Green folder for the parliament itself (g)            

*Date*:   
Date of the page register. This is hard to retrieve from individual pages (YYYY-MM-DD) and therefore has to be inputed in the folder as an extra metadata.

 *HadBeenExpected* :  
Register of people who had notified were coming “Ilmoittautuneet" (e) and register of people who had not notified “Ei ilmoittautuneet” (ne).
