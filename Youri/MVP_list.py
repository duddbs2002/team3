import requests
from bs4 import BeautifulSoup
import team3_module

url = "https://www.koreabaseball.com/Player/Awards/PlayerPrize.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

data = []
rows = soup.select("#contents > div.sub-content > table > tbody > tr")

for row in rows:
    cells = [cell.get_text(strip=True, separator=" ") for cell in row.find_all('td')]
    if cells:
        data.append(cells)

header = ["연도", "KBO MVP", "KBO 신인상"]
team3_module.save_to_csv("MVP LIST.csv", headers=header, data=data)
