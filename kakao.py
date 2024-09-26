from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

url = 'https://map.kakao.com/'
driver = webdriver.Chrome()  # 드라이버 경로
driver.get(url)

stations = ["부전 맛집", "거제 해맞이 맛집", "거제 맛집", "교대 맛집", "동래 맛집", "안락 맛집", "부산원동 맛집", "재송 맛집", "센텀 맛집", "벡스코 맛집", "신해운대 맛집", "송정 맛집", "오시리아 맛집", "기장 맛집", "일광 맛집", "좌천 맛집", "월내 맛집", "서생 맛집", "남창 맛집", "망양 맛집", "덕하 맛집", "개운포 맛집", "태화강 맛집", "북울산 맛집", "동해 맛집"]


# 음식점 입력 후 찾기 버튼 클릭 

for index, station in enumerate(stations): 
    search_area = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')   # 검색창

    # 기존 검색어 지우기
    search_area.clear()

    search_area.send_keys(station)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
    time.sleep(2)

    # 장소 버튼 클릭 
    driver.find_element(By.XPATH, '//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)

    
    def storeNamePrint(page, is_first_page):
        time.sleep(0.2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        store_lists = soup.select('.placelist > .PlaceItem')
        list = []
       
        for store in store_lists:
            temp = []
            name = store.select('.head_item > .tit_name > .link_name')[0].text
            category = store.select('.head_item > .subcategory')[0].text
            degree = store.select('.rating > .score > .num')[0].text
            addr = store.select('.info_item > .addr')[0].text.splitlines()[1]  # 도로명주소 
            tel = store.select('.info_item > .contact > .phone')[0].text
            peroid = store.select('.periodWarp a')[0].text

            temp.append(name)
            temp.append(category)
            temp.append(degree)
            temp.append(addr)
            temp.append(tel)
            temp.append(peroid)
            list.append(temp)
            
        if is_first_page:  # 첫 역 첫 페이지일 때 헤더를 추가합니다.
            f = open('store_list_1.csv', 'w', encoding='utf-8-sig', newline='')  # 파일명 써주기 
            writercsv = csv.writer(f)
            header = ['name', 'category', 'degree', 'address', 'tel', 'peroid']
            writercsv.writerow(header)

            for i in list:
                writercsv.writerow(i)
        else:   
            # 파일이 이미 존재하므로, 존재하는 파일에 이어서 쓰기 
            f = open('store_list_1.csv', 'a', encoding='utf-8-sig', newline='')
            writercsv = csv.writer(f)
            for i in list:
                writercsv.writerow(i)
    
    # 첫 번째 역의 첫 번째 페이지에서만 헤더를 추가하기 위해 index==0 and page==1 조건을 적용
    storeNamePrint(1, index == 0 and True)

    try:
        # 장소 더보기 버튼 누르기 
        btn = driver.find_element(By.CSS_SELECTOR, '.more')   
        driver.execute_script("arguments[0].click();", btn)

        for i in range(2, 7):
            # 페이지 넘기기
            xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
            driver.find_element(By.XPATH, xPath).send_keys(Keys.ENTER)
            time.sleep(1)

            storeNamePrint(i, False)
    except:
        print('ERROR!')

    print('**크롤링 완료**')

driver.quit()
