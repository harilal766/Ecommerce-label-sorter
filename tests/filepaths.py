import json, os
from pathlib import Path

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
test_and_root_join = os.path.join(TEST_DIR,"..")
Root = os.path.abspath(test_and_root_join)
test_label_dir = os.path.join(Root,"test_labels")

with open("label_sorter.json","r") as json_file:
    credentials = json.load(json_file)
    
    amazon_pdf = os.path.join(test_label_dir, credentials["amazon"])
    shopify_pdf = os.path.join(test_label_dir, credentials["shopify"])
    
    
