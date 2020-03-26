import time
from data.reportdata import ReportFormat
from parse import XMLParser
from bursamy.download import BursaFileDownloader


file_path = 'C://Users//vince//stockmy//testmct//xml//MCT-Q4 FY2019 Financial Results.pdf.xml'
#c0138 = ReportFormat("0138")
#c0138.add_page("Cashflow",1)
#c0138.add_page("Income",2)
#c0138.add_page_info(0,"Revenue","1","2","1000")
#print(c0138.get_page_info(0,0))




def downloading_report(symbol):
    BursaFileDownloader(symbol).get_financial_result()

def structuring_data(file_path):
    df = XMLParser(file_path).convert_pages_to_df()
    print(df[0])
    wholepdf = XMLParser.concat_all_pages_df(df)
    wholepdf = wholepdf[wholepdf['Content'].map(len)> 0]
    print(wholepdf)
    wholepdf.to_csv(r'MCTQ42019.csv',index=False)

if __name__ == "__main__":
    start_time = time.time()
    structuring_data(file_path)
    print("--- %s seconds ---" % (time.time() - start_time))