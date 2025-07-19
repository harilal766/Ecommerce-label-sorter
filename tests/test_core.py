import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from filepaths import amazon_pdf, shopify_pdf
from label_sorter.core import LabelSorter

def test_find_platfrom():
    inst = LabelSorter()
    assert inst.find_platform(pdf_path=shopify_pdf)
    #assert inst.find_platform(pdf_path=amazon_pdf) != "Shopify"
    

class Test_LabelSorter:
    inst = LabelSorter()
    
    assert inst.sorted_dict == {}
    
    
    