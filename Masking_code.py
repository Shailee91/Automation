import fileinput
import re
import os
import uuid
from datetime import datetime
import pandas as pd

curr_dir=os.path.dirname(os.path.abspath(r'C:\Users\abc\Downloads\Installables for Python\pandas_excel_sheet_test.py'))
UserInput = pd.ExcelFile(curr_dir+r'\UserInput.xlsx')

XML_FILE_PATH = (curr_dir+r'\Masking_rule_ref.xml')
REF_XML2 = open(XML_FILE_PATH, 'r')
REF_CONTENT2 = REF_XML2.read()


# Creating output XML file with the name '<Source Name>.xml'
def gen_xml(fileename,content):
    out_xml_file2 = open(fileename, 'w', newline='\n')
    out_xml_file2.writelines(content)
    out_xml_file2.close()
    
sheet = pd.read_excel(UserInput, sheet_name='SchemaSheet')
out_xml_name = curr_dir + r'\metadata_value.xml'
gen_xml(out_xml_name,REF_CONTENT2)
for line in fileinput.input(out_xml_name, inplace=True):
    if re.findall(r'<PORT ', line):
        for index, row in sheet.iterrows():
            if row['MASKING_RULE'] == 'Substitution' and re.findall(r'MASKING_OPTION="Substitution"', line):
                        print(line.replace('VAR_FIELD_NAME', row['NAME'])
                        .replace('VAR_FIELD_SCALE', str(row['SCALE']))
                        .replace('VAR_FIELD_PRECISION', str(row['PRECISION']))
                        .replace('VAR_MASK_OUT', str(row['MASKING_OUTPUT']))
                        .replace('VAR_MASK_IN', str(row['MASKING_INPUT']))
                        .replace('VAR_MASK_DICT', str(row['DICTIONARY_COLUMN']))
                        .replace('VAR_DIC_NAME', str(row['DICT_FILE'])), end='')
            elif row['MASKING_RULE'] == 'Key' and re.findall(r'MASKING_OPTION="Key"', line):
                print(line.replace('VAR_FIELD_NAME', row['NAME'])
                        .replace('VAR_FIELD_SCALE', str(row['SCALE']))
                        .replace('VAR_FIELD_PRECISION', str(row['PRECISION'])), end='')
            elif row['MASKING_RULE'] == 'Expression' and re.findall(r'MASKING_OPTION="Expression"', line):
                print(line.replace('VAR_FIELD_NAME', row['NAME'])
                        .replace('VAR_FIELD_SCALE', str(row['SCALE']))
                        .replace('VAR_FIELD_PRECISION', str(row['PRECISION'])), end='')
    else:
        print(line, end='')

for line in fileinput.input(out_xml_name, inplace=True):
    print(line.replace(r'&',r'&amp;').replace(r'<',r'&lt;').replace(r'>',r'&gt;').replace(r'"',r'&quot;').replace(r"'",r'&apos;').replace('\n',''), end='')