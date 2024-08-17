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
        elif columns:  # Check if it's a header row
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
    "https://statiz.sporki.com/player/?m=situation&p_no=10126&pos=pitching&year=2022&si=1",  # 김광현 (22년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10590&pos=pitching&year=2024&si=1",  # 류현진 (24년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10058&pos=pitching&year=2022&si=1", # 양현종 (22년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10367&pos=pitching&year=2020&si=1", # 오승환 (20년_징계로 인한 1년 공백)
    "https://statiz.sporki.com/player/?m=situation&p_no=10200&pos=pitching&year=2008&si=1", # 김선우 (08년)
    "https://statiz.sporki.com/player/?m=situation&p_no=11090&pos=pitching&year=2013&si=1", # 류제국 (13년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10907&pos=pitching&year=2012&si=1", # 박찬호 (12년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10514&pos=pitching&year=2007&si=1", # 봉중근 (07년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10053&pos=pitching&year=2008&si=1", # 서재응 (08년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10285&pos=pitching&year=2007&si=1", # 송승준 (07년)
    "https://statiz.sporki.com/player/?m=situation&p_no=10061&pos=pitching&year=2015&si=1", # 윤석민 (15년)
    "https://statiz.sporki.com/player/?m=situation&p_no=11907&pos=pitching&year=2019&si=1", # 이대은 (19년)
    "https://statiz.sporki.com/player/?m=situation&p_no=11281&pos=pitching&year=2014&si=1", # 임창용 (14년)
]

all_data = []

for url in url_list:
    response = requests.get(url)

    time.sleep(random.uniform(7, 12))

    bs = BeautifulSoup(response.text, 'html.parser')
    # 선수 정보 추출
    player_name, comeback_year = extract_player_info(bs)
    
    # 테이블 추출
    table = bs.find('table')

    time.sleep(random.uniform(6, 13))

    if table:
        data = []
        headers = extract_headers(table)
        
        # 선수의 이름과 복귀년도를 첫 번째 행에 추가
        data.insert(0, [f"이름: {player_name}", f"복귀년도: {comeback_year}"])
        
        # 전체 데이터를 하나의 리스트에 추가
        all_data.extend(data)

# 데이터를 CSV 파일로 저장
save_to_csv("상황별상세지표_투수.csv", headers=headers, data=all_data)
