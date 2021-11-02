import analyze
from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

class Go_detail():
  def setup_method(self):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  def work(self, name):
    self.driver.get("https://navi.cnki.net/knavi/journals/search?&q=" + quote(name))
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "h1").click()
    self.vars["win8248"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win8248"])
    pagesource = self.driver.page_source
    html = etree.HTML(pagesource)
    journal = {}
    journal["URL"] = self.driver.current_url
    journal["name"] = name
    journal["En_name"] = html.xpath('//h3[@class="titbox"]/following-sibling::p[1]/text()')[0]
    journal["unit"] = html.xpath('//label[contains(text(),"主办单位")]/following-sibling::span[1]/text()')[0]
    journal["cycle"] = html.xpath('//label[contains(text(),"出版周期")]/following-sibling::span[1]/text()')[0]
    journal["ISSN"] = html.xpath('//label[contains(text(),"ISSN")]/following-sibling::span[1]/text()')[0]
    journal["CN"] = html.xpath('//label[contains(text(),"CN")]/following-sibling::span[1]/text()')[0]
    journal["jiname"] = html.xpath('//span[1][@id="jiName"]/text()')[0]
    journal["tiname"] = html.xpath('//span[1][@id="tiName"]/text()')[0]
    journal["FIF"] = html.xpath('//label[contains(text(),"复合影响因子")]/following-sibling::span[1]/text()')[0]
    journal["ZIF"] = html.xpath('//label[contains(text(),"综合影响因子")]/following-sibling::span[1]/text()')[0]
    return journal

pdf_path = "/Users/tongweixi/Desktop/cnki-crawler/北大图书馆中文核心期刊要目总览（2020版）.pdf"
A = analyze.Analyze_pdf()
List = A.work(pdf_path)

domain = "https://navi.cnki.net"


for subject in List:
    for i, journal_name in enumerate(subject[1]):
        if i == 0:
            continue
        Detail = Go_detail()
        Detail.setup_method()
        subject[1][i] = Detail.work(journal_name)
        Detail.teardown_method()
        
print(List)