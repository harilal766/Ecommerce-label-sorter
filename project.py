from PyPDF2 import PdfReader
import pdfplumber
import pandas as pd
import json, re

from regex_patterns import amazon_order_id_pattern



def main():
    """
    read a pdf file and detect the shipment type eg : amazon, shopify etc
    """
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
                
                if platform.strip().lower() == 'amazon':
                    
                    # start of amazon function in the future
                    order_id_match = re.findall(amazon_order_id_pattern,page_text)
                    # Ensuring invoice pages
                    
                    page_status = f"Page {page_index+1}. "
                    if order_id_match:
                        if len(page_tables) > 1:
                            page_status += "Invoice page, "
                            # Products table
                            products_table = page_tables[0]
                            products_rows = products_table[:-3]
                                
                            item_count = len(products_rows)-1
                            if len(products_rows) > 2:
                                page_status += f"Mixed orders, count : {item_count}."
                            else:
                                page_status += "Single item order."       
                    else:
                        if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',page_text):
                            page_status += "Overlapping page."
                        else:
                            page_status += "Qr code page."
                        
                    print(page_status, end = ", " if "Qr code page." in page_status else None)
                                    
                    
    except Exception as e:
        print(e)
    else:
        return summary
        
def amazon_sorter():
    pass

if __name__ == "__main__":
    main()