from Ecommerce_Label_Sorter import LabelSorter
import re

pdf_input = str(input("Enter the pdf filepath : "))
pdf_input = re.sub(r'\"|\"','',pdf_input)
label_inst = LabelSorter(pdf_path=pdf_input)

print(label_inst.create_sorted_pdf_files())


