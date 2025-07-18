import re
from regex_patterns import *
import pdfplumber
from sorting_alrogithms.shopify import Shopify

class Sort:
    def __init__(self,pdf_path,platform):
        self.summary_dict = {}
        self.input_filepath = pdf_path
        self.platform = platform
        
    def create_shipment_summary(self, sorting_key:str, summary_dict, page_nums:list, qty : str) -> None:
        try:
            # different conditions for mixed and single items
            # sorting key initialization
            # The line `if sorti` is incomplete and does not exist in the provided code snippet. It
            # seems like there might have been a typo or an incomplete statement. If you can provide
            # more context or clarify the specific line of code you are referring to, I would be
            # happy to help explain it.
            
            numbers_list = None
            # Adding sorting key if not present
            if sorting_key not in summary_dict.keys(): 
                summary_dict[sorting_key] = [] if sorting_key == "Mixed" else {}

            if sorting_key == "Mixed":
                numbers_list = summary_dict[sorting_key]
            else:
                if qty not in summary_dict[sorting_key].keys():
                    summary_dict[sorting_key][qty] = []
                numbers_list = summary_dict[sorting_key][qty]
            numbers_list += page_nums
            
        except Exception as e:
            print(e)
        
    def get_sorted_summary(self):
        title = None
        try:
            with pdfplumber.open(self.input_filepath) as pdf_file:
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    page_number = f"{page_index+1} : "
                    # Sanitizing platform input
                    if self.platform == "amazon":
                        self.sort_amazon_label(page_number,self.summary_dict,page_text, page_tables, page_index+1)
                    elif self.platform == "shopify":
                        #print(page_text,end="\n"+"-"*20+"\n")
                        self.sort_shopify_label(page_text=page_text,page_num=int(page_number.replace(" : ", "")))
                        
        except Exception as e:
            print(e)
        else:
            return self.summary_dict

    def sort_amazon_label(
        self,status:str,summary_dict: dict,
        page_text,page_tables, page_num:int) -> None:
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
                self.create_shipment_summary(
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
            
    def sort_shopify_label(self, page_text, page_num):
        try:
            #print(page_text)
            id_match = re.findall(r'(Order)\s(#\d{4,5})', page_text)
            
            prod_desc_match = re.findall(r'ITEMS QUANTITY\n(.*)\nThank you for shopping with us', page_text,flags=re.DOTALL)
            if id_match:
                order_id = id_match[0][-1]
            
            if prod_desc_match:
                matched = prod_desc_match[0]
                
                match_split = matched.split("\n")
                
                prod_qty = re.sub(r'\sof\s\d', r'',match_split[-2])
                prod_variation = match_split[-1]
                
                prodname = match_split[0] + match_split[2] if len(match_split) == 4 else match_split[0]
                
                print(match_split)
                print(f"{order_id} : {prodname}-{prod_variation}-{prod_qty}.")
                
                
                self.create_shipment_summary(
                    sorting_key=prodname, summary_dict=self.summary_dict,
                    page_nums=[page_num], qty=prod_qty
                )
                
        except Exception as e:
            print(e)
        else:
            pass
            
            
    