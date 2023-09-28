from itertools import count
import os
import shutil #This helps move, copy, etc.
import chardet
import ftfy #This helps with encoding.
from docx import Document
import re 
from send2trash import send2trash #This helps throw things out to trash.
import subprocess #This helps with changing a file from Locked to Unlocked status.



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

#Note: Include whatever is in 'list_move_already_goodswith_filetypes'
list_encode_these_endswith_filetypes = [
    '.TXT',
    '.txt',
]
list_move_already_good_endswith_filetypes = [
    '.docx',
]

list_correct_endswith_files =[]
list_incorrect_endswith_files =[]

list_locked_to_unlocked_files = []

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



#Function:
def count_and_copy_files():
   print("ENCODING LOG:")
   
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
   within_section_separator()
   print(f"You have this number of files: {files_count}")


   #Step: Decider point
   within_section_separator()
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
            move_onto_next_function_unlock_files()
            break

        elif user_response.lower() in ['no']:
            #Section separator.
            section_separator()
            break

        else:
            print("Invalid input. Print 'yes copy' or 'no'.")



#Function:
def move_onto_next_function_unlock_files():
    while True: #While true loop will continuosuly prompt the user until valid response.
        user_response = input("Do you want to move onto the next function? (Unlock Files) (yes move on/no):")

        if user_response.lower() in ['yes move on']:          
            #Section separator.
            section_separator()

            #Next Function.
            unlock_files()
            break
        
        elif user_response.lower() in ['no']:
            #Section separator.
            section_separator()
            break

        else:
            print("Invalid input. Please enter 'yes move on' or 'no'.")



#Function: 
def unlock_files():
    #Variables.
    counter_successfully_unlocked_files = 0
    counter_not_locked = 0
    counter_failed_to_check_or_unlock_file = 0


    for root_folder, throwaway_variable, list_of_file_names in os.walk(destination_resolved_folder):
        for file in list_of_file_names:
            start_file_path = os.path.join(root_folder, file)

            try:
                result = subprocess.run(["ls", "-lO", start_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
                attributes = result.stdout.strip().split()
                if "uchg" in attributes:
                    # File is locked, so unlock it
                    subprocess.run(["chflags", "nouchg", start_file_path], check=True)
                    print(f"File '{start_file_path}' has been successfully unlocked.")
                    print_empty_row()

                    #Increment
                    counter_successfully_unlocked_files += 1

                    #Add to list
                    list_locked_to_unlocked_files.append(file)
                else:
                    print(f"File '{start_file_path}' is not locked.")
                    print_empty_row()
                    
                    #Increment
                    counter_not_locked += 1
            except subprocess.CalledProcessError:
                print(f"Failed to check or unlock file '{start_file_path}'.")
                print_empty_row()
                
                #Increment
                counter_failed_to_check_or_unlock_file += 1
    

    #Print Lists.
    #Using the join() method to print items separated by a newline
    within_section_separator()
    print("Locked to unlocked files:")
    for item in list_locked_to_unlocked_files:
        print(item)


    #Within section separator
    within_section_separator()

    print(f"Successfully unlocked files count: {counter_successfully_unlocked_files}")
    print(f"Files not locked count: {counter_not_locked}")
    print(f"Failed to check or unlock file count: {counter_failed_to_check_or_unlock_file}")


    #Section separator.
    section_separator()


    #Next Function.
    move_onto_next_function_separate_endswith_files()



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
    #Variables
    counter_separated_endswith_files = 0
    counter_error_moving_endswith_files = 0


    #Compile a regular expression pattern to match any of the extensions
    encode_endswith_pattern = r'|'.join(re.escape(ext) for ext in list_encode_these_endswith_filetypes)


    for root_folder, throwaway_variable, list_of_file_names in os.walk(destination_resolved_folder):
        for file in list_of_file_names:
            start_file_path = os.path.join(root_folder, file)
            incorrect_endswith_file_path = os.path.join(incorrect_endswith_dumpster_folder, file)
            

            #Go through encode_endswith_patterns.
            if re.search(encode_endswith_pattern, file, re.IGNORECASE):  # Case-insensitive match
                list_correct_endswith_files.append(file)
            else:
                #Ensure the destination directory exists before moving the file
                os.makedirs(incorrect_endswith_dumpster_folder, exist_ok=True)
                try:
                    if os.access(incorrect_endswith_dumpster_folder, os.W_OK):
                      shutil.move(start_file_path, incorrect_endswith_file_path)
                      list_incorrect_endswith_files.append(file)

                      #Increment.
                      counter_separated_endswith_files += 1

                except Exception as e:
                    print(f"Error moving {file} to {incorrect_endswith_file_path}: {e}")
                    
                    #Incremnet
                    counter_error_moving_endswith_files += 1
                    print_empty_row()


    #Print Lists.
    #Using the join() method to print items separated by a newline
    # within_section_separator()
    # print("Already good Endswith Files Identified:")
    # for item in list_move_already_good_endswith_filetypes:
    #     print(item)

    within_section_separator()
    print("Correct Endswith Files Identified:")
    for item in list_correct_endswith_files:
        print(item)
    
    within_section_separator()
    print("Incorrect Endswith Files Identified and moved:") 
    for item in list_incorrect_endswith_files:
        print(item)

    #Within section separator
    within_section_separator()
    print(f"Separated endswith files count: {counter_separated_endswith_files}")
    print(f"Error for separating endswith files count: {counter_error_moving_endswith_files}")
    

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
    counter_move_already_good_endswith_files = 0
    
    counter_successful_encoded_files = 0
    counter_error_processing_file = 0

    counter_error_saving_as_word_doc = 0
    counter_trashing_old_unencoded_files = 0
    counter_error_could_not_move_to_trash = 0
    counter_error_deleting_files = 0


    #Compile a regular expression pattern to match any of the extensions
    # move_already_good_endswith_pattern = r'|'.join(re.escape(ext) for ext in list_move_already_good_endswith_filetypes)


    for root_folder, _, list_of_file_names in os.walk(destination_resolved_folder):
        for file in list_of_file_names:
            
            broken_file_start_file_path = os.path.join(root_folder, file)
            file_name_without_extension, _ = os.path.splitext(os.path.basename(broken_file_start_file_path))
            destination_docname_file_path = os.path.join(root_folder, f'{file_name_without_extension}.docx')
            failed_encoding_files_file_path = os.path.join(failed_encoding_files_dumpster_folder, file)


            # #Go through move_already_good_endswith_patterns.
            # if re.search(move_already_good_endswith_pattern, file, re.IGNORECASE):
            #     list_move_already_good_endswith_filetypes.append(file)
            #     shutil.move(broken_file_start_file_path, broken_file_start_file_path) #Essentially, keep it where it is.

            #     #Increment.
            #     counter_move_already_good_endswith_files += 1

            try:
                with open(broken_file_start_file_path, 'rb') as f:
                    raw_content = f.read()
                result = chardet.detect(raw_content)
                encoding = result['encoding'] if result['encoding'] else 'utf-8'

                #Use ftfy to fix encoding issues
                content = ftfy.fix_text(raw_content.decode(encoding))

                #Remove control characters and non-XML-compatible characters
                content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F]', '', content)
            except Exception as e:
                print(f"Error processing {broken_file_start_file_path}: {e}")

                #Move the unencodable file to the failed encoding folder
                if os.access(failed_encoding_files_dumpster_folder, os.W_OK):
                    shutil.move(broken_file_start_file_path, failed_encoding_files_file_path)
                    print(f"The error file moved to: {os.path.join(failed_encoding_files_dumpster_folder, file)}")

                #Increment for failed files here.
                counter_error_processing_file += 1
                
                print_empty_row()
                continue
            

            # #Attempt to decode using fallback encodings if decoding as UTF-8 failed
            # if not content:
            #     for fallback_encoding in list_fallback_encodings:
            #         try:
            #             content = raw_content.decode(fallback_encoding, errors='ignore')
            #             break  # Break the loop if decoding succeeds
            #         except Exception as e:
            #               print(f"Error processing {broken_file_start_file_path}: {e}")

            #               #Move the unencodable file to the failed encoding folder
            #               if os.access(failed_encoding_files_dumpster_folder, os.W_OK):
            #                   shutil.move(broken_file_start_file_path, failed_encoding_files_file_path)
            #                   print(f"The error file moved to: {os.path.join(failed_encoding_files_dumpster_folder, file)}")

            #               #Increment for failed files here.
            #               counter_error_processing_file += 1
                          
            #               print_empty_row()
            #               continue


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
                    send2trash(broken_file_start_file_path)  # Move the file to Trash
                    
                    #Increment.
                    counter_trashing_old_unencoded_files += 1  
                except Exception as e:
                    print(f"Error moving {broken_file_start_file_path} to Trash: {e}")
                    
                    #Increment.
                    counter_error_could_not_move_to_trash += 1 
                    print_empty_row()
                    continue
                
                print(f'Successfully decoded and saved as {destination_docname_file_path}')
                print_empty_row()

            else:
                print(f'Unable to decode {broken_file_start_file_path}')
                print_empty_row()
    

    #Within section separator
    within_section_separator()
    print("ENCODING SUMMARY:")
    #print(f"Already good Endswith files count: {counter_move_already_good_endswith_files}")
    print(f"Successfully encoded files count: {counter_successful_encoded_files}")
    print(f"Error processing files count: {counter_error_processing_file}")
    print(f"Error saving as word doc count: {counter_error_saving_as_word_doc}")
    print(f"Trashing old unencoded files count: {counter_trashing_old_unencoded_files}")
    print(f"Error moving files to trash: {counter_error_could_not_move_to_trash}")
    print(f"Error deleting files count: {counter_error_deleting_files}")



#Call Functions:
count_and_copy_files()


#What to input into Command Prompt in MacBook:
    #1) cd /Users/simyoonchan/Documents/EncodingProject
    #2) python3 encode_files_edit12.py 

