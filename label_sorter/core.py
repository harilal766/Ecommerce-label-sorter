import pdfplumber, re, os,sys, logging, json
from pypdf import PdfReader, PdfWriter
from pprint import pprint
from label_sorter.platforms.ecommerce.base_label import BaseLabel
from label_sorter.platforms.ecommerce.shopify import ShopifyLabel
from label_sorter.platforms.ecommerce.amazon import AmazonLabel

logging.getLogger('pdfminer').setLevel(logging.ERROR)

class LabelSorter:
    def __init__(self, pdf_path):
        self.input_filepath = pdf_path
        self.output_folder = self.input_filepath.replace(".pdf","")
        self.platform = self.find_platform()
        self.misc_filename = "Mixed"
        
    def find_platform(self) -> str:
        platform = None
        if os.path.exists(self.input_filepath) == False:
            sys.exit("Input file does not exist....")
        try:
            with pdfplumber.open(self.input_filepath) as pdf_file:
                total_pages = 0; amazon_count = 0 
                
                shopify_order_id_count, amazon_order_id_count = 0, 0
                
                for page_index, page in enumerate(pdf_file.pages):
                    total_pages += 1
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    
                    # Shopify Initializations
                    sh = ShopifyLabel(page_text=page_text, page_table=page_tables,page_num=0)
                    am = AmazonLabel(page_text=page_text, page_table=page_tables,page_num=0)
                    
                    if re.findall(sh.shopify_order_id_pattern, page_text):
                        shopify_order_id_count += 1
                    elif re.findall(am.amazon_order_id_pattern, page_text):
                        amazon_order_id_count += 1
                        
                if total_pages == shopify_order_id_count:
                    platform = "Shopify"
                # this condition is not complete, need to add overlap page detection
                elif amazon_order_id_count > 0:
                    platform = "Amazon"
            
        except FileNotFoundError:
            print(f"The file {self.input_filepath} does not exist.")
        except Exception as e:
            print(e)
        else:
            return platform

    def create_sorted_summary(self):
        page_debrief = None; sorted_dict = {}
        try:
            with pdfplumber.open(self.input_filepath) as pdf_file:
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_table = page.extract_tables()
                    page_number = page_index+1
                    """
                    debriefs = {
                        "Shopify" : ShopifyLabel(page_text=page_text, page_table=page_table,page_num=page_number).analyze_shpy_page(),
                        "Amazon" : AmazonLabel(page_text=page_text, page_table=page_table,page_num=page_number).analyze_amzn_page(),
                    }
                    page_debrief = debriefs.get(self.platform,None)
                    print(page_debrief)                    
                    
                    is_page_debrief_populated = page_debrief["order_id"] != None
                    # sorting summary
                    if self.platform and is_page_debrief_populated:
                        # different conditions for mixed and single items
                        # sorting key initialization
                        numbers_list = None
                        
                        sorting_key = page_debrief.get("sorting_key"); qty = page_debrief.get("qty")
                        page_nums=[page_number - 1, page_number] if self.platform == "Amazon" else [page_number]
                        print(page_debrief)
                    
                        # Adding sorting key if not present
                        if sorting_key not in sorted_dict.keys(): 
                            sorted_dict[sorting_key] = {}

                        if sorting_key == self.misc_filename:
                            numbers_list = sorted_dict[sorting_key]["pages"]
                        else:
                            if qty not in self.sorted_dict[sorting_key].keys():
                                sorted_dict[sorting_key][qty] = []
                            numbers_list = sorted_dict[sorting_key][qty]
                        numbers_list += page_nums
                    """  
        except FileNotFoundError as fe:
            print(fe)
        except Exception as e:
            print(e)
        else:
            return sorted_dict
            
    def create_single_pdf_file(self, pdf_name, page_numbers):
        if page_numbers == None:
            sys.exit("Received Nonetype instead of page numbers")
        try:
            reader = PdfReader(self.input_filepath); writer = PdfWriter()
            print(pdf_name, page_numbers)
            # adding pages to the writer
            for page in page_numbers:
                writer.add_page(reader.pages[page-1])
                
            page_count = len(page_numbers)
            order_count = int(page_count/2) if self.platform == "Amazon" else page_count
            
            sorted_pdf_file = f"{re.sub(r"[\|\.\/]*",r"",pdf_name)} - {order_count} order{"s" if order_count > 1 else ""}.pdf"
        except Exception as e:
            print(e)
        else:
            if writer:
                if sorted_pdf_file:
                    out_filepath = os.path.join(self.output_folder, sorted_pdf_file)
                    with open(out_filepath, "wb") as out_pdf:
                        writer.write(out_pdf)        
            
    def create_sorted_pdf_files(self):
        summary_dict = self.create_sorted_summary()
        
        #pprint(summary_dict.keys())
        
        if len(summary_dict.keys()) == 0:
            sys.exit("Cannot sort with empty summary...")
            
        order_count = None; page_numbers = None
        output_file = None 
        
        # Create output folder if not created already.
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"Created output folder : {self.output_folder}")
        
        # save the summary as a json file to the output folder
        with open(f"{self.output_folder}/summary.json","w") as summary_json:
            json.dump(summary_dict, summary_json)
            
        try:
            print(f"Sorted Summary :")
            for sorting_key, value in summary_dict.items():
                # Assigning output file name and its pages according to order type
                # single item orders
                if type(value) == dict:
                    if type(sorting_key) != self.misc_filename:
                        #print(f"Writing Single item order",end=", ")
                        for qty,page_list in value.items():
                            #print(f"Detected more than one qty.")
                            self.create_single_pdf_file(pdf_name=f"{sorting_key} - {qty}", page_numbers=page_list)
                    else:
                        self.create_single_pdf_file(
                            pdf_name = self.misc_filename, page_numbers= value.get("pages",None)
                        )
                # Mixed orders which returns page numbers list
                elif type(value) == list:
                    self.create_single_pdf_file(pdf_name=sorting_key, page_numbers=value)
                
        except Exception as e:
            print(f"Err : {e}")
