from pypdf import PdfReader, PdfWriter
import pdfplumber, re, os, sys, logging
from regex_patterns import *
from pprint import pprint
from sorting_algorithms import *

logging.getLogger('pdfminer').setLevel(logging.ERROR)
            
def main() -> dict:
    summary_dict = {}
    while True:
        try:
            input_dir = input("Enter the input pdf file directory : ")
            # Remove the quote characters from the input directory string
            input_dir = re.sub(r'"|\'',"",input_dir)
            # Make sure the file exists
            #verify_directory(input_dir)
            
            # Platform setting, need to be automated in the future
            platform = find_platform(input_dir)
            with pdfplumber.open(input_dir) as pdf_file:
                for page_index, page in enumerate(pdf_file.pages):
                    page_text = page.extract_text(); page_tables = page.extract_tables()
                    
                    page_number = f"{page_index+1} : "
                    
                    # Assigning the sorting algorithm based on the platform
                    sorting_dict = {
                        "amazon" : sort_amazon_label(page_number,summary_dict,page_text, page_tables, page_index+1),
                    }
                    # Sanitizing platform input
                    platform = platform.strip().lower()
                    # selecting sorting function based on the selection
                    if platform in sorting_dict.keys():
                        sorting_dict[platform]
                    else:
                        print("Unsupported platform")
                        break
        except AttributeError:
            print("Attribute issues at the regex matching.")
        except FileNotFoundError:
            print(f"The filepath : {input_dir} does not exist, check the input and try again..")
        except Exception as e:
            print(e)
        else:
            
            # Creating a folder in the name of the input file
            out_folder = input_dir.replace(".pdf","")
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
            
            # verify the summary dict is populated
            # store the sorted orders into their respective files in the target directory
            
            for sorted_prodname, keys in summary_dict.items():
                if sorted_prodname == "Mixed":
                    create_pdf(
                        input_pdf_dir = input_dir, sorted_page_nums = keys, 
                        output_directory = out_folder, out_file = sorted_prodname
                    )
                else:
                    for sorted_qty,sorted_pages in keys.items():
                        create_pdf(
                            input_pdf_dir = input_dir, sorted_page_nums = sorted_pages, 
                            output_directory = out_folder, out_file = f"{sorted_prodname} - {sorted_qty}"
                        )
            return summary_dict 
                
def create_shipment_summary(
    sorting_key:str, summary_dict, page_nums:list, qty : str
    ) -> None:
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
    
def verify_directory(directory: str) -> None:
    try:
        if not os.path.exists(directory):
            sys.exit(f"The directory : {directory} does not exist.")
        else:
            return True
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    main()