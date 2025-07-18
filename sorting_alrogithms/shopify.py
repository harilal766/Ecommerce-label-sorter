import re


class Shopify:
    def __init__(self):
        self.id_pattern = r'(Order)\s(#\d{4,5})'
        self.prod_name_pattern = r'(ITEMS QUANTITY\n)([a-zA-Z\s]*\n)(\d of \d\n)(\d{3,4}\sGM|ML)'
        
    def sort_shopify_label(self, filepath, page_text, page_num):
        try:
            id_match = re.findall(self.id_pattern, page_text)
            prod_desc_match = re.findall(self.prod_name_pattern, page_text)
            if id_match:
                order_id = id_match[0][-1]
            
            if prod_desc_match:
                matched = prod_desc_match[0]
                
                prodname = matched[1].replace("\n", "")
                prod_variation = matched[-1].replace("\n", "")
                
                prod_qty = matched[2].replace("\n", "")
                prod_qty = re.sub(r'\sof\s\d',r'',prod_qty)
                
                print(f"{order_id} : {prodname} {prod_variation} - {prod_qty}")
                
            si = Sort(pdf_path=filepath, platform="Shopify")
            si.create_shipment_summary(
                sorting_key=f"{prodname} {prod_variation}", summary_dict={},
                page_nums=[page_num]
            )
            #print(page_text)
                
        except Exception as e:
            print(e)
        else:
            pass