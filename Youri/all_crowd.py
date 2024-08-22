import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_table_header(soup):
    thead = soup.select_one("#tblHistory > thead")
    if thead:
        header = [th.text.strip() for th in thead.find_all("th")]
    else:
        header = ["Year", "Total Attendance", "Games", "Average Attendance", "Per Game Average"]
    
    # '_avg' 추가
    header_avg = [f"{h}_avg" if h else '' for h in header]
    return header, header_avg

def parse_table_data(soup):
    rows = soup.select("#tblHistory > tbody > tr")
    data = []

    for row in rows:
        cols = row.find_all("td")
        row_data = []
        row_avg_data = []

        for col in cols:
            text = col.text.strip()
            # 괄호 안 값과 밖의 값을 구분
            match = re.match(r"([^\(\)]+)\s*\(?([^\(\)]*)\)?", text)
            if match:
                value = match.group(1).strip()
                avg_value = match.group(2).strip() if match.group(2) else ''
            else:
                value = text
                avg_value = ''
            
            row_data.append(value)
            row_avg_data.append(avg_value)
        
        data.append(row_data + row_avg_data)
    
    return data


def save_to_csv(data, header, header_avg, filename):
    full_header = header + header_avg
    df = pd.DataFrame(data, columns=full_header)
    df.to_csv(filename, index=False, encoding='utf-8')

def main(url, output_csv):

    html = fetch_html(url)

    soup = BeautifulSoup(html, 'html.parser')

    header, header_avg = parse_table_header(soup)

    data = parse_table_data(soup)

    save_to_csv(data, header, header_avg, output_csv)
    print(f"CSV 파일로 저장이 완료되었습니다: {output_csv}")

if __name__ == "__main__":
    url = "https://www.koreabaseball.com/Record/Crowd/History.aspx"
    output_csv = "kbo_crowd_history.csv"
    main(url, output_csv)
