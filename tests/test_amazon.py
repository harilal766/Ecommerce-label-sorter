from sorting_alrogithms.amazon import Amazon 
from test_project import *
import pdfplumber

amzn = Amazon()
class Test_Amazon:
    
    def test_find_amazon_page_type():
        qr_page = amzn_input_filepath
        
        with pdfplumber.open(amzn_input_filepath) as pdf:
            for page in pdf:
                page = page.extract_text()
                print(page)