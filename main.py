from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import json
import re


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
    WebDriverWait(self.driver, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h1"))
    )
    self.vars["window_handles"] = self.driver.window_handles
    self.driver.find_element(By.CSS_SELECTOR, "h1").click()
    self.vars["win8248"] = self.wait_for_window(2000)
    self.driver.switch_to.window(self.vars["win8248"])
    pagesource = self.driver.page_source
    html = etree.HTML(pagesource)
    journal = {}
    journal["URL"] = self.driver.current_url
    journal["name"] = name
    tmp = html.xpath('//h3[@class="titbox"]/following-sibling::p[1]/text()')
    if(len(tmp) > 0):
      journal["En_name"] = tmp[0]
    else:
      journal["En_name"] = ""
    tmp = html.xpath('//label[contains(text(),"主办单位")]/following-sibling::span[1]/text()')
    if(len(tmp) > 0):
      journal["unit"] = tmp[0]
    else:
      journal["unit"] = ""
    tmp = html.xpath('//label[contains(text(),"出版周期")]/following-sibling::span[1]/text()')
    if(len(tmp) > 0):
      journal["cycle"] = tmp[0]
    else:
      journal["cycle"] = ""
    tmp = html.xpath('//label[contains(text(),"ISSN")]/following-sibling::span[1]/text()')
    if(len(tmp) > 0):
      journal["ISSN"] = tmp[0]
    else:
      journal["ISSN"] = ""
    tmp = html.xpath('//label[contains(text(),"CN")]/following-sibling::span[1]/text()')
    if(len(tmp) > 0):
      journal["CN"] = tmp[0]
    else:
      journal["CN"] = ""
    tmp = html.xpath('//span[1][@id="jiName"]/text()')
    if(len(tmp) > 0):
      journal["jiname"] = tmp[0]
    else:
      journal["jiname"] = ""
    tmp = html.xpath('//span[1][@id="tiName"]/text()')
    if(len(tmp) > 0):
      journal["tiname"] = tmp[0]
    else:
      journal["tiname"] = ""
    tmp = html.xpath('//label[contains(text(),"复合影响因子")]/following-sibling::span[1]/text()')
    if(len(tmp) > 0):
      journal["FIF"] = tmp[0]
    else:
      journal["FIF"] = ""
    tmp = html.xpath('//label[contains(text(),"综合影响因子")]/following-sibling::span[1]/text()')
    if(len(tmp) > 0):
      journal["ZIF"] = tmp[0]
    else:
      journal["ZIF"] = ""
    return journal

with open("name.json","r") as f:
  List = json.load(f)

domain = "https://navi.cnki.net"


for subject in List:
  for i, subsubject in enumerate(subject):
    if i == 0:
      continue
    for j, journal_name in enumerate(subsubject):
        if j == 0:
            continue
        Detail = Go_detail()
        Detail.setup_method()
        pos = re.search(r'\.', journal_name, re.U)
        if(pos != None):
          journal_name = journal_name.replace(r'\.', '(')
          journal_name = journal_name + ')'
        subsubject[j] = Detail.work(journal_name)
        Detail.teardown_method()

    

json_list = json.dumps(List, indent=1, ensure_ascii=False)
fo = open('sample_output.json', 'w')
fo.write(json_list)