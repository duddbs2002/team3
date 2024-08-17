import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv
import time
import random

def extract_headers(table):
    headers = []
    is_header_row = False  # Flag to track header row
    for row in table.find_all('tr'):
        columns = row.find_all(['th', 'td'])  # Search for both th and td tags
        if columns and not is_header_row:  # Check if it's a data row
            row_data = [col.get_text(strip=True) for col in columns]
            data.append(row_data)
        elif columns:  # Check if it's a header rowt 
            is_header_row = True
            header = [col.get_text(strip=True) for col in columns]
            headers.append(header)
    return headers

def extract_player_info(soup):
    # 선수의 이름 추출
    player_name = soup.select_one('body > div.warp > div.container > section > div.top_meum_box > div.team_list > div > div.team_info > div.t_name').get_text(strip=True)
    
    # 복귀년도 추출
    comeback_year = soup.select_one('#select_year > button').get_text(strip=True)
    
    return player_name, comeback_year

url_list = [
    "https://statiz.sporki.com/player/?m=situation&p_no=10187&pos=batting&year=2018&si=1", # 김현수 (18년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10470&pos=batting&year=2018&si=1", # 박병호 (18년)
    "https://statiz.sporki.com/player/?m=situation&p_no=14888&pos=batting&year=2021&si=1", # 추신수(21년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10407&pos=batting&year=2021&si=1", # 황재균 (18년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10251&pos=batting&year=2017&si=1", # 이대호 (17년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10025&pos=batting&year=2007&si=1", # 최희섭 (07년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10552&pos=batting&year=2012&si=1", # 김태균 (12년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10559&pos=batting&year=2011&si=1", # 이범호 (11년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10491&pos=batting&year=2010&si=1", # 이병규 (10년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10881&pos=batting&year=2012&si=1" # 이승엽 (12년)
]

all_data = []

for url in url_list:
    response = requests.get(url)

    time.sleep(random.uniform(4, 8))

    bs = BeautifulSoup(response.text, 'html.parser')
    # 선수 정보 추출
    player_name, comeback_year = extract_player_info(bs)
    
    # 테이블 추출
    table = bs.find('table')

    time.sleep(random.uniform(5, 11))

    if table:
        data = []
        headers = extract_headers(table)
        
        # 선수의 이름과 복귀년도를 첫 번째 행에 추가
        data.insert(0, [f"이름: {player_name}", f"복귀년도: {comeback_year}"])
        
        # 전체 데이터를 하나의 리스트에 추가
        all_data.extend(data)

# 데이터를 CSV 파일로 저장
save_to_csv("상황별상세지표_타자.csv", headers=headers, data=all_data)
