import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv
import random
import time

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
        time.sleep(random.randint(3, 6))
    return data

def get_headers(url, headers_selector):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    header_cells = [cell.text.strip() for cell in soup.select(f"{headers_selector} th")]
    return ["name"] + header_cells

retire_hitter_url = [
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=71564",
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=77623",
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=71752",
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=70756",
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=97109",
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=95436"
]

hitter_url = [
    "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=76290",
    "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=75125",
    "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=51817",
    "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=76313",
    "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=50848",
]

retire_hitter_data = scrape_data(retire_hitter_url, "#cphContents_cphContents_cphContents_ucRetireInfo_lblName", "#contents > div.sub-content > div.player_records > table.tData01.tt.mb5 > tbody")

hitter_data = scrape_data(hitter_url, "#cphContents_cphContents_cphContents_playerProfile_lblName", "#contents > div.sub-content > div.player_records > div > table > tbody")

headers = get_headers("https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=76313", "#contents > div.sub-content > div.player_records > div > table > thead")

all_data = retire_hitter_data + hitter_data

save_to_csv("메이저리그진출타자.csv", headers=headers, data=all_data)
