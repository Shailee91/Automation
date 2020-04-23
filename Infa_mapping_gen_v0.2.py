import pandas as pd
import re
from pathlib import Path
import fileinput
from datetime import datetime
import uuid
 
# Providing input excel file path
UserInput = (r'C:\Users\abc\Downloads\Installables for Python\UserInput.xlsx')

# Saving excel sheet content to variables
var_sheet = pd.read_excel(UserInput,sheet_name='Variables')
src_sheet = pd.read_excel(UserInput,sheet_name='SourceFields')

# Reading reference XML file
XML_FILE_PATH=(r'C:\Users\abc\Downloads\Installables for Python\Single_field_refrence_XML.xml')
REF_XML=open(XML_FILE_PATH,'r')
REF_CONTENT=REF_XML.read()

# Replacing global variables in reference XML and saving it in a new variable
NEW_FILE_CONTENT=REF_CONTENT.replace('VAR_FOLDER_NAME',var_sheet.iloc[0,1]).replace('VAR_SOURCE_NAME',var_sheet.iloc[1,1]).replace('VAR_CURRENT_DATE',datetime.now().strftime("%m/%d/%Y %H:%M:%S")).replace('VAR_UUID',str(uuid.uuid1()))

# Creating output XML file with the name '<Source Name>.xml' 
out_xml_name='C:\\Users\\abc\\Downloads\\Installables for Python\\m_'+var_sheet.iloc[1,1]+'.xml'
out_xml_file=open(out_xml_name, 'w', newline='\n')
out_xml_file.writelines(NEW_FILE_CONTENT)
out_xml_file.close()

# Replacing dynamic variables in the output XML
for line in fileinput.input(out_xml_name, inplace=True):
    if re.findall(r'SOURCEFIELD|TARGETFIELD|TRANSFORMFIELD|CONNECTOR', line):
        for index, row in src_sheet.iterrows():
            print(line.replace('VAR_FIELD_NAME',row['NAME'])
                      .replace('VAR_FIELD_SCALE',str(row['SCALE']))
                      .replace('VAR_FIELD_PRECISION',str(row['PRECISION']))
                      .replace('VAR_FIELD_KEYTYPE',row['KEYTYPE'])
                      .replace('VAR_FIELD_DATATYPE',row['DATATYPE']), end='')
    else:
        print(line, end='')