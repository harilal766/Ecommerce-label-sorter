import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from filepaths import amazon_pdf, shopify_pdf
from label_sorter.core import LabelSorter

class Test_LabelSorter:
    label_inst = LabelSorter(pdf_path=shopify_pdf)
    
    files = {
        "Shopify" : shopify_pdf,
        "Amazon" : amazon_pdf
    }
    
    def test_find_platfrom(self):
        for key,value in self.files.items():
            inst = LabelSorter(pdf_path=value)
            assert inst.find_platform() == key
        
    def test_sort_label(self):
        assert len(self.label_inst.create_sorted_dictionary().keys()) > 0
        
        
    # need more tests for mixed orders and amazon qr page

