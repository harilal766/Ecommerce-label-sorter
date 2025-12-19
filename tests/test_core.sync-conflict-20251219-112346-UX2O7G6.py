import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from filepaths import *
from label_sorter.core import LabelSorter


class Test_LabelSorter:
    label_inst = LabelSorter(pdf_path=amazon_pdf)
    
    files = {
        "Shopify" : shopify_pdf,
        "Amazon" : amazon_pdf
    }
    def test_find_platfrom(self):
        for platform,filename in self.files.items():
            if filename.endswith('.pdf') and os.path.exists(filename):
                inst = LabelSorter(pdf_path=filename)
                assert inst.find_platform() == platform
    
    def test_create_sorted_summary(self):
        assert type(self.label_inst.create_sorted_summary()) == dict