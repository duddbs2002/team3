from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
import time

def fetch_html(driver):
    """현재 페이지의 HTML을 가져옵니다."""
    return driver.page_source

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
    driver = webdriver.Chrome()
    driver.get(url)
    driver.set_window_size(1500, 1300)

    try:
        season_select = Select(driver.find_element(By.ID, "cphContents_cphContents_cphContents_ddlSeason"))
        season_select.select_by_visible_text("2023")

        # 검색 버튼 클릭
        search_button = driver.find_element(By.ID, "cphContents_cphContents_cphContents_btnSearch")
        search_button.click()

        time.sleep(2)
        
        html = fetch_html(driver)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        header = parse_table_header(soup)
        
        data = parse_table_data(soup)
        
        save_to_csv(data, header, output_csv)
        print(f"CSV 파일로 저장이 완료되었습니다: {output_csv}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.koreabaseball.com/Record/Crowd/GraphDaily.aspx"
    output_csv = "daily_crowd_data_2324.csv"
    main(url, output_csv)
