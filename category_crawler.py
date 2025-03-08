import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm 
import random

for index, _cat2 in enumerate(["A0502"]):
    df = pd.read_csv("hanam_restaurant_real_url.csv", encoding='cp949')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    count = 0 #
    current = 0 #현재 진행 상황

    goal = len(df['name']) #총 식당 수

    #데이터 프레임으로 만들 빈 리스트 생성
    rev_list=[]


    for i in tqdm(range(len(df))): 
        
        current += 1
        print('진행상황 : ', current,'/',goal,sep="")
        
        try:
            # 식당 리뷰 개별 url 접속
            driver.get(df['naverURL'][i])
            thisurl = df['naverURL'][i]
            time.sleep(2)
            print('현재 수집중인 식당 : ', df['name'][i])
        except:
            print("exception at driver.get() / continue")
            continue
                
        #식당 평균 별점 수집
        try:
            possible_rating_text = driver.find_element(By.CLASS_NAME, "PXMot") # 얘 CLASS_NAME 바뀔 수도???
            rating_text = possible_rating_text.text.replace("별점", '')
        except:
            rating_text = ''
            pass
        
        try:
            #리뷰 데이터 스크래핑을 위한 html 파싱
            driver.switch_to.frame("entryIframe")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        except:
            print("no iframe. continue")
            continue
        
        try:
            # #app-root > div > div > div > div.place_section.no_margin.OP4V8 > div > div
            review_metadata = soup.select(".place_section")[0]
            # print(possible_review_lists.select('div > div')[1].get_text())
            # for l, _ in enumerate(review_metadata.select('div > div')):
            #     print(l, _.get_text())
        except ValueError:
            print("Strnage error. no '.place_section'")
            continue
        except:
            print("Even more strange error.")
            continue
        try:
            contains_visitor = True if ("방문자 리뷰" in review_metadata.select('div > div')[3].get_text()) else False
            if(contains_visitor == False):
                raise ValueError()
        except ValueError:
            print("no 방문자 리뷰")
            continue
        except:
            print("Even more strange error.")
            continue

        
        try:
            time.sleep(random.randint(0, 3))
            rev_category = soup.find(class_="lnJFt").text
            rev_list.append([df['name'][i], rev_category])

            print(str(i) + ' / ' + str(len(df)) + ' ' + df['name'][i] + ' ' + rev_category)
            time.sleep(1)

        except:
            time.sleep(random.randint(0, 3))
            rev_list.append([df['name'][i], ''])

            print(str(i) + ' / ' + str(len(df)) + ' ' + df['name'][i] + " no category??")
            time.sleep(1)
            
    driver.close()

    #스크래핑한 데이터를 데이터 프레임으로 만들기  
    column = ["name", "category"]
    df2 = pd.DataFrame(rev_list, columns=column)
    df2.to_csv("preprocessed_urls_hanam_restaurant_real_url_category_v7.csv", encoding='utf-8-sig')