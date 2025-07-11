import re
from regex_patterns import *
import pdfplumber

class Sort:
    def __init__(self,pdf_path,platform):
        self.summary_dict = {}
        self.input_filepath = pdf_path
        self.platform = platform
        
    def get_sorted_summary(self):
        title = None
        try:
            with pdfplumber.open(self.input_filepath) as pdf_file:
                title = "PAGE INFO"
                print(f"\n{title}\n{"-"*len(title)}")
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    page_number = f"{page_index+1} : "
                    # Sanitizing platform input
                    if self.platform == "amazon":
                        self.sort_amazon_label(page_number,self.summary_dict,page_text, page_tables, page_index+1)
        except Exception as e:
            print(e)
        else:
            return self.summary_dict

    def sort_amazon_label(
        self,status:str,summary_dict: dict,
        page_text,page_tables, page_num:int) -> None:
        sorting_key = None
        from project import create_shipment_summary
        try:
            # start of amazon function in the future
            order_id_match = re.findall(amazon_order_id_pattern,page_text)
            # Ensuring invoice pages
            if order_id_match:
                status += "Invoice page, "
                products_table = page_tables[0]
                products_rows = products_table[:-3]
                                    
                item_count = len(products_rows)-1
                product_qty = None
                # Deciding order type by reading the product table and types of items
                if len(products_rows) > 2:
                    status += f"Mixed orders, count : {item_count}."                
                    sorting_key = "Mixed"
                else:
                    status += "Single item order."
                    product_description = products_rows[-1][1] 
                    product_name_match = re.sub(
                        amazon_name_regex,"",product_description, flags = re.IGNORECASE
                    )
                    product_qty = products_rows[-1][3]
                    #sorting_key = f"{product_name_match.replace("\n"," ")} - {product_qty} qty"
                    sorting_key = product_name_match.replace("\n"," ")
                        
                # populating summary dict based on the order condition
                create_shipment_summary(
                    sorting_key = sorting_key, summary_dict = summary_dict, 
                    page_nums = [page_num-1, page_num], qty = product_qty
                )
                
            # Handling QR code and Overlapping page
            else:
                if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',page_text):
                    status += "Overlapping page."
                else:
                    status += "Qr code page"
                            
            print(status, end = ", " if "Qr code page" in status else None)
        except Exception as e:
            print(e)