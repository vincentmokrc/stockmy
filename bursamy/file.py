from base import _BaseSelenium
import pandas as pd
import glob
import os
import shutil
from os import path
from selenium.webdriver.common.by import By
from pathlib import Path
import re
from datetime import datetime

class GetPdf(_BaseSelenium):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        self.url_list = []
        self.company_name_list = []
        self.file_naming = []
        self.file_info =[]
        self.url = "https://www.bursamalaysia.com/market_information/announcements/company_announcement/announcement_details?ann_id={0}"

    def download_all_pdf(self, df):
        #print(df)
        url_list = self.generate_all_links(df)
        k = 0
        self.remove_all_pdf()
        for m, i in enumerate(url_list):
            self.file_info.clear()
            
            if (k > len(url_list)):
                print("done")
                break

            self.index = url_list.index(i)
            self.company_name = self.company_name_list[m]

            print(i)
            self.driver.get(i)
            self.wait_until_presence(By.XPATH,'//iframe[@id = "bm_ann_detail_iframe"]')
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
            k+=1
            try:
                #get the info of the table
                table_id = self.driver.find_element(By.CLASS_NAME, 'formContentTable')
                rows = table_id.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    col = row.find_elements(By.TAG_NAME, "td")[1]
                    self.file_info.append(col.text)

                self.driver.find_element_by_xpath("//div[@class='attachment fixed']//a").click()
            except:
                pass

            #self._wait(5)
            self.check_pdf_file_exist()
        
        print("Waiting Countdown 60 s")
        self._wait(5)
        self.quit_driver()

    def generate_all_links(self, df):
        self.df = df
        self.company_name_list = df['Company'].tolist()
        self.file_naming = df['Content'].tolist()
        linkid_list = df['Link ID'].tolist()
        for linkid in linkid_list:
            url_generated = self.url.format(linkid)
            self.url_list.append(url_generated)

        return self.url_list

    def check_pdf_file_exist(self):

        while (len(glob.glob(self.save_directory + "//*pdf.part")) > 0):
            self._wait(1)

        file_list = []
        file_list = glob.glob(self.save_directory + "//*pdf")
        print(file_list[0])


        if path.exists(file_list[0]): 
            real_path = path.realpath(file_list[0])
                
            try:
                newfile = self.rename_file(real_path)
            except:
                self.unblock_file(real_path)
                newfile = self.rename_file(real_path)

            if(path.exists(newfile)):
                self.copy_remove_file(newfile)
            else:
                self.copy_old_file(real_path)

    def copy_old_file(self, old_file_name):
        src_file = old_file_name
        dst_dir= os.path.join("C://fs",self.company_name)
        print(dst_dir)
        self.ensure_dir(dst_dir)
        shutil.copy(src_file,dst_dir)
        os.remove(old_file_name)

    def rename_file(self, old_file_name):
        #print(old_file_name)
        path_name = path.realpath(old_file_name)
        #print(os.path.basename(path_name))
        dir_path = os.path.dirname(path_name)
        file_ext = self.get_file_ext(old_file_name)

        if(self.is_pattern_line(r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}",self.file_info[2])):
            self.file_info[2] = self.change_date_format(self.file_info[2])

        new_file_name = "{0} {1} {2}{3}".format(self.company_name, self.file_info[1], self.file_info[2], file_ext)
        new_file_name = os.path.join(dir_path , new_file_name)
        os.rename(old_file_name, new_file_name)
        print("RENAME: {0} -> {1}".format(old_file_name,new_file_name))
        return new_file_name

    def copy_remove_file(self, src_file):
        dst_dir= os.path.join("C://fs",self.company_name)
        self.ensure_dir(dst_dir)
        print("MOVE to {0}".format(dst_dir))
        shutil.copy(src_file,dst_dir)
        os.remove(src_file)

    def ensure_dir(self, dir_path):
        #directory = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def remove_all_pdf(self, dir_path = None):
        
        file_list = []
        file_list = glob.glob(self.save_directory + "//*pdf")
        for f in file_list:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

    def unblock_file(self, dirpath):
        system_str = 'powershell.exe -Command Unblock-File -Path "{0}"'.format(os.path.normpath(dirpath))
        print("Unblock file : " + system_str)
        os.system(system_str)
        self._wait(1)

    def get_file_ext(self,file_path):
        return Path(file_path).suffix

    def is_pattern_line(self, pattern, line):
        r =re.compile(pattern)
        return bool(r.match(line))

    def change_date_format(self,date_string):
        date = datetime.strptime(date_string, r'%d/%m/%Y')
        return date.strftime("%d %b %Y")