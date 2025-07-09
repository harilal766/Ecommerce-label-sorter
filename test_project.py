from project import *
from sorting_algorithms import *
import json, os
"""
    Verify the pdf file exists
"""
with open("creds.json","r") as json_file:
    credentials = json.load(json_file)
    amzn_input_filepath = credentials["amazon_input_filepath"]
    out_dir = amzn_input_filepath.replace(".pdf", "")
    
def test_verify_directory():
    # Verify output directory exists
    assert os.path.isdir(out_dir)

def test_find_platform():
    platform = find_platform(pdf_path=amzn_input_filepath)
    assert platform == "Amazon"

def test_sort_amazon_label():
    """
    Send an amazon pdf file and verify it has invoice pages
    """
    pass

def test_create_shipment_summary():
    """
    assert the summary dict was empty
    run the script for shipping summary
    assert the summary dict is populated
    """
    pass

def test_create_pdf():
    """
    create sorted pdf files
    Verify a folder in the filename is created and it contains sorted pdf files
    """
    # Verify all the files in the dir is pdf
    pdf_list = os.listdir(out_dir)
    pdf_count = sum("pdf" == pdf.split(".")[-1] for pdf in pdf_list)
    assert pdf_count == len(pdf_list)
