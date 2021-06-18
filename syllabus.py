from selenium import webdriver
from time import sleep
import datetime
from selenium.webdriver.common.keys import Keys
#ActionChainsを使う時は、下記のようにActionChainsのクラスをロードする
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup, BeautifulStoneSoup
from selenium.webdriver.chrome.options import Options
import requests
import json

# mac環境用
import chromedriver_binary

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




class Syllabus:
    #初期化処理
    def __init__(self):
        self.options = Options()
        #ブラウザ立ち上げは処理が重たくなるので本番環境ではheadlessモードを採用
        # self.options.add_argument('--headless')
        self.options.add_argument('--window-size=1920,1080')
        #mac環境用
        self.driver = webdriver.Chrome(chrome_options=self.options)

        # Use a service account
        cred = credentials.Certificate('serviceAccount.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        # self.doc_ref = self.db.collection('subject')

    def act(self,url,value):
        self.driver.get(url)

        #履修期
        term = self.driver.find_element_by_id("selTacTrmCd")
        select = Select(term)
        select.select_by_value("02")

        #学部
        department = self.driver.find_element_by_id("selLsnMngPostCd")
        select = Select(department)
        select.select_by_value(value)

        #selector格納変数
        day_num = ["A","B","C","D","E","F","G"]
        week_num = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        count = 0
        for i in range(1,40):
            print(f'スターーーーと{i}番目')
            

            #6,7限スキップ処理
            if i % 6 == 0:
                count += 1
                i %= 6 
                i += 1
                print(f'{day_num[count]}{i}')
            elif i % 6 == 5:
                count += 1
                i %= 6
                i -= 4
            elif i >= 6:
                i %= 6 
                i += 1
                
            #曜時
            day = self.driver.find_element_by_id("selTmtxCd")
            select = Select(day)
            select.select_by_value(f'{day_num[count]}{i}')

            self.driver.find_element_by_xpath('//*[@id="contents"]/div[2]/input[1]').click()

            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            class_lists = soup.find_all("tr")[1:]
            max_num = len(class_lists)

            print(f'春学期：{week_num[count]}{i}限スターーート！')

            # 授業格納Object
            classinfo = {}

            self.driver.find_element_by_name
            for num in range(2,max_num+1):
                sleep(1)
                self.driver.find_element_by_xpath(f'//*[@id="contents"]/div[1]/div[2]/table/tbody/tr[{num}]/td[1]/input[1]').click()

                classcode = self.driver.find_element_by_name('lblLsnCd').get_attribute("value")
                administrativedepartment = self.driver.find_element_by_name('lblAc119ScrDispNm').get_attribute("value")
                coursenumber = self.driver.find_element_by_name('lblRepSbjKnjNm').get_attribute("value")
                instructor = self.driver.find_element_by_name('lstChagTch_st[0].lblTchName').get_attribute("value")
                dayandperiod = self.driver.find_element_by_name('lstSlbtchinftJ002List_st[0].lblTmtxCd').get_attribute("value")


                # doc_ref = self.db.collection('users').document('alovelace')
                # doc_ref.set({
                #     'first': 'Ada',
                #     'last': 'Lovelace',
                #     'born': 1815
                # })
                
                print(week_num[count])
                print(i)
                print(classcode)
                print(administrativedepartment)
                print(coursenumber)
                print(instructor)

                doc_ref = self.db.collection('subject')
                doc_ref.document(week_num[count]).collection(str(i)).document().set({
                    '授業コード': classcode,
                    '管理部署': administrativedepartment,
                    '科目': coursenumber,
                    '担当教授': instructor,
                    '曜時': dayandperiod
                })

                classinfo.setdefault(classcode, { 
                    '管理部署': administrativedepartment,
                    '科目': coursenumber,
                    '担当教授': instructor,
                    '曜時': dayandperiod,
                })


                # json = {
                # classcode : {
                # '管理部署': administrativedepartment,
                # '科目': coursenumber,
                # '担当教授': instructor,
                # '曜時': dayandperiod,
                # '成績評価': grading.text,
                # }
                # }
            
                
                print(f'jsonファイル{num-1}番目 : {classinfo}')

                
                sleep(1)
                self.driver.find_element_by_tag_name('body').click()
                self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)  
                sleep(1)

                self.driver.find_element_by_xpath('//*[@id="contents"]/div[2]/input').click()


            # Jsonファイル書き出し
            # text = json.dumps(classinfo, sort_keys=True, ensure_ascii=False, indent=2)
            # with open(f'{week_num[count]}{i}.json', "wb") as f:
            #     f.write(text.encode("utf-8"))
            
            #戻るボタンクリック
            self.driver.find_element_by_xpath('//*[@id="contents"]/div[2]/input').click()


        # 処理が終わったらwindowを閉じる
        self.driver.close()
        self.driver.quit()

        # return json
if __name__ == '__main__':
    driver = Syllabus()
    driver.act('https://syllabus.kwansei.ac.jp/uniasv2/UnSSOLoginControlFree',"26")
    # driver.open_url('https://syllabus.kwansei.ac.jp/uniasv2/UnSSOLoginControlFree')
    # driver.select_dropdown()
    # driver.submit()
    # driver.clcik_function()
    # driver.print()
    # driver.scroll()
    # driver.select_calender()
    # driver.get_shift_list()


