from project import *
import json, os
"""
    Verify the pdf file exists
"""
with open("creds.json","r") as json_file:
    credentials = json.load(json_file)
    
    input_filepath = credentials["input_filepath"]
    
    
def test_main():
    assert verify_directory(input_filepath) == True

def test_sort_amazon_label():
    pass

def test_create_shipment_summary():
    pass

def test_create_pdf():
    """
    create sorted pdf files
    Verify a folder in the filename is created and it contains sorted pdf files
    """
    test_dir = input_filepath.replace(".pdf", "")
    
    # verify output directory exists
    assert os.path.isdir(test_dir)
    
    # to verify all the files in the dir is pdf
    pdf_list = os.listdir(test_dir)
    assert sum(".pdf" in pdf for pdf in pdf_list) == 5

def test_verify_directory():
    pass

#print(os.listdir(input_filepath.replace(".pdf","")))