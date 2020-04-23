import fileinput
import re
import os
import uuid
from datetime import datetime
import pandas as pd

curr_dir=os.path.dirname(os.path.abspath(r'C:\Users\abc\Downloads\Installables for Python\pandas_excel_sheet_test.py'))
UserInput = pd.ExcelFile(curr_dir+r'\UserInput.xlsx')

# Reading reference XML file
XML_FILE_PATH = (curr_dir+r'\combined_ref.xml')
REF_XML = open(XML_FILE_PATH, 'r')
REF_CONTENT = REF_XML.read()

# Creating output XML file with the name '<Source Name>.xml'
def gen_xml(fileename,content):
    out_xml_file = open(fileename, 'w', newline='\n')
    out_xml_file.writelines(content)
    out_xml_file.close()

sheet = pd.read_excel(UserInput, sheet_name='SchemaSheet')
table_df = sheet['TABLENAME'].drop_duplicates()
for table in table_df:
    NEW_FILE_CONTENT = REF_CONTENT.replace('VAR_SOURCE_NAME', table).replace('VAR_CURRENT_DATE',datetime.now().strftime("%m/%d/%Y %H:%M:%S")).replace('VAR_UUID', str(uuid.uuid1()))
    out_xml_name = curr_dir + '\wf_' + table + '.xml'
    gen_xml(out_xml_name,NEW_FILE_CONTENT)
    for line in fileinput.input(out_xml_name, inplace=True):
        if re.findall(r'SOURCEFIELD|TARGETFIELD|TRANSFORMFIELD |CONNECTOR', line):
            for index, row in sheet.iterrows():
                if sheet.iloc[index,0]==table:
                    print(line.replace('VAR_FIELD_NAME', row['NAME'])
                          .replace('VAR_FIELD_SCALE', str(row['SCALE']))
                          .replace('VAR_FIELD_PRECISION', str(row['PRECISION']))
                          .replace('VAR_FIELD_KEYTYPE', row['KEYTYPE'])
                          .replace('VAR_FIELD_DATATYPE', row['DATATYPE']), end='')
        else:
            print(line, end='')