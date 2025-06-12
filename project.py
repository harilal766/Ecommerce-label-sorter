from PyPDF2 import PdfReader
import pdfplumber, json, re
import pandas as pd
from regex_patterns import *

with open('creds.json') as json_file:
    json_dict = json.load(json_file)
    input_dir = json_dict["input"]
    output_dir = json_dict["output"]
            
def main():
    """
    read a pdf file and detect the shipment type eg : amazon, shopify etc
    """
    
    summary_dict = {}
    try:
        platform = "Amazon "
        summary = 0
        
        with pdfplumber.open(input_dir) as pdf_file:
            for page_index, page in enumerate(pdf_file.pages):
                page_text = page.extract_text(); page_tables = page.extract_tables()
                
                page_status = f"{page_index+1} : "
                
                sorting = {
                    "amazon" : sort_amazon_label(page_status,summary_dict,page_text, page_tables, page_index+1),
                }
                
                platform = platform.strip().lower()
                if platform in sorting.keys():
                    sorting[platform]
                else:
                    print("Unsupported platform")
                    
    except AttributeError:
        print("Attribute issues at the regex matching.")
    except Exception as e:
        print(e)
    else:
        print(summary_dict)
        return summary_dict
        
def sort_amazon_label(status:str,summary_dict: dict,page_text,page_tables, page_num:int):
    sorting_key = None
    try:
        # start of amazon function in the future
        order_id_match = re.findall(amazon_order_id_pattern,page_text)
        # Ensuring invoice pages
        if order_id_match:
            status += "Invoice page, "
            products_table = page_tables[0]
            products_rows = products_table[:-3]
                                
            item_count = len(products_rows)-1
                            
            # Deciding order type by reading the product table and types of items
            if len(products_rows) > 2:
                status += f"Mixed orders, count : {item_count}."                
                sorting_key = "Mixed"
            else:
                status += "Single item order."
                product_description = products_rows[-1][1] 
                product_name_match = re.sub(
                    amazon_name_regex,"",product_description,re.IGNORECASE
                )
                product_qty = products_rows[-1][3]
                sorting_key = f"{product_name_match.replace("\n"," ")} - {product_qty} qty"
                    
            # populating summary dict based on the order condition
            if sorting_key not in summary_dict.keys():
                summary_dict[sorting_key] = []    
            summary_dict[sorting_key] += [page_num-1, page_num]
        # Handling QR code and Overlapping page
        else:
            if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',page_text):
                status += "Overlapping page."
            else:
                status += "Qr code page"
                        
        print(status, end = ", " if "Qr code page" in status else None)
    except Exception as e:
        print(e)

def create_shipment_summary():
    try:
        pass
    except Exception as e:
        print(e)
    else:
        pass

def create_pdf(input_pdf_dir: str, page_nums: list, output_directory:str):
    try:
        # verify the pdf file exists
        # Verify the page contains something
        
        pass
    except Exception as e:
        pass

def verify_directory():
    try:
        pass
    except:
        pass
    else:
        pass

if __name__ == "__main__":
    main()