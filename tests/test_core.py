from filepaths import amazon_pdf, shopify_pdf
from label_sorter.platform_detector import find_platform 
from label_sorter.core import LabelSorter


def test_find_platfrom():
    assert find_platform(pdf_path=shopify_pdf) == "Shopify"
    assert find_platform(pdf_path=amazon_pdf) != "Shopify"
    
"""
class Test_LabelSorter:
    inst = LabelSorter(pdf_path=amazon_pdf)
    
    assert inst.sorted_dict == {}
"""    