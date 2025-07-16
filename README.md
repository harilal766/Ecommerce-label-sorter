# Ecommerce-label-sorter

#### Video Demo:  https://youtu.be/M-e7C4bOUvY

## Description:
A python program to sort Amazon pdf shipping labels.
Each sorted group of orders will be stored in a dedicated pdf file which is named after the product name and quantity.
On Miscellaneous orders these pdf file will be named "Mixed".
All of these files will be stored inside a folder which is named after the input pdf file.

## Reason to develop this project
Each order in the PDF consists of two pages: the first page is the shipping label, and the second page is the invoice.
Manually sorting a large PDF containing thes kind of multiple orders is time-consuming and prone to human error.

## Operating procedure
1. Enter the filepath including the pdf file.
2. Make sure the filepath is correct, or the program    will reprompt.
3. The program will display each page number, page type and orders type (single item order/ Mixed order and the item count) of the pages it is going through and sorting.
4. After the sorting is completed, a sorted summary will be displated.

## Source code walkthrough
This program takes the filepath of the pdf file, checks each page of it using a for loop and add page numbers of the invoice and qr code page of each order to the sorting dictionary to a dedicated list which has its product name as the main dictionary amd its qty as the sub dictionary, for orders that contains multiple items, the numbers will go to a list of the key Mixed.
After the loop is finished running another nested loop will iterate this dict and create dedicated pdf files for the sorted orders based on the order name, all these files will be stored in a folder which has the input pdf name, and the qty of items and total order count will be noted on ybe output filename.

