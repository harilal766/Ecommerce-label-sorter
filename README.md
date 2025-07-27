# Ecom-label-sorter

## Description:
1. A python program to sort Amazon and Shopify pdf shipping labels.
2. Each sorted group of orders will be stored in a dedicated pdf file which is named after the product name and quantity.
3.  On Miscellaneous orders these pdf file will be named "Mixed".
4. All of these files will be stored inside a folder which is named after the input pdf file.

## Reason to develop this project
Manually sorting a large PDF containing multiple orders is time-consuming and prone to human error.

# Installation
```
pip install ecom_label_sorter
```

# Usage
```
from label_sorter import Label_sorter

sorter_instance = Label(pdf_path = <path to the pdf file>)

# Creating sorted pdf files
# this will create a folder named after the pdf file and will be containig sorted pdf files and summary json fle.
sorter_instance.created_sorted_pdf_files()

```




# Classes and their descriptions

[ Label Sorter](docs/Label_Sorter.md)