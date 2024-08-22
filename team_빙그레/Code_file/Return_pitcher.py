import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

def scrape_data(urls, name_selector, table_selector):
    data = []
    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.select_one(name_selector).text.strip()
        table_rows = soup.select(f"{table_selector} > tr")
        for row in table_rows:
            cells = [cell.text.strip() for cell in row.find_all('td')]
            if cells:
                data.append([name] + cells)

        time.sleep(random.uniform(11, 30))

    return data

def get_headers(url, headers_selector):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    header_cells = [cell.text.strip() for cell in soup.select(f"{headers_selector} th")]
    return ["name"] + header_cells

retire_pitcher_url = [
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=93715", # 구대성
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=62349", # 김병현
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=78232", # 김선우
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=63111", # 류제국
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=62761", # 박찬호
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=77147", # 봉중근
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=78640", # 서재응
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=77591", # 송승준
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=75620", # 윤석민
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=67008", # 이대은
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=93147", # 이상훈
    "https://www.koreabaseball.com/Record/Retire/Pitcher.aspx?playerId=95657", # 임창용
]

pitcher_url = [
    "https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId=77829", # 김광현
    "https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId=76715", # 류현진
    "https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId=77637", # 양현종
    "https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId=75421", # 오승환
]

retire_pitcher_data = scrape_data(retire_pitcher_url, "#cphContents_cphContents_cphContents_ucRetireInfo_lblName", "#contents > div.sub-content > div.player_records > table.tData01.tt.mb5 > tbody")

pitcher_data = scrape_data(pitcher_url, "#cphContents_cphContents_cphContents_playerProfile_lblName", "#contents > div.sub-content > div.player_records > div > table > tbody")

headers = get_headers("https://www.koreabaseball.com/Record/Player/PitcherDetail/Total.aspx?playerId=75421", "#contents > div.sub-content > div.player_records > div > table > thead")

all_data = retire_pitcher_data + pitcher_data

save_to_csv("메이저리그진출투수.csv", headers=headers, data=all_data)
