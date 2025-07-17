from sorting_alrogithms.amazon import Amazon 
import pdfplumber, json

from credentials import amzn_input_filepath, non_existing_file, out_dir

amzn = Amazon()
class Test_Amazon:
    
    def test_find_amazon_page_type():
        with pdfplumber.open(amzn_input_filepath) as pdf:
            for page in pdf:
                page = page.extract_text()
                print(page)