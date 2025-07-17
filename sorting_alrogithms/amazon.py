import re

class Amazon:
    def __init__(self):
        self.order_id_pattern = r'\d{3}-\d{7}-\d{7}'
        self.prodname_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)Shipping Charges'
        
    def find_amazon_page_type(self, page_text):
        type = None
        try:
            order_id_match = re.findall(self.order_id_pattern,page_text)
            if order_id_match:
                type = "Invoice"
            else:
                if re.findall(r'^Tax Invoice/Bill of Supply/Cash Memo',page_text):
                    status += "Overlap"
                else:
                    status += "Shipping Label"            
        except Exception as e:
            print(e)
        else:
            return type
        
        