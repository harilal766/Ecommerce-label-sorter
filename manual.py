
from label_sorter.core import LabelSorter

from label_sorter.platforms.ecommerce.amazon import AmazonLabel
from tests.filepaths import *

label_inst = LabelSorter(pdf_path=r"D:\5.Amazon\Mathew global\INvoice\21.7.25 cod 11.pdf")


print(label_inst.create_sorted_pdf_files())


