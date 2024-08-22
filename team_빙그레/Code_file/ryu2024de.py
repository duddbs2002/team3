import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv

def scrape_pitcher_detail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headers = []
    header_elements = soup.select('#contents > div.sub-content > div.player_records > div:nth-child(4) > table > thead > tr > th')
    for header in header_elements:
        headers.append(header.text.strip())

    data = []
    table_selectors = [
        '#contents > div.sub-content > div.player_records > div:nth-child(4) > table > tbody > tr',
        '#contents > div.sub-content > div.player_records > div:nth-child(5) > table > tbody > tr',
        '#contents > div.sub-content > div.player_records > div:nth-child(6) > table > tbody > tr',
        '#contents > div.sub-content > div.player_records > div:nth-child(7) > table > tbody > tr',
        '#contents > div.sub-content > div.player_records > div:nth-child(8) > table > tbody > tr',
        '#contents > div.sub-content > div.player_records > div:nth-child(9) > table > tbody > tr'
    ]

    for selector in table_selectors:
        row_elements = soup.select(selector)
        for row in row_elements:
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            data.append(row_data)

    return headers, data

def main():
    url = 'https://www.koreabaseball.com/Record/Player/PitcherDetail/Daily.aspx?playerId=76715'
    headers, data = scrape_pitcher_detail(url)
    
    save_to_csv("ryu2024de.csv", headers=headers, data=data)

if __name__ == "__main__":
    main()
