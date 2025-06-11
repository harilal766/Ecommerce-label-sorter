from PyPDF2 import PdfReader
import pdfplumber
import pandas as pd
import json, re

from regex_patterns import amazon_order_id_pattern


def main():
    """
    read a pdf file and detect the shipment type eg : amazon, shopify etc
    """
    
    summary_dict = {
        "Mixed" : []
    }
    try:
        with open('creds.json') as json_file:
            json_dict = json.load(json_file)
            input_dir = json_dict["input"]
            output_dir = json_dict["output"]
        platform = "Amazon "
        summary = 0
        
        with pdfplumber.open(input_dir) as pdf_file:
            for page_index, page in enumerate(pdf_file.pages):
                page_text = page.extract_text(); page_tables = page.extract_tables()
                
                page_status = f"Page {page_index+1} : "
                
                sorting = {
                    "amazon" : amazon_sorter(
                        status=page_status, summary_dict = summary_dict,
                        page_text = page_text, page_tables=page_tables, 
                        page_num = page_index + 1
                    ),
                }
                
                platform = platform.strip().lower()
                if platform in sorting.keys():
                    summary = sorting[platform]
                else:
                    print("Unsupported platform")
                    
    except Exception as e:
        print(f"00 {e}")
    else:
        print(summary)
        return summary
        
        
        
        
def amazon_sorter(status:str,summary_dict: dict,page_text,page_tables, page_num:int):
    try:
        # start of amazon function in the future
        order_id_match = re.findall(amazon_order_id_pattern,page_text)
        # Ensuring invoice pages
        if order_id_match:
            status += "Invoice page, "
            if len(page_tables) > 1:
                # Products table
                products_table = page_tables[0]
                products_rows = products_table[:-3]
                                
                item_count = len(products_rows)-1
                            
                if len(products_rows) > 2:
                    status += f"Mixed orders, count : {item_count}."
                    summary_dict["Mixed"] += [page_num-1, page_num]
                    
                else:      
                    product_name_match = re.search(r'(\(\s[A-Z0-9-]+\s\))',products_rows[-1][1])
                    product_name = product_name_match
                    product_qty = products_rows[-1][3]
                    page_status += "Single item order." 
                    print(product_name_match, product_qty)
        else:
            if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',page_text):
                status += "Overlapping page."
            else:
                status += "Qr code page."
                        
            print(status, end = "," if "Qr code page." in status else None)
    except Exception as e:
        print(e)     
        
        
        
                        

if __name__ == "__main__":
    main()