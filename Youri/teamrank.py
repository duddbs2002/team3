from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging
import csv
import time
import random

# 주어진 함수들
def open_url(driver, url):
    driver.get(url)
    driver.set_window_size(1500, 1300)

def get_logger(logger_name, defalut_log_level=logging.DEBUG, console_log_level=logging.WARNING, \
               file_debug_log_level=logging.DEBUG, file_error_log_level=logging.ERROR, \
                debug_log_file="debug.log", error_log_file="error.log", encoding="utf-8"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(defalut_log_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    file_debug_handler = logging.FileHandler(f"{logger_name}.{debug_log_file}", encoding=encoding)
    file_debug_handler.setLevel(file_debug_log_level)
    file_error_handler = logging.FileHandler(f"{logger_name}.{error_log_file}", encoding=encoding)
    file_error_handler.setLevel(file_error_log_level)
    formatter = \
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_debug_handler.setFormatter(formatter)
    file_error_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_debug_handler)
    logger.addHandler(file_error_handler)

    return logger

def save_to_csv(path, mode="w", encoding="utf-8", newline="", *, headers=[], data=[]):
    with open(path, mode, encoding=encoding, newline=newline) as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        writer.writerows(data)

# 새로운 함수들
def scrape_team_rank(driver, logger):
    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx"
    open_url(driver, url)

    all_data = []
    headers = []

    # 2001년부터 2024년까지 데이터 수집
    for year in range(1982, 2025):
        # 드롭다운에서 연도 선택
        select = Select(driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_ddlYear"))
        select.select_by_value(str(year))

        # 2초에서 5초 사이에 랜덤하게 대기
        wait_time = random.uniform(3, 6)
        time.sleep(wait_time)

        # 테이블 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > table"))
        )

        # 헤더 가져오기 (한 번만 가져오기)
        if not headers:
            header_elements = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > table > thead > tr th")
            headers = ['Year'] + [header.text for header in header_elements]

        # 데이터 가져오기
        rows = driver.find_elements(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > table > tbody > tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [year] + [cell.text for cell in cells]
            all_data.append(row_data)

        # 디버그 로그 출력
        logger.debug(f"{year}년 데이터 수집 완료!")

    # CSV 파일로 저장
    save_to_csv("team_rank.csv", headers=headers, data=all_data)

def main():
    logger = get_logger("TeamRankScraper")
    driver = webdriver.Chrome()

    try:
        scrape_team_rank(driver, logger)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
