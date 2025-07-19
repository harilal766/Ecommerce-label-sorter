import json, os

with open("creds.json","r") as json_file:
    credentials = json.load(json_file)
    test_directory = credentials["test_dir"]
    
    amazon_pdf = os.path.join(test_directory, credentials["amazon_input_filepath"])
    shopify_pdf = os.path.join(test_directory, credentials["shopify"])