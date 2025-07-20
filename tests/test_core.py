import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from filepaths import amazon_pdf, shopify_pdf
from label_sorter.core import LabelSorter

class Test_LabelSorter:
    def test_find_platfrom(self):
        files = {
            "Shopify" : shopify_pdf
        }
        
        for key,value in files.items():
            inst = LabelSorter(pdf_path=value)
            assert inst.find_platform(pdf_path=value) == key
        
        """
        with pytest.raises(FileNotFoundError):
            self.inst.find_platform(pdf_path=shopify_pdf.replace(".pdf",".py"))
        """
        
    def test_sort_label(self):
        shpy_inst = LabelSorter(pdf_path=shopify_pdf)
        
        assert type(shpy_inst.sort_label()) == dict
        
        
        
