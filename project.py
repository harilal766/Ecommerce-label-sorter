from PyPDF2 import PdfReader
import pdfplumber
import pandas as pd
import json



def main():
    """
    read a pdf file and detect the shipment type eg : amazon, shopify etc
    """
    try:
        with open('creds.json') as json_file:
            json_dict = json.load(json_file)
            input_dir = json_dict["input"]
            output_dir = json_dict["output"]
        platform = "Amazon "
        summary = 0
        
        str = {
            "vertical_strategy": "lines", 
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": [],
            "explicit_horizontal_lines": [],
            "snap_tolerance": 3,
            "snap_x_tolerance": 3,
            "snap_y_tolerance": 3,
            "join_tolerance": 3,
            "join_x_tolerance": 3,
            "join_y_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 3,
            "min_words_horizontal": 1,
            "intersection_tolerance": 3,
            "intersection_x_tolerance": 3,
            "intersection_y_tolerance": 3,
            "text_tolerance": 3,
            "text_x_tolerance": 3,
            "text_y_tolerance": 3,
            #"text_*": …, # See below
        }
        
        with pdfplumber.open(input_dir) as pdf_file:
            for page in pdf_file.pages:
                page_text = page.extract_text()
                page_table = page.extract_tables()
                
                if platform.strip().lower() == 'amazon':
                    processed_invoice_data = []
                    if len(page_table) > 1:
                        processed_headers = [column.replace("\n", " ") for column in page_table[0][0]]
                        print(processed_headers)
                        print("+++")

                    
    except Exception as e:
        print(e)
    else:
        return summary
        


if __name__ == "__main__":
    main()