
from label_sorter.core import LabelSorter
import re

from label_sorter.platforms.ecommerce.amazon import AmazonLabel

pdf_input = str(input("Enter the pdf filepath : "))
pdf_input = re.sub(r'\"|\"','',pdf_input)
label_inst = LabelSorter(pdf_path=pdf_input)


print(label_inst.create_sorted_pdf_files())