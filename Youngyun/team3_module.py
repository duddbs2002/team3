from selenium import webdriver # Selenium WebDriver를 사용하여 웹 브라우저를 자동으로 제어합니다.
from selenium.webdriver.common.by import By # 요소를 찾기 위한 다양한 방법을 제공합니다. 
from selenium.webdriver.support.ui import WebDriverWait # 특정 조건이 만족될 때까지 대기할 수 있습니다.
from selenium.webdriver.support import expected_conditions as EC # 요소의 특정 조건을 정의합니다.
from selenium.webdriver.support.ui import Select # 드롭다운 목록을 제어하기 위한 Select 클래스를 제공합니다.
import logging
import csv
import time
import random

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
    
    """
    주어진 경로에 CSV 파일로 데이터를 저장하는 함수.

    지정된 파일 경로에 주어진 헤더와 데이터를 CSV 형식으로 저장합니다.

    매개변수:
        path (str): CSV 파일을 저장할 경로.
        mode (str, optional): 파일을 열 때 사용할 모드. 기본값은 "w" (쓰기 모드).
        encoding (str, optional): 파일 인코딩 방식. 기본값은 "utf-8".
        newline (str, optional): 파일에서 줄바꿈 문자를 처리하는 방식. 기본값은 "".
        headers (list, optional): CSV 파일의 첫 번째 행에 저장할 헤더 리스트. 기본값은 빈 리스트.
        data (list, optional): CSV 파일에 저장할 데이터가 담긴 리스트. 각 항목은 행을 나타내는 리스트입니다. 기본값은 빈 리스트.

    반환값:
        없음.

    """
    with open(path, mode, encoding=encoding, newline=newline) as file:
        if data[0] and isinstance(data[0], dict):
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            
        else:
            writer = csv.writer(file)
            writer.writerow(headers)

        for row in data:
            writer.writerow(row)

