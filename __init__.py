import time
from data.reportdata import ReportFormat
from parse import XMLParser

start_time = time.time()
file_path = 'C://Users//vince//stockmy//testmi//xml\\MI Q1 FYE2019.pdf.xml'
#c0138 = ReportFormat("0138")
#c0138.add_page("Cashflow",1)
#c0138.add_page("Income",2)
#c0138.add_page_info(0,"Revenue","1","2","1000")
#print(c0138.get_page_info(0,0))

########
#dir_path = "C://Users//vince//stockmy//test//xml"
#XMLConvertor(dir_path).open_xml()
#####
df = XMLParser(file_path).convert_pages_to_df()
print(df[0])
wholepdf = XMLParser.concat_all_pages_df(df)
print(wholepdf)
wholepdf.to_csv(r'testlol.csv',index=False)

print("--- %s seconds ---" % (time.time() - start_time))

