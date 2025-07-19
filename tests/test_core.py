from filepaths import amazon_pdf, shopify_pdf
from core import LabelSorter

def test_find_platfrom():
    inst = LabelSorter()
    assert inst.find_platform(pdf_path=shopify_pdf) == "Shopify"
    assert inst.find_platform(pdf_path=amazon_pdf) != "Shopify"
    
"""
class Test_LabelSorter:
    inst = LabelSorter(pdf_path=amazon_pdf)
    
    assert inst.sorted_dict == {}
"""    