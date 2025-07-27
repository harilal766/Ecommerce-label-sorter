import json, os
from pathlib import Path

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
test_and_root_join = os.path.join(TEST_DIR,"..")
Root = os.path.abspath(test_and_root_join)



with open("creds.json","r") as json_file:
    credentials = json.load(json_file)
    
    amazon_pdf = os.path.join(TEST_DIR, credentials["amazon"])
    shopify_pdf = os.path.join(TEST_DIR, credentials["shopify"])
    
    
with open("requirements.txt", "r") as req:
    required_dependencies = [line.strip() for line in req.readlines()]
    