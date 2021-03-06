import time
from data.reportdata import ReportFormat
from parse import XMLParser
from bursamy.download import BursaFileDownloader
from text import TextParser
#from bursamy.company import GetCompanyList
from regex import RegularExp
from bursa.company import CompanyList
from bursa.stats import Statistics
from bursa.announcement import Announcement
from utils.parser import Parser
from bursa.download import FileDownloader


file_path = 'C://Users//vince//stockmy//source//testptrans//txt//PTRANS 2016.09-final.pdf.txt'
file_path2 = 'C://Users//vince//stockmy//source//testlayhong//txt//LHB-QR Q1-FYE2019.pdf.txt'
#c0138 = ReportFormat("0138")
#c0138.add_page("Cashflow",1)
#c0138.add_page("Income",2)
#c0138.add_page_info(0,"Revenue","1","2","1000")
#print(c0138.get_page_info(0,0))




def downloading_report(symbol : str):
    BursaFileDownloader(symbol).get_financial_result()

def structuring_data(file_path : str):
    df = XMLParser(file_path).convert_pages_to_df()
    print(df[0])
    wholepdf = XMLParser.concat_all_pages_df(df)
    wholepdf = wholepdf[wholepdf['Content'].map(len)> 0]
    print(wholepdf)
    wholepdf.to_csv(r'MCTQ42019.csv',index=False)

def get_company_list(market : str):
    pass

def display_text_valid(file_path : str):
    lines = TextParser(file_path)._read_all_lines()
    RegularExp(lines).restructure_lines()

if __name__ == "__main__":
    start_time = time.time()
    #downloading_report('0040')
    #display_text_valid(file_path)
    #TextParser(file_path2).get_value("Revenue")
    #df = get_company_list("ace_market")
    #CompanyList("main_market").get_list()
    Statistics().get_trading_participation()
    #Announcement("0186").get_financial_result()
    #FileDownloader("5147").download_finiancial_result()
    #Parser(file_path2).restructure_lines()
    print("--- %s seconds ---" % (time.time() - start_time))