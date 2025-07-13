from project import *
from sorting_algorithms import *
import json

with open("creds.json","r") as json_file:
    credentials = json.load(json_file)
    amzn_input_filepath = credentials["amazon_input_filepath"]
    non_existing_file = amzn_input_filepath.replace(".pdf",".py")
    out_dir = amzn_input_filepath.replace(".pdf", "")
    
def test_main():
    # the function should throw an error when presented with an invalid file
    assert main(input_dir=amzn_input_filepath)

def test_find_platform():
    assert find_platform(pdf_path=amzn_input_filepath) == 'Amazon'
    

