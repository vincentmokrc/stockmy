from base import _BaseSelenium
import pandas as pd

class GetPdf(_BaseSelenium):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = self.get_driver()
        self.url_list = []
        self.url = "https://www.bursamalaysia.com/market_information/announcements/company_announcement/announcement_details?ann_id="

    def download_all_pdf(self, df):
        #print(df)
        url_list = self.generate_all_links(df)
        for i in url_list:
            print(i)
            self.driver.get(i)
            self.wait_until_presence('//iframe[@id = "bm_ann_detail_iframe"]')
            self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
            self.driver.find_element_by_xpath("//div[@class='attachment fixed']//a").click()

    def generate_all_links(self, df):
        linkid_list = df['Link ID'].tolist()
        for linkid in linkid_list:
            url_generated = self.url + linkid
            self.url_list.append(url_generated)

        return self.url_list