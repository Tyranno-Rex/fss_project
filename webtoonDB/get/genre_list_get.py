from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Selenium 설정
options = Options()
options.headless = True  # 브라우저를 띄우지 않고 실행할 경우

Genre_list = ['로멘스', '판타지', '액션', '일상', '스릴러', '개그', '무협/사극', '드라마',
        '감성', '스포츠', '연도별웹툰', '브랜드웹툰', '드라마&영화 원작웹툰', '먼치킨',
        '학원로멘스', '로판', '게임판타지', '오피스로맨스', '하이퍼리얼리즘', '캠퍼스로맨스',
        'sf', '야구', '까칠남', '걸크러쉬', '재벌', '머니게임', '의학드라마']



# 브라우저 열기
driver = webdriver.Chrome(options=options)
for i in range(0, len(Genre_list)):
    driver.get('https://comic.naver.com/webtoon?tab=genre&genre={0}'.format(Genre_list[i]))

    # 페이지가 로딩될 때까지 기다리기 (예: 5초)
    driver.implicitly_wait(5)
    time.sleep(5)

    total_li_list = []

    # # 스크롤을 끝까지 내리기
    while True:
        # 현재 찾은 li 요소의 개수
        current_li_count = len(driver.find_elements(By.CSS_SELECTOR, 'div.component_wrap ul > li'))

        # 스크롤을 끝까지 내리기
        action = driver.find_element(By.TAG_NAME, 'body')
        action.send_keys(Keys.END)
        for i in range(15):
            action.send_keys(Keys.ARROW_UP)

        # 새로운 li 요소들이 로딩될 때까지 기다리기
        time.sleep(5)  # 페이지가 로딩되는 동안 대기

        # 새로운 li 요소들 가져오기
        li_elements = driver.find_elements(By.CSS_SELECTOR, 'div.component_wrap ul > li')
        # print(li_elements)
        total_li_list += li_elements
        # 새로운 li 요소가 더 이상 로딩되지 않으면 반복 종료
        
        if len(li_elements) == current_li_count:
            break

    driver.execute_script('window.scrollTo(0, 0)')

    import pymongo
    from pymongo import MongoClient

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    db_genre = []
    # MongoDB 연결
    client = MongoClient('localhost', 27017)
    db = client['fsdb_naver']  # 여기에는 사용할 데이터베이스의 이름을 입력하세요
    collection = db['Genre_{0}'.format(Genre_list[i])]  # 여기에는 사용할 컬렉션의 이름을 입력하세요

    # 위에서 사용한 코드를 그대로 가져와서 MongoDB에 데이터 넣기
    for index in range(1, 1000):
        title_selector = f'div.component_wrap ul > li:nth-child({index}) > div > a > span > span'
        title_span = soup.select_one(title_selector)
        
        if title_span is None:
            break
        if title_span:
            genre_data = {'index': index, 'title': title_span.text}
            collection.insert_one(genre_data)

client.close()  # MongoDB 연결 종료

driver.quit()