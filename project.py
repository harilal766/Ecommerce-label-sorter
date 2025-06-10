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
            input_dir = json.load(json_file)["input"]
        platform = "Amazon "
        summary = 0
        
        print(input_dir)
        """
        with pdfplumber.open(input_dir) as pdf_file:
            for page in pdf_file.pages:
                page_text = page.extract_text()
                page_table = page.extract_table()
                
                if platform.strip().lower() == 'amazon':
                    df = pd.DataFrame(page_table)
        """
                    
        
        
    except Exception as e:
        pass
    else:
        return summary
        





if __name__ == "__main__":
    main()