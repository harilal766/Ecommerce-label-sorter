from label_sorter import LabelSorter
from tests.filepaths import shopify_pdf, amazon_pdf




ls = LabelSorter(pdf_path=shopify_pdf)
print(ls.find_platform())

