
from label_sorter.core import LabelSorter
from tests.filepaths import *

label_inst = LabelSorter(pdf_path=shopify_pdf)


label_inst.sort_label()