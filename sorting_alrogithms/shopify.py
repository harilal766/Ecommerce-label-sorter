import re

class Shopify:
    def __init__(self):
        self.id_pattern = r'Order #\d{4,5}'
        self.prod_name_pattern = r'(ITEMS QUANTITY\n)([a-zA-Z\s]*\n)(\d of \d\n)(\d{3,4}\sGM|ML)'
        
    def sort_shopify_label(self, page_text):
        try:
            id_match = re.findall(self.id_pattern, page_text)
            prod_desc_match = re.findall(self.prod_name_pattern, page_text)
            if id_match:
                order_id = id_match[0]
            
            if prod_desc_match:
                matched = prod_desc_match[0]
                
                prodname = matched[1].replace("\n", "")
                prod_qty = matched[2].replace("\n", "")
                prod_variation = matched[-1].replace("\n", "")
                
                print(f"{prodname} {prod_variation} - {prod_qty}")
                
            #print(page_text)
                
        except Exception as e:
            print(e)
        else:
            pass