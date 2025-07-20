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
            if re.findall(self.amazon_order_id_pattern,self.page_text):
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
            # Ensuring invoice pages
            if self.find_amazon_page_type() == "Invoice":
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
                        
        except Exception as e:
            print(e)