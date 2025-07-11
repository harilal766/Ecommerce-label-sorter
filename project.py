from pypdf import PdfReader, PdfWriter
import pdfplumber, re, os, sys, logging
from regex_patterns import *
from pprint import pprint
from sorting_algorithms import *

logging.getLogger('pdfminer').setLevel(logging.ERROR)
            
def main(input_dir = None) -> dict:
    sorted_dict = None
    print("Welcome to Shipping label sorter")
    while True:
        try:
            if not input_dir:
                input_dir = input("Please enter the input pdf filepath : ")
            input_dir = re.sub(r'"|\'',"",input_dir)
            platform = find_platform(input_dir).strip().lower()
            if platform:
                sort_inst = Sort(pdf_path=input_dir, platform='amazon')
                sorted_dict = sort_inst.get_sorted_summary()
            else:
                sys.exit("Unsupported platform")        
        except AttributeError:
            print("Attribute issues at the regex matching.")
        except FileNotFoundError:
            print(f"The filepath : {input_dir} does not exist, check the input and try again..")
        except Exception as e:
            print(e)
        else:
            if sorted_dict:
                out_folder = input_dir.replace(".pdf","")
                if not os.path.exists(out_folder):
                    os.makedirs(out_folder)
                for sorted_prodname, keys in sorted_dict.items():
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
                return sorted_dict

def find_platform(pdf_path : str) -> str:
    """Finding the platform by reading the pdf file
    
    Args:
        pdf_path (str): Filepath of the label pdf file

    Returns:
        str: Name of the Ecommerce platfrom to which the pdf belongs to, Eg : Amazon, Flipkart etc.
    """
    platform = None
    try:
        with pdfplumber.open(pdf_path) as pdf_file:
            total_pages = 0; amazon_count = 0 
            for page_index, page in enumerate(pdf_file.pages):
                total_pages += 1
                page_text = page.extract_text(); page_tables = page.extract_tables()
                
                # finding platfrom based on the order id
                amazon_order_id_match = re.findall(amazon_order_id_pattern,page_text)
                if amazon_order_id_match:
                    amazon_count +=1
    except Exception as e:
        print(e)
    else:
        if amazon_count == total_pages/2:
            platform = "Amazon"
        return platform

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