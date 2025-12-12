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

## Methods and their working logic
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
1. if the sorting key == "Mixed", a nested dictionary which have the keys pages and summary, 
    pages contains a list that contains the page numbers and summary will contain product names and
    quantites of the mixed section.
2. if the sorting key is a product name, 
    product name and quantity will be provided as the main key and nested dictionaries inside it which contains the quantity and respective page numbers.

### Create sorted pdf files
after the sorted summary dict is generated, this function will use a nested loop to analyze it and will generate the pdf file based on the page numbers list.    

### Create single pdf file
creates a single pdf file based on the output folder, product name and its sorted page nums,
this function will be used inside a loop to create sorted pdfs for all the details in the sorted dictionary.


# Potential bugs
while dealing with Delhivery, Bluedart etc, if their api integrations are done with shopify, these labels will have shopify order id, which will make the program think its handling with shopify and execute its algorithm.

amazon platform detection needs more tight logic in the future.