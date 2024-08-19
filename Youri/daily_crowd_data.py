import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html(url):
    """URL에서 HTML을 가져옵니다."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_table_header(soup):
    """테이블의 헤더를 파싱합니다."""
    thead = soup.select_one("#cphContents_cphContents_cphContents_udpRecord > table > thead > tr")
    if thead:
        header = [th.text.strip() for th in thead.find_all("th")]
    else:
        header = []
    
    return header

def parse_table_data(soup):
    """테이블의 데이터를 파싱합니다."""
    tbody = soup.select_one("#cphContents_cphContents_cphContents_udpRecord > table > tbody")
    rows = tbody.find_all("tr") if tbody else []
    
    data = []
    for row in rows:
        cols = row.find_all("td")
        row_data = [col.text.strip() for col in cols]
        data.append(row_data)
    
    return data

def save_to_csv(data, header, filename):
    """데이터를 CSV 파일로 저장합니다."""
    df = pd.DataFrame(data, columns=header)
    df.to_csv(filename, index=False, encoding='utf-8')

def main(url, output_csv):
    """메인 함수 - 전체 스크래핑 작업을 수행합니다."""
    # HTML 가져오기
    html = fetch_html(url)
    
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html, 'html.parser')
    
    # 헤더 파싱
    header = parse_table_header(soup)
    
    # 데이터 파싱
    data = parse_table_data(soup)
    
    # CSV 파일로 저장
    save_to_csv(data, header, output_csv)
    print(f"CSV 파일로 저장이 완료되었습니다: {output_csv}")

# 실행
if __name__ == "__main__":
    url = "https://www.koreabaseball.com/Record/Crowd/GraphDaily.aspx"
    output_csv = "daily_crowd_data.csv"
    main(url, output_csv)
