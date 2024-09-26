from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re

driver = webdriver.Chrome()

stations = ["부전", "거제해맞이", "거제", "교대", "동래", "안락", "부산원동", "재송", "센텀", "벡스코", "신해운대", "송정", "오시리아", "기장", "일광", "좌천", "월내", "서생", "남창", "망양", "덕하", "개운포", "태화강", "북울산", "동해"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

stores = []
scores = []
stars = []
category = []

for station in stations:
    url = f'https://www.diningcode.com/list.dc?query={station}'
    driver.get(url)
    driver.implicitly_wait(10)

    foodInfos = driver.find_elements(By.CLASS_NAME, 'Info')
    for foodInfo in foodInfos:
        foods = foodInfo.find_elements(By.XPATH, '*')
        
        temp = []
        for index, food in enumerate(foods):
            if index == 0: temp.append(food.text.split(".")[-1])
            elif index == 1: temp.append(re.findall(r'\d+', food.text)[0])
            elif index == 3: temp.append(food.text)

    
for store in stores:
    print(store)

driver.quit()