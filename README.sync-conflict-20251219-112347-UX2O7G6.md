# Ecommerce Label Sorter

## Description:
1. A python program to sort Amazon and Shopify shipping labels based on the product name and quantity.
2. Each sorted group of orders will be stored in a dedicated output pdf file which is named after the product name and quantity.
3. Miscellaneous orders will be stored on a dedicated file named "Mixed".
4. All of these files will be stored inside a folder which is named after the input pdf file.

## Installation
```
pip install ecom_label_sorter
```

## Usage
```
from label_sorter import LabelSorter

# Initialize
sorter_instance = LabelSorter(pdf_path = <path to the pdf file>)

# begin sorting
sorter_instance.create_sorted_pdf_files()

# a new folder named after the input pdf file will be created and the output files will be stored inside it.
```