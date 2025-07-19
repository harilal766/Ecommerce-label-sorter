import pdfplumber, re

# Inside the project
from label_sorter.platforms.ecommerce.shopify import ShopifyLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel

ORDER_ID_PATTERNS = {
    'amazon' : AmazonLabel.order_id_pattern,
    'shopify' : ShopifyLabel.order_id_pattern
}

PRODUCT_NAME_PATTERNS = {
    'shopify' : ''
}

def find_platform(pdf_path : str) -> str:
    platform = None
    try:
        with pdfplumber.open(pdf_path) as pdf_file:
            total_pages = 0; amazon_count = 0 
            
            shopify_order_id_count, amazon_order_id_count = 0, 0
            
            for page_index, page in enumerate(pdf_file.pages):
                total_pages += 1
                page_text = page.extract_text(); page_tables = page.extract_tables()
                
                # Shopify Initializations
                if re.findall(ShopifyLabel.order_id_pattern, page_text):
                    shopify_order_id_count += 1
                elif re.findall(AmazonLabel.order_id_pattern, page_text):
                    amazon_order_id_count += 1
                    
                
            if total_pages == shopify_order_id_count:
                platform = "Shopify"
            # this condition is not complete, need to add overlap page detection
            elif total_pages/2 == amazon_order_id_count:
                platform == "Amazon"
        
    except Exception as e:
        print(e)
    else:
        return platform