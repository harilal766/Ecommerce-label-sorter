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
    def test_pages(self):
        assert type(self.pages) == list