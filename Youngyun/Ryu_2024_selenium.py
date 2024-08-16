from team3_module import open_url, get_logger
from selenium import webdriver # Selenium WebDriver를 사용하여 웹 브라우저를 자동으로 제어합니다.
from selenium.webdriver.common.by import By # 요소를 찾기 위한 다양한 방법을 제공합니다. 
from selenium.webdriver.support.ui import WebDriverWait # 특정 조건이 만족될 때까지 대기할 수 있습니다.
from selenium.webdriver.support import expected_conditions as EC # 요소의 특정 조건을 정의합니다.
from selenium.webdriver.support.ui import Select
import time
import random
import csv

year = '2024'

url = "https://statiz.sporki.com/player/?m=situation&p_no=10590" # 강서구야구소프트볼협회의 '팀 순위기록' 페이지 URL

driver = webdriver.Chrome() # Chrome 웹 브라우저를 제어하는 WebDriver 객체를 생성

logger = get_logger("Ryu")

def extract_player_stats(driver, year):
    headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, "body > div.warp > div.container > section > div.table_type02.transverse_scroll.cbox > table > tbody > tr:nth-child(1) > th:nth-child(1) > tr")]
    # 모든 데이터를 저장할 리스트
    data = []
    
    # 테이블의 모든 행을 선택하는 CSS 선택자
    rows = driver.find_elements(By.CSS_SELECTOR, "body > div.warp > div.container > section > div.table_type02.transverse_scroll.cbox > table > tbody > tr")
    
    # 각 행의 데이터를 추출
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # 'td' 태그를 찾아 각 셀의 데이터를 가져옴
        row_data = [cell.text for cell in cells]  # 셀 데이터를 리스트로 저장
        row_data.insert(0, year)  # 첫 번째 열에 연도 추가
        data.append(row_data)  # 데이터를 리스트에 추가
    
    return headers, data

def save_to_csv(path, headers, data, encoding="utf-8", newline=""):
    with open(path, mode="w", encoding=encoding, newline=newline) as file:
        writer = csv.writer(file)
        
        # 헤더가 있으면 헤더를 작성
        if headers:
            writer.writerow(headers)
        
        # 데이터를 작성
        writer.writerows(data)

def main():
    try:
        open_url(driver, url)

        time.sleep(7)

        headers, data_ryu = extract_player_stats(driver, year)

        filename = '류현진상세지표(샘플)'

        save_to_csv(filename, headers=headers, data=data_ryu)

    except Exception as e:
        logger.error("An error occurred", exc_info=True)
    
    finally:
        driver.quit()

        
if __name__ == "__main__":
    main()
