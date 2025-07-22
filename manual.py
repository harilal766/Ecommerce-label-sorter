
from label_sorter.core import LabelSorter

from label_sorter.platforms.ecommerce.amazon import AmazonLabel
from tests.filepaths import *

label_inst = LabelSorter(pdf_path=amazon_pdf)


print(label_inst.create_sorted_pdf_files())