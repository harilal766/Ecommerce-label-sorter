

class AmazonLabel:
    order_id_pattern = r'\d{3}-\d{7}-\d{7}'
    product_name_pattern = r'\|\s[A-Z\d]+\s\(\s[A-Z\d-]+\s\)(\s|\n)Shipping Charges'