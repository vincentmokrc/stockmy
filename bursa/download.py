from bursa.announcement import Announcement
from utils.download import FileDownloader
from utils.file import FileOps
from selenium.webdriver.common.by import By
from utils.regex import RegularExpression
from datetime import datetime
import os

class FileDownloader(FileDownloader):
    def __init__(self, symbol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbol = symbol
        self.save_directory = "C:\\report_pdf"
        self.url = "https://www.bursamalaysia.com/{0}"
        self.url_list = []
        self.company_name = ""
        self.file_naming = []
        self.file_info =[]

    def do_action(self, action_list):
        for url in self.url_list:
            self.download_file(url)

    def download_file(self, url):
        FileOps.remove_all_files_in_type(self.save_directory,"pdf")
        self.file_info.clear()
        print(url)
        self.driver.get(url)
        self.wait_until_presence(By.XPATH,'//iframe[@id = "bm_ann_detail_iframe"]')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        try:
            table_id = self.driver.find_element(By.CLASS_NAME, 'formContentTable')
            rows = table_id.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                col = row.find_elements(By.TAG_NAME, "td")[1]
                self.file_info.append(col.text)
            company_name_element = self.driver.find_element(By.CLASS_NAME, 'company_name')
            self.company_name = company_name_element.text
            self.driver.find_element_by_xpath("//div[@class='attachment fixed']//a").click()
        except:
            pass

        self.ensure_downloaded()

    def ensure_downloaded(self):
        FileOps.check_until_none(self.save_directory, "pdf.part")
        pdf_list = FileOps.check_file_exist(self.save_directory, "pdf")
        self.rename_downloaded(pdf_list[1][0])

    def get_new_file(self, old_file_name):
        path_name = FileOps.get_real_path(old_file_name)
        dir_path = FileOps.get_dir_path(path_name)
        file_ext = FileOps.get_file_ext(old_file_name)
        if(RegularExpression.is_pattern_line(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}",self.file_info[2])):
            self.file_info[2] = self.change_date_format(self.file_info[2])
        
        new_file_name = "{0} {1} {2}{3}".format(self.company_name, self.file_info[1], self.file_info[2], file_ext)
        new_file_name = os.path.join(dir_path , new_file_name)
        return new_file_name

    def rename_downloaded(self, file_path):
        old_file_name = FileOps.get_real_path(file_path)
        new_file_name = self.get_new_file(old_file_name)
        FileOps.rename_file(old_file_name, new_file_name)
        dest_dir = "C://fs//" + self.company_name
        dest_dir = FileOps.get_real_path(dest_dir)
        FileOps.copy_remove_file(new_file_name, dest_dir)

    def download_finiancial_result(self):
        df = Announcement(self.symbol).get_financial_result()
        self._generate_all_links(df['ID'].tolist())
        print(self.url_list)
        #url = 'https://www.bursamalaysia.com//market_information/announcements/company_announcement/announcement_details?ann_id=3029423'
        #self.download_file(url)
        self.do_action(None)
        self.quit_driver()
    
    def _generate_all_links(self, link_list):
        for link in link_list:
            url_generated = self.url.format(link)
            self.url_list.append(url_generated)

    def change_date_format(self,date_string):
        date = datetime.strptime(date_string, r'%d/%m/%Y')
        return date.strftime("%d %b %Y")
