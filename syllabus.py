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

class Syllabus:
    #初期化処理
    def __init__(self):
        self.options = Options()
        #ブラウザ立ち上げは処理が重たくなるので本番環境ではheadlessモードを採用
        self.options.add_argument('--headless')
        self.options.add_argument('--window-size=1920,1080')
        #mac環境用
        self.driver = webdriver.Chrome(chrome_options=self.options)
        searchingADJa = {}

    def act(self,url,value):
        self.driver.get(url)
        term = self.driver.find_element_by_id("selTacTrmCd")
        select = Select(term)
        select.select_by_value("02")

        department = self.driver.find_element_by_id("selLsnMngPostCd")
        select = Select(department)
        select.select_by_value(value)

        day = self.driver.find_element_by_id("selTmtxCd")
        select = Select(day)
        select.select_by_value("A1")

        self.driver.find_element_by_xpath('//*[@id="contents"]/div[2]/input[1]').click()

        print('春学期：月曜1限スターーート！')

        classinfo = {}

        for num in range(2,8):
            sleep(1)
            self.driver.find_element_by_xpath(f'//*[@id="contents"]/div[1]/div[2]/table/tbody/tr[{num}]/td[1]/input[1]').click()

            classcode = self.driver.find_element_by_name('lblLsnCd').get_attribute("value")
            administrativedepartment = self.driver.find_element_by_name('lblAc119ScrDispNm').get_attribute("value")
            coursenumber = self.driver.find_element_by_name('lblRepSbjKnjNm').get_attribute("value")
            instructor = self.driver.find_element_by_name('lstChagTch_st[0].lblTchName').get_attribute("value")
            dayandperiod = self.driver.find_element_by_name('lstSlbtchinftJ002List_st[0].lblTmtxCd').get_attribute("value")
            grading = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[6]/tbody')

            classinfo.setdefault(classcode, { 
                '管理部署': administrativedepartment,
                '科目': coursenumber,
                '担当教授': instructor,
                '曜時': dayandperiod,
                '成績評価': grading.text,
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

        text = json.dumps(classinfo, sort_keys=True, ensure_ascii=False, indent=2)
        with open("Monday1.json", "wb") as f:
            f.write(text.encode("utf-8"))

        # 処理が終わったらwindowを閉じる
        self.driver.close()
        self.driver.quit()

        # return json
    # def open_url(self, url):
    #     self.driver.get(url)

    # def select_dropdown(self,value):
    #     # ドロップダウンのselectのときはclickを使わないほうが良いっぽい
    #     dropdown = self.driver.find_element_by_id("selLsnMngPostCd")
    #     select = Select(dropdown)
    #     select.select_by_value(value)

    # def submit(self):
    #     self.driver.find_element_by_xpath('//*[@id="contents"]/div[2]/input[1]').click()

    # def clcik_function(self):

    #   #htmlを調べる
    #     # page_source = self.driver.page_source
    #     # soup = BeautifulSoup(page_source, 'html.parser')

    #     # class_lists = soup.find_all("tr")[1:]

    #     # # function_lists = class_list.find_all("tr")
    #     # for class_list in class_lists:
    #     #   print(class_list.find_all("td")[6].text)
        
    #     self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/div[2]/table/tbody/tr[2]/td[1]/input[1]').click()

    # def print(self):
    #     classcode = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[1]/tbody/tr[1]/td[1]')
    #     administrativedepartment = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[1]/tbody/tr[3]/td')
    #     coursenumber = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[1]/tbody/tr[4]/td')
    #     instructor = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[1]/tbody/tr[6]/td')
    #     dayandperiod = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[8]/tbody/tr[2]/td[3]')
    #     grading = self.driver.find_element_by_xpath('//*[@id="contents"]/div[1]/table[6]/tbody')

        
    #     json = {
    #       classcode.text : {
    #       '管理部署': administrativedepartment.text,
    #       '科目': coursenumber.text,
    #       '担当教授': instructor.text,
    #       '曜時': dayandperiod.text,
    #       '成績評価': grading.text,
    #       }
    #     }
       
    #     print(json)

    # def scroll(self):
    #     self.driver.find_element_by_tag_name('body').click()
    #     self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)  

    #     self.driver.find_element_by_xpath('//*[@id="contents"]/div[2]/input').click()
        

        # 処理が終わったらwindowを閉じる
        # self.driver.close()
        # self.driver.quit()

    # def select_calender(self):
    #     #現在日時を取得して選択していく

    #     year = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/table[1]/tbody/tr[6]/td/div[2]/select[1]")
    #     selectyear = Select(year)
    #     currentyear = datetime.datetime.now().strftime('%Y')
    #     selectyear.select_by_value(currentyear)

    #     month = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/table[1]/tbody/tr[6]/td/div[2]/select[2]")
    #     selectmonth = Select(month)
    #     # 0埋めする。表示は05でもvalueの値は5になっている
    #     currentmonth = datetime.datetime.now().strftime('%-m')
    #     selectmonth.select_by_value(currentmonth)

    #     day = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/table[1]/tbody/tr[6]/td/div[2]/select[3]")
    #     selectday = Select(day)
    #     currentday = datetime.datetime.now().strftime('%-d')
    #     selectday.select_by_value(currentday)

    #     #表示ボタンクリック
    #     btn = self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/div[1]/a/div')
    #     btn.click()

    # def get_shift_list(self):
    #     #htmlを調べる
    #     page_source = self.driver.page_source
    #     soup = BeautifulSoup(page_source, 'html.parser')

    #     #シフトテーブルを選択。tableタグが他にもあるので配列から特定
    #     shift_list = soup.find_all("table")[5]

    #     #trタグからスタッフ一覧のみを取得。0,1には要らない要素が隠れているので排除。
    #     member_lists = shift_list.find_all("tr")[2:]

    #     #メンバー値を取得していく
    #     member_text = "知るカフェシフト表（笑）"
    #     for member_list in member_lists:
    #         # arr.append(f'@{member_list.find_all("td")[0].text} :{member_list.find_all("td")[1].text}')
    #         member_text+=(f'{member_list.find_all("td")[0].text} :{member_list.find_all("td")[1].text}') +"\n"
    #         # print(f'@{member_list.find_all("td")[0].text}')
    #         # print(f'出勤時間:{member_list.find_all("td")[1].text}')

    #     message = member_text
    #     payload = {'message': message}
    #     headers = {'Authorization': 'Bearer ' + line_notify_token}  # Notify URL
    #     line_notify = requests.post(line_notify_api, data=payload, headers=headers)


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


