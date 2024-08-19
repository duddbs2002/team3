import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv
import pandas as pd
import os
import sys
sys.path.append('../')  # 부모 디렉토리로 이동하여 모듈을 불러올 수 있게 함
from team3_module import save_to_csv


def extract_headers(table):
  headers = []
  is_header_row = False  # Flag to track header row
  for row in table.find_all('tr'):
    columns = row.find_all(['th', 'td'])  # Search for both th and td tags
    if columns and not is_header_row:  # Check if it's a data row
      row_data = [col.get_text(strip=True) for col in columns]
      data.append(row_data)
    elif columns:  # Check if it's a header row
      is_header_row = True
      header = [col.get_text(strip=True) for col in columns]
      headers.append(header)
  return headers

url = "https://statiz.sporki.com/player/?m=situation&p_no=10590"

response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

table = bs.find('table')

data = []
headers = extract_headers(table)

save_to_csv("류현진상세지표(샘플).csv", headers=headers, data=data)