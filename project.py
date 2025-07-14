from pypdf import PdfReader, PdfWriter
import pdfplumber, re, os, sys, logging
from regex_patterns import *
from pprint import pprint
from sorting_algorithms import *

logging.getLogger('pdfminer').setLevel(logging.ERROR)
exit_key = "E"
quit_message = f"Press {exit_key} key to exit the program."
            
def main(input_dir = None) -> dict:
    status_list = ["\nSorting Summary"]; sorted_dict = None
    print("Welcome to Shipping label sorter\n")
    try:
        if not input_dir:
            input_dir = get_filepath()
            
        #input_dir = re.sub(r'"|\'',"",input_dir)
        if os.path.exists(input_dir):
            platform = find_platform(input_dir)
            if platform:
                print(f"Platform : {platform}")
                print("\nSorted pages")
                sort_inst = Sort(pdf_path=input_dir, platform=platform.strip().lower())
                sorted_dict = sort_inst.get_sorted_summary()
            else:
                sys.exit("Unsupported platform, Exiting....")  
        else:
            print(f"This filepath does not exist, check the input and try again..")
    except AttributeError:
        pass
    else:
        if sorted_dict:
            out_folder = input_dir.replace(".pdf","")
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)
                    
            for sorted_prodname, value in sorted_dict.items():
                if sorted_prodname == "Mixed":
                    create_pdf(
                        input_pdf_dir = input_dir, sorted_page_nums = value, 
                        output_directory = out_folder, out_file = sorted_prodname
                    )
                    status_list.append(f"{sorted_prodname} : {int(len(value)/2)} Orders.")
                else:
                    for sorted_qty,sorted_pages in value.items():
                        create_pdf(
                            input_pdf_dir = input_dir, sorted_page_nums = sorted_pages, 
                            output_directory = out_folder, out_file = f"{sorted_prodname} - {sorted_qty}"
                        )
                        status_list.append(f"{sorted_prodname} - {sorted_qty} : {int(len(sorted_pages)/2)} Orders.")
            print(f"\nSorted files saved to : {out_folder}")
            print("\n".join(status_list))
            return sorted_dict

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
    
if __name__ == "__main__":
    main()