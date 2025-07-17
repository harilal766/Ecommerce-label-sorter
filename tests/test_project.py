from project import *
from sorting_alrogithms.sorting_algorithms import *
from credentials import amzn_input_filepath, non_existing_file, out_dir
import json



def test_main():
    # the function should throw an error when presented with an invalid file
    assert main(input_dir=amzn_input_filepath)

def test_find_platform():
    assert find_platform(pdf_path=amzn_input_filepath) == 'Amazon'
    
def test_get_filepath():
    assert get_filepath() == None

