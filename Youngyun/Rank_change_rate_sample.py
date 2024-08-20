from team3_module import open_url, get_logger, save_to_csv
from selenium import webdriver # Selenium WebDriver를 사용하여 웹 브라우저를 자동으로 제어합니다.
from selenium.webdriver.common.by import By # 요소를 찾기 위한 다양한 방법을 제공합니다. 
from selenium.webdriver.support.ui import WebDriverWait # 특정 조건이 만족될 때까지 대기할 수 있습니다.
from selenium.webdriver.support import expected_conditions as EC # 요소의 특정 조건을 정의합니다.
import time
import random
url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx" # KBO 일자별 팀순위 URL

driver = webdriver.Chrome() # Chrome 웹 브라우저를 제어하는 WebDriver 객체를 생성

logger = get_logger("Rank_change_rate")

def select_date(driver):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > div.yeardate > span:nth-child(3)"))
    )
    element.click()

    time.sleep(random.uniform(2, 4))

    month_AUG = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-datepicker-div > div > div > select.ui-datepicker-month"))
    )
    month_AUG.click()

    time.sleep(random.uniform(1, 4))

    month_MAR = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-datepicker-div > div > div > select.ui-datepicker-month > option:nth-child(3)"))
    )
    month_MAR.click()

    time.sleep(random.uniform(2, 5))

    date = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#ui-datepicker-div > table > tbody > tr:nth-child(4) > td:nth-child(7)"))
    )
    date.click()

def select_next_date(driver):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > div.yeardate > span:nth-child(3)"))
    )
    element.click()

                                                    
def extract_team_ranks(driver):
    # 테이블의 헤더를 추출하여 리스트에 저장
    headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > table > thead > tr > th")]
    # '일자'를 헤더 리스트의 첫 번째 항목으로 삽입
    headers.insert(0, '일자')

    # 데이터를 저장할 리스트 초기화
    data = []
    
    # 테이블의 모든 행을 선택하는 CSS 선택자
    rows = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > table > tbody > tr")
    
    # 날짜 타이틀 추출
    date_title = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_lblSearchDateTitle").text

    # 각 행의 데이터를 순회
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # 'td' 태그를 찾아 각 셀의 데이터를 가져옴
        row_data = [cell.text for cell in cells]  # 셀 데이터를 리스트로 저장
        
        # 각 행의 첫 번째 요소로 일자(날짜 타이틀)를 추가
        row_data.insert(0, date_title)
        
        # 데이터를 리스트에 추가
        data.append(row_data)
    
    return headers, data


def main():
    try:
        open_url(driver, url)

        time.sleep(random.uniform(3, 6))

        select_date(driver)

        time.sleep(random.uniform(4, 7))

        headers, data = extract_team_ranks(driver)

        filename = '2024_일자별순위(샘플).csv'

        save_to_csv(filename, headers=headers, data=data)

    except Exception as e:
        logger.error("An error occurred", exc_info=True)
    
    finally:
        driver.quit()

        
if __name__ == "__main__":
    main()
