import json
from opcode import opname
from operator import mod
from bs4 import BeautifulSoup
import requests
import time
def get_timestamp():
  return str(int(time.time()))
DICTIONARY = {
  
}
def get_all_link(path):
  url = "http://tracnghiem.net/cntt/700-cau-hoi-trac-nghiem-excel-2010-co-dap-an-10.html?mode=part&part="
  for page in range(1,15):
    page_link = url + str(page)
    x = requests.get(page_link, verify=False)
    soup = BeautifulSoup(x.text.encode('ascii','ignore'),'html.parser')
    exam_content = soup.find('div',{'class':"exam-content"})
    if exam_content != None:
      list_questions = exam_content.findAll('a')
      for item in list_questions:
        href = item.attrs["href"]
        with open(path,mode='a') as f:
          f.write(href+"\n")
    print("Finish page "+str(page))
def load_links(path):
  contents = []
  with open(path,mode='r') as f:
    content = f.readlines()
    for item in content:
        contents.append(item.strip())
    return contents
# get_all_link()
def crawl_link(link):
  global DICTIONARY
  id = get_timestamp()
  DICTIONARY[id] = {}
  x = requests.get(link, verify=False)
  soup = BeautifulSoup(x.text.encode('utf-8','ignore'),'html.parser')
  box  = soup.find('div',{'class':"d9Box part-item detail question-detail"})
  cauhoi = soup.find("h1")
  cauhoi_text = cauhoi.text.strip()
  inputs = box.findAll("label")
  cautraloi = ''
  for item in inputs:
      cautraloi += item.text.strip()+"\n"
  cautraloi = cautraloi.strip()
  dapan = soup.find("span",{'class':"right-answer"})
  dapan_key = dapan.find("b").text.strip()
  # dapan_text = dapan.text.strip()
  DICTIONARY[id]['question'] = cauhoi_text+"\n"+cautraloi
  DICTIONARY[id]['answer'] = dapan_key
  print("Crawled "+str(link))
def save_data(path):
  json_string = json.dumps(DICTIONARY, ensure_ascii=False)
  with open(path, mode='w',encoding='utf-8') as f:
    f.write(json_string)
def load_data(path):
  with open(path, mode='r', encoding='utf-8') as f:
    content = f.read()
    DATA = json.loads(content)
    return DATA
def start_crawl(path):
  links = load_links(path)
  for link in links:
    links = load_links(path)
    crawl_link(link)
  save_data(path)
# start_crawl()
# load_data()