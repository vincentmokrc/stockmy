from bursamy.convert import PdfConverter
import sys

#LINUX convert

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

#dir_path = "./test"
print(sys.argv[1])
PdfConverter(sys.argv[1]).covert_all_to_xml()
#xml = convert_pdf(dir_path,'xml')
#print(xml)