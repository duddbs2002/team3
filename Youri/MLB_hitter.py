import requests
from bs4 import BeautifulSoup
from team3_module import save_to_csv
import time
import random

# 1. 두 그룹의 URL
retire_hitter_group = [
    "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=64300",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=67341",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=76325",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=71564",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=77623",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=71752",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=70756",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=97109",
    # "https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId=95436"
]

hitter_group = [
    "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=76290",
    # "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=75125",
    # "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=51817",
    # "https://www.koreabaseball.com/Record/Player/HitterDetail/Total.aspx?playerId=76313"
]

# 요청 헤더 수정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 데이터 추출
def extract_data_from_url(url, css_selectors):
    """
    주어진 URL에서 CSS 선택자를 사용해 데이터를 추출하는 함수입니다.

    이 함수는 주어진 URL에 GET 요청을 보내고, HTML 콘텐츠를 BeautifulSoup으로 파싱합니다.
    지정된 CSS 선택자를 사용해 HTML 요소에서 텍스트를 추출합니다.

    매개변수:
    url (str): 데이터를 추출할 URL입니다. 유효한 웹 주소여야 합니다.
    css_selectors (dict): 키는 데이터 항목의 이름, 값은 CSS 선택자를 포함하는 딕셔너리입니다.

    반환값:
    dict: 추출된 데이터가 담긴 딕셔너리입니다. 각 키는 `css_selectors`의 키에 대응하며,
          값은 HTML 요소의 텍스트입니다. 요소를 찾을 수 없으면 'N/A'로 반환됩니다.
    requests.exceptions.RequestException: URL에 대한 HTTP 요청이 실패하면 발생할 수 있습니다.
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}
    for key, selector in css_selectors.items():
        element = soup.select_one(selector)
        data[key] = element.get_text(strip=True) if element else 'N/A'
        time.sleep(random.uniform(3,6))
    return data

# 각 그룹의 CSS 셀렉터 생성
retire_hitter_group_selector = {
    "name": "#cphContents_cphContents_cphContents_ucRetireInfo_lblName",
    "data": "#contents > div.sub-content > div.player_records > table.tData01.tt.mb5 > tbody"
}

# hitter_group_selector = {
#     "name": "#cphContents_cphContents_cphContents_playerProfile_lblName",
#     "data": "#contents > div.sub-content > div.player_records > div > table > tbody"
# }

# 데이터를 리스트에 저장
all_data = []

for url in retire_hitter_group:
    data = extract_data_from_url(url, retire_hitter_group_selector)
    all_data.append(data)

# for url in hitter_group:
#     data = extract_data_from_url(url, hitter_group_selector)
#     all_data.append(data)

# CSV 헤더 설정
headers = ["name", "data"]

# CSV로 저장
save_to_csv("메이저리그진출타자.csv", headers=headers, data=all_data)

print(f"Data successfully saved")