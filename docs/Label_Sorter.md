# LabelSorter Class
### Location : [core.py](label_sorter/core.py)
## Attributes
Sorting dictionary : to store the sorted data i.e; product name, quantity, and page numbers.
label filepath : path of the input pdf file
output folder : name of the folder to store sorted pdf files, created by replacing the `.pdf` extension with empty string
platform : platform of the pdf label eg : Amazon, Shopify etc...


# Technical Terms to Remember
Sorting key :
Platform : 

## Methods
### Find platform
Loops through each page of the pdf file, counts order id occurences of each  platforms.
After the loop is exited, the total page count and counts of these orders ids are compared,
based on these conditions.
1. if shopify order ids are same as that of page counts, the pdf belongs to shopify.
2. if amazon order id is present, its amazon.

### Sort labels
Loops the pages, and activates the sorting algorithm based on the platform, the dictionary returned from it contains order id, product name and quantity of each page, it is used to create the sorting dictionary

### Populate shipment summary
Accepts sorting key and page numbers list as arguments
1. if the sorting key == "Mixed", quantity will not be provided
    it will be created as the key in the dict if not already present,
    if already present, it will add the page numbers to its value which is a list
2. if the sorting key is a product name, 
    quantity will be provided and the product name and quantity will be provided as the main key and sub dict key if not already present,
    if already present, page numbers of the orders contains the product and the qty will be given

### Create sorted pdf files
after the sorting dict is finished, this function will loop through the main sorted dictionary and the sub dictionaries inside it and creates sorted pdf files.    

### Create single pdf file
creates a single pdf file based on the output folder, product name and its sorted page nums,
this function will be used inside a loop to create sorted pdfs for all the details in the sorted dictionary.


# Potential bugs
while dealing with Delhivery, Bluedart etc, if their api integrations are done with shopify, these labels will have shopify order id, which will make the program think its handling with shopify and execute its algorithm.

amazon platform detection needs more tight logic in the future.