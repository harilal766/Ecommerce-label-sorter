from PyPDF2 import PdfReader
import pdfplumber, json, re
import pandas as pd
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
                
                page_status = f"{page_index+1} : "
                
                sorting = {
                    "amazon" : amazon_sorter(page_status,summary_dict,page_text, page_tables, page_index+1),
                }
                
                platform = platform.strip().lower()
                if platform in sorting.keys():
                    sorting[platform]
                else:
                    print("Unsupported platform")
                    
    except Exception as e:
        print(e)
    else:
        print(summary_dict)
        return summary_dict
        
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
                    amazon_name = r'([a-zA-Z0-9|\n\s]+)\s\|\s|\n([A-Z0-9]+\s\(\s[A-Z0-9-]+\s\))'    
                    product_name_match = re.search(amazon_name,products_rows[-1][1])
                    product_name = product_name_match.group(1)
                    product_qty = products_rows[-1][3]
                    
                    sorting_key = f"{product_name} - {product_qty} qty"
                    
                    if sorting_key not in summary_dict.keys():
                        summary_dict[sorting_key] = []
                    
                    summary_dict[sorting_key] += [page_num-1, page_num]
                        
                    status += "Single item order." 
                    print(product_name)
        else:
            if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',page_text):
                status += "Overlapping page."
            else:
                status += "Qr code page."
                        
            #print(status, end = "," if "Qr code page." in status else None)
    except Exception as e:
        print(e)     

def create_pdf(output_directory:str):
    try:
        pass
    except Exception as e:
        pass

if __name__ == "__main__":
    main()