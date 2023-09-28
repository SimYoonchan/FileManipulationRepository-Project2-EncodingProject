from itertools import count
import os
import chardet
import ftfy
from docx import Document

# List of fallback encodings to try
fallback_encodings = [
    'utf-8', 'latin-1', 'utf-16', 'utf-32', 'cp1252', 'iso-8859-1',
    'iso-8859-2', 'iso-8859-3', 'iso-8859-4', 'iso-8859-5', 'iso-8859-6',
    'iso-8859-7', 'iso-8859-8', 'iso-8859-9', 'iso-8859-10', 'iso-8859-13',
    'iso-8859-14', 'iso-8859-15', 'iso-8859-16', 'windows-1250', 'windows-1251',
    'windows-1252', 'windows-1253', 'windows-1254', 'windows-1255', 'windows-1256',
    'windows-1257', 'windows-1258', 'macintosh', 'mac-roman', 'ascii',
    'big5', 'euc-jp', 'euc-kr', 'gb2312', 'gbk', 'hz-gb-2312', 'shift-jis',
    'ks_c_5601-1987'
]

# Function to fix broken .txt files
def fix_files():

    # This keeps track of how many successful and failed counting there is.
    totalEncodingCounter = 0
    failedEncodingCounter = 0
    failedEncodingFiles = [] #This is a list to store all the failed encoded files.

    # !!! Get the list of broken .txt files in the "Broken" folder !!!
    broken_folder = '/Users/simyoonchan/Documents/EncodingProject/BrokenRound1-Test2'
    broken_files = [f for f in os.listdir(broken_folder) if f.endswith('.txt')]

    # Process each broken file
    for file in broken_files:
        file_path = os.path.join(broken_folder, file)

        # Open the broken .txt file and read its content
        with open(file_path, 'rb') as f:
            raw_content = f.read()

        # Detect the encoding of the content using chardet
        result = chardet.detect(raw_content)
        encoding = result['encoding']

        if encoding is None:
            encoding = 'utf-8'  # Use UTF-8 as a default encoding if detection fails

        # Try decoding the content using the detected encoding
        try:
            content = raw_content.decode(encoding)
        except UnicodeDecodeError:
            # Attempt decoding with fallback encodings if other attempts fail
            for fallback_encoding in fallback_encodings:
                try:
                    content = raw_content.decode(fallback_encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"Unable to decode {file_path}")
                failedEncodingCounter += 1
                failedEncodingFiles.append(file)
                continue

        # Fix the encoding issues using ftfy
        content = ftfy.fix_text(content)

        # Create a new .docx file
        doc = Document()
        doc.add_paragraph(content)

        # !!! Save the fixed .docx file in the "Resolved" folder with the same name !!!
        resolved_folder = '/Users/simyoonchan/Documents/EncodingProject/ResolvedRound1'
        docx_file_path = os.path.join(resolved_folder, os.path.splitext(file)[0] + '.docx')
        doc.save(docx_file_path)

        print('Fixed file created: ' + docx_file_path)
        totalEncodingCounter += 1

    print('Number of times total encoding: ' + str(totalEncodingCounter))
    print('Number of times failed encoding: ' + str(failedEncodingCounter))
    print('Files with failed encoding:', failedEncodingFiles)

# Call the fix_files function
fix_files()






