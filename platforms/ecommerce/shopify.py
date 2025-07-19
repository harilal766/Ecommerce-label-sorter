import re

class ShopifyLabel:
    order_id_pattern = r'(Order)\s(#\d{4,5})'
    product_name_pattern = r'ITEMS QUANTITY\n(.*)\nThank you for shopping with us'
    
    def sort_label(self, page_text, page_num):
        try:
            #print(page_text)
            id_match = re.findall(r'(Order)\s(#\d{4,5})', page_text)
            
            prod_desc_match = re.findall(self.product_name_pattern, page_text,flags=re.DOTALL)
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
    