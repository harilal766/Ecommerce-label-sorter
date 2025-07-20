import re
from .base_label import BaseLabel



class AmazonLabel(BaseLabel):
    def __init__(self, page_text, page_table):
        super().__init__(page_text, page_table)
        self.amazon_order_id_pattern = r'\d{3}-\d{7}-\d{7}'
        self.amazon_product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)Shipping Charges'
    
    def find_amazon_page_type(self):
        type = None
        try:
            order_id_match = re.findall(self.amazon_order_id_pattern,self.page_text)
            if order_id_match:
                type = "Invoice"
            else:
                if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',self.page_text):
                    type = "Overlap"
                else:
                    type = "Shipping Label"
            
        except Exception as e:
            print(e)
        else:
            return type
    
    def analyze_amazon_page(
        self,status:str,summary_dict: dict,
        page_text,page_tables, page_num:int) -> None:
        sorting_key = None
        try:
            # start of amazon function in the future
            order_id_match = re.findall(self.amazon_order_id_pattern,page_text)
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
                        self.amazon_product_name_pattern,"",product_description, flags = re.IGNORECASE
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