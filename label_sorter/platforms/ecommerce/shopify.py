import re

class ShopifyLabel:
    def __init__(self):
        self.order_id_pattern = r'#\d{4,5}'
        self.product_name_pattern = r'ITEMS QUANTITY\n(.*)\nThank you for shopping with us'
        self.qty_pattern = r'(\d+)\sof\s\d+'
        
        # Common 
        self.page_debrief_dict = {
            "order_id" : None, "sorting_key" : None, "qty" : None
        }
    
    def analyze_shopify_page(self, label_text, page_num):
        try:
            #print(page_text)
            id_match = re.findall(self.order_id_pattern, label_text)
            
            prod_desc_match = re.findall(self.product_name_pattern, label_text,flags=re.DOTALL)
            if id_match:
                self.page_debrief_dict["order_id"] = id_match[0]
            
            if prod_desc_match:
                # find the product name in string form
                prod_desc_str = prod_desc_match[0].replace("\n"," ")
                
                # check it the order is mixed
                item_count = len(re.findall(self.qty_pattern,prod_desc_str))
                    
                if item_count == 1:
                    self.page_debrief_dict["qty"] = re.search(self.qty_pattern, prod_desc_str).group(1)
                    self.page_debrief_dict["sorting_key"] = re.sub(self.qty_pattern,'',prod_desc_str)
                else:
                    self.page_debrief_dict["sorting_key"] = "Mixed"
                    
                return self.page_debrief_dict
        except Exception as e:
            print(e)
        else:
            pass
    