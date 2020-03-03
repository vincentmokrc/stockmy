from base import _BaseSelenium
import pandas as pd
import glob
import os
import shutil
from os import path
from selenium.webdriver.common.by import By

class GetPdf(_BaseSelenium):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        self.url_list = []
        self.company_name_list = []
        self.file_naming = []
        self.url = "https://www.bursamalaysia.com/market_information/announcements/company_announcement/announcement_details?ann_id="

    def download_all_pdf(self, df):
        #print(df)
        url_list = self.generate_all_links(df)
        k = 0
        self.remove_all_pdf()
        for i in url_list:
            
            if (k > len(url_list)):
                print("done")
                break

            self.index = url_list.index(i)

            print(i)
            self.driver.get(i)
            self.wait_until_presence(By.XPATH,'//iframe[@id = "bm_ann_detail_iframe"]')
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
            k+=1
            try:
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
            url_generated = self.url + linkid
            self.url_list.append(url_generated)

        return self.url_list

    def check_pdf_file_exist(self):

        while (len(glob.glob(self.save_directory + "//*pdf.part")) > 0):
            self._wait(1)
            print("Waiting Download")

        file_list = []
        file_list = glob.glob(self.save_directory + "//*pdf")
        print(file_list[0])

        if path.exists(file_list[0]):
            self.copy_rename(file_list[0],"me")
            pass

    def copy_rename(self, old_file_name, new_file_name):
        #src_dir= self.save_directory
        #dst_dir= os.path.join("C://fs",, ".pdf")
        #src_file = os.path.join(src_dir, old_file_name)
        #self.ensure_dir(old_file_name)
        src_file = old_file_name
        print(old_file_name)
        dst_dir= os.path.join("C://fs",self.company_name_list[self.index])
        print(dst_dir)
        self.ensure_dir(dst_dir)
        shutil.copy(src_file,dst_dir)
        
        dst_file = os.path.join(dst_dir, old_file_name)
        #new_dst_file_name = os.path.join(dst_dir, self.file_naming[self.index])
        #os.rename(dst_file, new_dst_file_name) 
        os.remove(old_file_name)

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