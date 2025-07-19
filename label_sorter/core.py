import pdfplumber, re, os
from pypdf import PdfReader, PdfWriter

from label_sorter.platforms.ecommerce.shopify import ShopifyLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel

class LabelSorter:
    def __init__(self):
        self.sorted_dict = {}
        
    def find_platform(self,pdf_path : str) -> str:
        platform = None
        try:
            with pdfplumber.open(pdf_path) as pdf_file:
                total_pages = 0; amazon_count = 0 
                
                shopify_order_id_count, amazon_order_id_count = 0, 0
                
                for page_index, page in enumerate(pdf_file.pages):
                    total_pages += 1
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    
                    # Shopify Initializations
                    if re.findall(ShopifyLabel.order_id_pattern, page_text):
                        shopify_order_id_count += 1
                    elif re.findall(AmazonLabel.order_id_pattern, page_text):
                        amazon_order_id_count += 1
                        
                    
                if total_pages == shopify_order_id_count:
                    platform = "Shopify"
                # this condition is not complete, need to add overlap page detection
                elif total_pages/2 == amazon_order_id_count:
                    platform == "Amazon"
            
        except Exception as e:
            print(e)
        else:
            return platform
        
    def get_filepath() -> str:
        while True:
            try:
                filepath = str(input("Enter the pdf filepath : "))
                filepath = re.sub(r'"|\'',"",filepath)
                if os.path.exists(filepath):
                    print("\nFile verified..\n")
                    return filepath
                else:
                    print(f"The path does not exist, try again")
            except FileNotFoundError:
                print("Try again")

    def sort_label(self):
        title = None
        try:
            print(self.platform)
            
            """
            with pdfplumber.open(self.input_filepath) as pdf_file:
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    page_number = page_index+1
                    
                    if self.platform == "Shopify":
                        #print(page_text,end="\n"+"-"*20+"\n")
                        self.sort_shopify_label(page_text=page_text,page_num=int(page_number))
            """
        except Exception as e:
            print(e)
        else:
            return self.sorted_dict
        
    def create_pdf(input_pdf_dir: str, sorted_page_nums: list, out_file:str, output_directory:str) -> None:
        try:
            # verify the pdf file exists
            # Verify the page contains something
            if len(sorted_page_nums) > 0:
                # Init
                reader = PdfReader(input_pdf_dir); writer = PdfWriter()
                
                for page in sorted_page_nums:
                    writer.add_page(reader.pages[page-1])
                
                order_count = int(len(sorted_page_nums)/2)
                # Sanitizing out file name
                out_file = re.sub(r'\|',",",out_file)
                #print(out_file)
                
                output_directory = os.path.join(
                    output_directory, f"{out_file.replace("/"," ")} - {order_count} Order{"s" if order_count > 1 else ""}.pdf"
                )
                #print(output_directory)
                if output_directory:
                    with open(output_directory,"wb") as output_pdf:
                        writer.write(output_pdf)
            else:
                sys.exit("Enter page nums")
        except FileNotFoundError as e:
            print("File location issues :\n", e)
        """
        except Exception as e:
            print(e)
        """
        
    def create_shipment_summary(self, sorting_key:str, summary_dict, page_nums:list, qty : str) -> None:
        try:
            # different conditions for mixed and single items
            # sorting key initialization
            # The line `if sorti` is incomplete and does not exist in the provided code snippet. It
            # seems like there might have been a typo or an incomplete statement. If you can provide
            # more context or clarify the specific line of code you are referring to, I would be
            # happy to help explain it.
            
            numbers_list = None
            # Adding sorting key if not present
            if sorting_key not in summary_dict.keys(): 
                summary_dict[sorting_key] = [] if sorting_key == "Mixed" else {}

            if sorting_key == "Mixed":
                numbers_list = summary_dict[sorting_key]
            else:
                if qty not in summary_dict[sorting_key].keys():
                    summary_dict[sorting_key][qty] = []
                numbers_list = summary_dict[sorting_key][qty]
            numbers_list += page_nums
            
        except Exception as e:
            print(e)
            
    def create_sorted_pdf_files():
        pass