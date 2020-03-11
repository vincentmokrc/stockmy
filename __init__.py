#from bursamy.download import BursaFileDownloader
import time
from bursamy.xml import XMLConvertor
#from convert_pdf import convert_pdf

start_time = time.time()
#BursaFileDownloader("9385").get_financial_result()
#dir_path = "C:\\fs\\test\\test.pdf"

#LINUX convert
#dir_path = "./test"
#print(dir_path)
#PdfConverter(dir_path).covert_all_to_xml()
#xml = convert_pdf(dir_path,'xml')
#print(xml)


########
dir_path = "C://Users//vince//stockmy//test//xml"
XMLConvertor(dir_path).open_xml()
#####

print("--- %s seconds ---" % (time.time() - start_time))

