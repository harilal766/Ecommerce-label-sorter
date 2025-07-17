import json


with open("creds.json","r") as json_file:
    credentials = json.load(json_file)
    amzn_input_filepath = credentials["amazon_input_filepath"]
    non_existing_file = amzn_input_filepath.replace(".pdf",".py")
    out_dir = amzn_input_filepath.replace(".pdf", "")