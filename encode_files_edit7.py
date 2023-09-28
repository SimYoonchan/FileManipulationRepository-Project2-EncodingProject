from itertools import count
import os
import shutil #This helps move, copy, etc.
import chardet
import ftfy
from docx import Document
import re 



#Lists: (Learning Note: Appending to a list within a function still saves it in the list even for other functions)
list_fallback_encodings = [
    'utf-8', 'latin-1', 'utf-16', 'utf-32', 'cp1252', 'iso-8859-1',
    'iso-8859-2', 'iso-8859-3', 'iso-8859-4', 'iso-8859-5', 'iso-8859-6',
    'iso-8859-7', 'iso-8859-8', 'iso-8859-9', 'iso-8859-10', 'iso-8859-13',
    'iso-8859-14', 'iso-8859-15', 'iso-8859-16', 'windows-1250', 'windows-1251',
    'windows-1252', 'windows-1253', 'windows-1254', 'windows-1255', 'windows-1256',
    'windows-1257', 'windows-1258', 'macintosh', 'mac-roman', 'ascii',
    'big5', 'euc-jp', 'euc-kr', 'gb2312', 'gbk', 'hz-gb-2312', 'shift-jis',
    'ks_c_5601-1987'
]

list_expected_languages = ['en', 'fr', 'de', 'es', 'ko']  # Update with the languages you expect. 
    # En = English,
    # Fr = French,
    # De = German,
    # Es = Spanish,
    # Ko = Korean,


list_encode_these_endswith_filetypes = [
    '.txt',
]

list_correct_endswith_files =[]
list_incorrect_endswith_files =[]

list_successful_encoding_files= []
list_failed_encoding_files = []



# Set the folder pathways [MANUAL]:
start_broken_folder = '/Users/simyoonchan/Documents/EncodingProject/1. Start Broken Folder'
incorrect_endswith_dumpster_folder = '/Users/simyoonchan/Documents/EncodingProject/2. Incorrect Endswith Dumpster Folder'
failed_encoding_files_dumpster_folder = '/Users/simyoonchan/Documents/EncodingProject/3. Failed Encoding Files Dumpster Folder'
destination_resolved_folder = '/Users/simyoonchan/Documents/EncodingProject/4. Destination Resolved Folder'



#Function Line Break:
def print_empty_row():
    print()



#Function Vertical Line: To divide major sections
def print_vertical_line():
    print("|"*80)



#Function Horizontal Line: To divide minor sections
def print_horizontal_line():
    print("-"*100)



#Function Section Separators:
def section_separator():
    print_empty_row()
    print_empty_row()
    print_vertical_line()
    
def within_section_separator():
    print_empty_row()
    print_horizontal_line()



# Function:
def count_and_copy_files():
   #Initialize the counter for all files.
   files_count = 0
   

   #Step: Loop through files & Count files
   for root_folder, throwaway_variable, list_of_file_names in os.walk(start_broken_folder):
       for file in list_of_file_names:
          start_file_path = os.path.join(root_folder, file)

          #Identify file for copy.
          print(f"File ready for copy: {file} from {start_file_path}")
          print_empty_row()

          #Increment file count.
          files_count += 1

    
   #Step: Declare total number of files
   print(f"You have this number of files: {files_count}")


   #Step: Decider point
   while True: #While true loop will continuosuly prompt the user until valid response.
        user_response = input("Would you like to copy all these files and its folders? (yes copy/no):")
   
        if user_response.lower() in ['yes copy']:
            
            #Step: Copy files
                #Note: Before copying the files, you can remove the destination folder if it already exists. You can do this by using the shutil.rmtree() function to delete the destination folder and its contents. After that, you can proceed with copying the files.
            if os.path.exists(destination_resolved_folder):
                 shutil.rmtree(destination_resolved_folder)
            shutil.copytree(start_broken_folder, destination_resolved_folder)
            
            #Section separator.
            section_separator()

            #Next Function.
            move_onto_next_function_separate_endswith_files()
            break

        elif user_response.lower() in ['no']:
            #Section separator.
            section_separator()
            break

        else:
            print("Invalid input. Print 'yes copy' or 'no'.")



#Function:
def move_onto_next_function_separate_endswith_files():
    while True: #While true loop will continuosuly prompt the user until valid response.
        user_response = input("Do you want to move onto the next function? (Separate endswith files) (yes move on/no):")

        if user_response.lower() in ['yes move on']:          
            #Section separator.
            section_separator()

            #Next Function.
            separate_endswith_files()
            break
        
        elif user_response.lower() in ['no']:
            #Section separator.
            section_separator()
            break

        else:
            print("Invalid input. Please enter 'yes move on' or 'no'.")



#Function:
def separate_endswith_files():
    for root_folder, throwaway_variable, list_of_file_names in os.walk(destination_resolved_folder):
        for file in list_of_file_names:
            start_file_path = os.path.join(root_folder, file)
            could_not_resolve_file_path = os.path.join(incorrect_endswith_dumpster_folder, file)

            for endswith in list_encode_these_endswith_filetypes:
                if file.endswith(endswith):
                    list_correct_endswith_files.append(file)
                else:
                    # Ensure the destination directory exists before moving the file
                    os.makedirs(incorrect_endswith_dumpster_folder, exist_ok=True)
                    new_destination_path = os.path.join(incorrect_endswith_dumpster_folder, file)
                    
                    try:
                        shutil.move(start_file_path, new_destination_path)
                        list_incorrect_endswith_files.append(file)
                    except Exception as e:
                        print(f"Error moving {file} to {new_destination_path}: {e}")
                        print_empty_row()


    #Print Lists.
    #Using the join() method to print items separated by a newline
    within_section_separator()
    print("Correct Endswith Files Identified:")
    for item in list_correct_endswith_files:
        print(item)
    
    within_section_separator()
    print("Incorrect Endswith Files Identified and moved:") 
    for item in list_incorrect_endswith_files:
        print(item)
    

    #Section separator.
    section_separator()


    #Next Function.
    move_onto_next_function_encode_files()



#Function:
def move_onto_next_function_encode_files():
    while True: #While true loop will continuosuly prompt the user until valid response.
        user_response = input("Do you want to move onto the next function? (Encode files as word doc) (yes move on/no):")

        if user_response.lower() in ['yes move on']:          
            #Section separator.
            section_separator()

            #Next Function.
            encode_files_as_word_doc()
            break
        
        elif user_response.lower() in ['no']:
            #Section separator.
            section_separator()
            break

        else:
            print("Invalid input. Please enter 'yes move on' or 'no'.")



# Function to encode files as Word documents
def encode_files_as_word_doc():
    #Variables.
    counter_successful_encoded_files = 0
    counter_error_processing_file = 0

    counter_error_saving_as_word_doc = 0
    counter_error_deleting_files = 0


    for root_folder, _, list_of_file_names in os.walk(destination_resolved_folder):
        for file in list_of_file_names:
            broken_file_start_file_path = os.path.join(root_folder, file)
            file_name_without_extension, _ = os.path.splitext(os.path.basename(broken_file_start_file_path))
            destination_docname_file_path = os.path.join(root_folder, f'{file_name_without_extension}.docx')

            try:
                with open(broken_file_start_file_path, 'rb') as f:
                    raw_content = f.read()
                result = chardet.detect(raw_content)
                encoding = result['encoding'] if result['encoding'] else 'utf-8'

                #Use ftfy to fix encoding issues
                content = ftfy.fix_text(raw_content.decode(encoding))
            except Exception as e:
                print(f"Error processing {broken_file_start_file_path}: {e}")

                #Move the unencodable file to the failed encoding folder
                shutil.move(broken_file_start_file_path, os.path.join(failed_encoding_files_dumpster_folder, file))
                print(f"The error file moved to: {os.path.join(failed_encoding_files_dumpster_folder, file)}")

                #Increment for failed files here.
                counter_error_processing_file += 1
                
                print_empty_row()
                continue

            if content:
                doc = Document()
                doc.add_paragraph(content)

                try:
                    doc.save(destination_docname_file_path)
                    
                    #Increment after the save happens.
                    counter_successful_encoded_files += 1
                except Exception as e:
                    print(f"Error saving as Word document: {e}")

                    #Increment.
                    counter_error_saving_as_word_doc += 1

                    print_empty_row()
                    continue

                try:
                    os.remove(broken_file_start_file_path)
                except Exception as e:
                    print(f"Error deleting original file: {e}")

                    #Increment.
                    counter_error_deleting_files += 1

                    print_empty_row()
                
                print(f'Successfully decoded and saved as {destination_docname_file_path}')
                print_empty_row()

            else:
                print(f'Unable to decode {broken_file_start_file_path}')
                print_empty_row()
    
    print_empty_row()
    print_horizontal_line()
    print(f"Successfully encoded files count: {counter_successful_encoded_files}")
    print(f"Error processing files count: {counter_error_processing_file}")
    print(f"Error saving as word doc count: {counter_error_saving_as_word_doc}")
    print(f"Error deleting files count: {counter_error_deleting_files}")



#Call Functions:
count_and_copy_files()


#What to input into Command Prompt in MacBook:
    #1) cd /Users/simyoonchan/Documents/EncodingProject
    #2) python3 encode_files_edit7.py 

