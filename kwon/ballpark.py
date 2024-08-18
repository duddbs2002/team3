import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv
import sys


url = "https://statiz.sporki.com/add/"

try:  
  response = requests.get(url)
  response.raise_for_status()
except requests.RequestException as e:
  print(f"요청오류:{e}")
  sys.exit() # 오류발생시 프로그램 종료

bs = BeautifulSoup(response.text, 'html.parser')

table = bs.find('table')
if table is None:
  print("테이블을 찾을 수 없습니다")
  sys.exit()

headers = []
for th in table.find_all('th'):
  headers.append(th.text.strip())

rows=[] 
for tr in table.find_all('tr'):
  cells=[td.text.strip() for td in tr.find_all('td')]
  if cells:   
    rows.append(cells)
  
try:
  save_to_csv("ballpark.csv", headers=headers, data=rows)
  print("데이터가 저장되었습니다")
except Exception as e:
  print(f"CSV 저장 오류:{e}")