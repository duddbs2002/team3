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
        time.sleep(random.uniform(2, 5))
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.select_one(name_selector).text.strip()
        table_rows = soup.select(f"{table_selector} > tr")
        for row in table_rows:
            cells = [cell.text.strip() for cell in row.find_all('td')]
            if cells:
                data.append([name] + cells)

        time.sleep(random.uniform(5, 10))

    return data

def get_headers(url, headers_selector):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    header_cells = [cell.text.strip() for cell in soup.select(f"{headers_selector} tr:nth-child(1)")]
    return ["name"] + header_cells

pitcher_url = "https://statiz.sporki.com/player/?m=situation&p_no=10590" # 류현진

pitcher_data = scrape_data(pitcher_url, "body > div.warp > div.container > section > div.top_meum_box > div.team_list > div > div.team_info > div.t_name", "body > div.warp > div.container > section > div.table_type02.transverse_scroll.cbox > table > tbody")

headers = get_headers("https://statiz.sporki.com/player/?m=situation&p_no=10590", "body > div.warp > div.container > section > div.table_type02.transverse_scroll.cbox > table > tbody > tr:nth-child(1)")

all_data = pitcher_data

save_to_csv("류현진상세지표(샘플).csv", headers=headers, data=all_data)
