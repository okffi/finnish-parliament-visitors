# lobbyist-register
Finnish Parliament Visitor Logs

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
***Run***        :  bash 1.processImages.sh   
***Depends On***: ImageMagick -> https://www.imagemagick.org   
***Exports***    : A folder called 'processed_photos' in each of the above where the images found are color balanced and rotated if they are portraits.                      
***Replies***    : Each subfolder has a 'processed_photos' with the results of the processing.

 -  If there is an issue with the name of the folder it gets renamed with a trailing '_'
 -  If the photo processed is in portrait it moves it clockwise (270deg arbitrary) it  adds a trailing 'check_' to the name
 - If the photos are upside down (landscape) you need to turn them manually.


#### **ocrImages.sh**  
 ***Run***       : bash 2.ocrImages.sh   
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

#### **3.collate_csv.sh**  

 ***Run***       : bash 3.collate_csv.sh   
 ***Depends On*** :   

***Asks for***  : main folder of folders (full path) give the same as the one before!      
***Replies***    :  
 -  Runs through and collects all the individual csv files and puts them all together in a compiled csv file with individual ID for each row 

#### **4.test_all.sh**  

 ***Run***       : bash 4.test_all.sh   
 ***Depends On*** :   

***Asks for***  : main folder of folders (full path) give the same as the one before!      
***Replies***   :  
 - Runs a check of what the python file will fail to process. Gives an error message that needs to be handled manually
 - It will tell you the name of the csv file and the now nearby to look for. Yeah manual processing...


#### **5.post_ocr_all.sh**  

 ***Run***       : bash 5.post_ocr_all.sh   
 ***Depends On*** :   

***Asks for***  : main folder of folders (full path) give the same as the one before!      
***Replies***   :  
 - Runs the python file to correct basic structure and add full ID so that the row and original photograph where it was found are still searchable.
 


## Contact

(https://github.com/FourCoffees)
(https://github.com/AleksiKnuutila)


## Current Data structure   

The above is optimised for the following data structure:

For each date, there are two sets of pages. The first pages describe the people who the reception had been notified were coming (“Ilmoittautuneet”). The latter pages, starting again from the morning hours, list the people who had not been notified (“Ei ilmoittautuneet”). The second set of pages does not list the date. Hence it’s important to maintain the order of photographs and this is why we name them in the folders.
 
There are two separate registers for different buildings. These are filled in different folders, the green and the blue folder. The blue folder is for the temporary use of the Sibelius Academy building, and green folder for the parliament itself.
 
The administration removes certain information from the register before making it viewable. The only way they have described what they remove is by saying, it is for example the people who visit the Ombudsman (Oikeusasiamies).


## Folder Structure
 
 These 2 scripts runs through all folders that have the following structure

           BuildingRegister#date#Notified

*BuildingRegister* :   
There are two separate registers for different buildings
 (g or b) Blue folder is for the temporary use of the Sibelius Academy (b), Green folder for the parliament itself (g)            

*Date*:   
Date of the page register. This is hard to retrieve from individual pages (YYYY-MM-DD) and therefore has to be inputed in the folder as an extra metadata.

 *Notified* :  
Register of people who had notified were coming “Ilmoittautuneet" (e) and register of people who had not notified “Ei ilmoittautuneet” (ne).


## Results

The final output is a folder named CSV containing all the exported csvs. This will be created at the root of the folders. Each csv is named:

      Date#BuildingRegister#Notified#photo-id.csv
 
      2017-05-26#g#e#IMG_20170602_120608.jpg.csv


