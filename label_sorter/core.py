import pdfplumber, re, os,sys, logging
from pypdf import PdfReader, PdfWriter
from pprint import pprint
from label_sorter.platforms.ecommerce.shopify import ShopifyLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel

logging.getLogger('pdfminer').setLevel(logging.ERROR)

class LabelSorter:
    def __init__(self, pdf_path):
        self.sorted_dict = {}
        self.label_filepath = pdf_path
        self.output_folder = self.label_filepath.replace(".pdf","")
        self.platform = self.find_platform(pdf_path=self.label_filepath)
        
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
                    sh = ShopifyLabel()
                    if re.findall(sh.order_id_pattern, page_text):
                        shopify_order_id_count += 1
                    elif re.findall(AmazonLabel.order_id_pattern, page_text):
                        amazon_order_id_count += 1
                        
                if total_pages == shopify_order_id_count:
                    platform = "Shopify"
                # this condition is not complete, need to add overlap page detection
                elif total_pages/2 == amazon_order_id_count:
                    platform == "Amazon"
            
        except FileNotFoundError:
            print(f"The file {pdf_path} does not exist.")
        except Exception as e:
            print(e)
        else:
            return platform
        
    def sort_label(self):
        if not self.platform:
            sys.exit("Unsupported Platform, exiting....")
        page_debrief = None
        try:
            print(f"Platform : {self.platform}")
            with pdfplumber.open(self.label_filepath) as pdf_file:
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    page_number = page_index+1
                    
                    #print(f"{page_number}",end=" - ")
                    if self.platform == "Shopify":
                        #print(page_text,end="\n"+"-"*20+"\n")
                        inst = ShopifyLabel()
                        page_debrief = inst.analyze_page(label_text=page_text, page_num=page_number)
                        
                    # sorting summary
                    if self.platform:
                        self.populate_shipment_summary(
                            sorting_key=page_debrief["sorting_key"], qty=page_debrief["qty"],
                            page_nums=[page_number - 1, page_number] if self.platform == "Amazon" else [page_number]
                        )
                    #print(page_debrief)
        except FileNotFoundError as fe:
            print(fe)
        except Exception as e:
            print(e)
        else:
            return self.sorted_dict
        
    def populate_shipment_summary(self, sorting_key:str, page_nums:list, qty : str) -> None:
        try:
            # different conditions for mixed and single items
            # sorting key initialization
            
            numbers_list = None
            # Adding sorting key if not present
            if sorting_key not in self.sorted_dict.keys(): 
                self.sorted_dict[sorting_key] = [] if sorting_key == "Mixed" else {}

            if sorting_key == "Mixed":
                numbers_list = self.sorted_dict[sorting_key]
            else:
                if qty not in self.sorted_dict[sorting_key].keys():
                    self.sorted_dict[sorting_key][qty] = []
                numbers_list = self.sorted_dict[sorting_key][qty]
            numbers_list += page_nums
            
        except Exception as e:
            print(e)
            
    def create_pdf(self, pdf_name, page_numbers):
        try:
            reader = PdfReader(self.label_filepath); writer = PdfWriter()
            print(pdf_name, page_numbers)
            # adding pages to the writer
            for page in page_numbers:
                writer.add_page(reader.pages[page-1])
            page_count = len(page_numbers)
            order_count = int(page_count/2) if self.platform == "Amazon" else page_count
            sorted_pdf_file = f"{pdf_name} - {order_count} order{"s" if order_count > 1 else ""}.pdf"
        except Exception as e:
            print(e)
        else:
            if writer:
                with open(os.path.join(self.output_folder, sorted_pdf_file), "wb") as out_pdf:
                    writer.write(out_pdf)        
            
    def create_sorted_pdf_files(self):
        summary_dict = self.sort_label()
        
        #pprint(summary_dict.keys())
        
        if len(summary_dict.keys()) == 0:
            sys.exit("Cannot sort with empty summary...")
            
        order_count = None; page_numbers = None
        output_file = None 
        
        # Create output folder
            
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"Created output folder : {self.output_folder}")
            
        try:
            print(f"Sorted Summary :")
            for sorting_key, value in summary_dict.items():
                # Assigning output file name and its pages according to order type
                # Mixed orders
                if type(value) == list:
                    self.create_pdf(pdf_name=sorting_key, page_numbers=value)
                # single item orders
                elif type(value) == dict:
                    for qty,page_list in value.items():
                        self.create_pdf(pdf_name=f"{sorting_key} - {qty}", page_numbers=page_list)
        except Exception as e:
            print(e)
    

        
