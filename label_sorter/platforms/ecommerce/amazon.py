import re
from .base_label import BaseLabel

class AmazonLabel(BaseLabel):
    def __init__(self, page_text, page_table,page_num):
        super().__init__(page_text, page_table,page_num)
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
    
    def analyze_amzn_page(self) -> dict:
        try:
            # start of amazon function in the future
            # Ensuring invoice pages
            order_id_match = re.findall(self.amazon_order_id_pattern,self.page_text)
            if self.find_amazon_page_type() == "Invoice":
                self.page_debrief_dict["order_id"] = order_id_match[0]
                
                product_table = self.page_table[0]
                product_rows = product_table[1:-3]
                for row in product_rows:
                        prod_name = row[1].replace("\n",""); qty = row[3]
                        page_dict = {"item_name" : prod_name, "qty" : qty}
                        
                        if page_dict["item_name"] != None:
                            self.page_debrief_dict["items"].append(page_dict)
                print(self.page_debrief_dict)
                """
                # Deciding order type by reading the product table and types of items
                if len(product_rows) > 2:
                    print(product_rows)
                    self.page_debrief_dict["sorting_key"] = "Mixed"
                else:
                    product_description = product_rows[-1][1] 
                    product_name_match = re.sub(
                        self.amazon_product_name_pattern,"",product_description, flags = re.IGNORECASE
                    )
                    self.page_debrief_dict["qty"] = product_rows[-1][3]
                    self.page_debrief_dict["sorting_key"] = product_name_match.replace("\n"," ")
                """
        except Exception as e:
            print(e)
            
        else:
            return self.page_debrief_dict