from label_sorter.platforms.ecommerce.base_label import BaseLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel
from tests.test_core import Test_LabelSorter
from tests.filepaths import amazon_pdf

import pdfplumber



class TestBaseLabel(Test_LabelSorter):
    pass

class TestAmazon(TestBaseLabel):
    pdf = pdfplumber.open(amazon_pdf)
    pages = pdf.pages
    
    page = pages[33]
    am_inst = AmazonLabel(
        page_text= page.extract_text(), page_table=page.extract_table(),page_num=33
    )
    def test_pages(self):
        assert type(self.pages) == list
        assert self.pages[0]
    
    def test_analyze_amzn_page(self):
        assert self.am_inst.analyze_amzn_page()