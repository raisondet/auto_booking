from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from twocaptcha import TwoCaptcha

import time
import pyautogui
import pyperclip
import datetime
import sys
import os
import platform
import configparser as parser

# 프로퍼티 읽기
properties = parser.ConfigParser()
properties.read('./config.ini', encoding='utf-8')

# OS 확인
platform_os = platform.system()

# 요일 설정
SUN = 1
MON = 2
TUE = 3
WED = 4
THU = 5
FRI = 6
SAT = 7
days = {"SUN":SUN, "MON":MON, "TUE":TUE, "WED":WED, "THU":THU, "FRI":FRI, "SAT":SAT}

# 웹페이지 설정
user_id = properties['USER']['id']
user_pw = properties['USER']['pwd']

# web url
url = properties['WEB']['url']
print("Connect URL : {}".format(url))

# 브라우져 설정
browser_type = properties['BROWSER']['type']
if browser_type == "firefox":
  driver_path = "/opt/homebrew/bin/geckodriver"
  s= Service(driver_path)
  browser = webdriver.Firefox(service=s)
else:
  if platform_os == "Windows":
    driver_path = "C:\chromedriver.exe"
  else:
    driver_path = "/Users/c._.hwan/Documents/chromedriver"
  
  s= Service(driver_path)
  browser = webdriver.Chrome(service=s)
browser.implicitly_wait(10) # 페이지가 로딩될때까지 최대 10초 기다려줌
#browser.maximize_window() # 화면 최대화
browser.get(url)

def move_login_page():
  # selector 설정
  login = "#header > div.top_area > ul > li:nth-child(1) > a"
  
  # 로그인
  login_btn = browser.find_element(By.CSS_SELECTOR, login)
  login_btn.click()
  time.sleep(1)
      
def do_login():
  # selector 설정
  id_sellector = "#user_id"
  pw_sellector = "#user_pwd"
  login_selector = "#frm > div > div > div > a.btn_base.on"

  # 아이디 입력창
  id = browser.find_element(By.CSS_SELECTOR, id_sellector)
  id.click()
  #pyperclip.copy(user_id)
  #pyautogui.hotkey("ctrl", "v")
  id.send_keys(user_id)
  time.sleep(0.1)

  # 비밀번호 입력창
  pw = browser.find_element(By.CSS_SELECTOR, pw_sellector)
  pw.click()
  #pyperclip.copy(user_pw)
  #pyautogui.hotkey("ctrl", "v")
  pw.send_keys(user_pw)
  time.sleep(0.1)

  # 로그인 버튼
  login_btn = browser.find_element(By.CSS_SELECTOR, login_selector)
  login_btn.click()
  time.sleep(0.1)
  
def request_book():
  request_selector = "#content > div.section.info_area01 > div > div.info_con01 > a"
  request_btn = browser.find_element(By.CSS_SELECTOR, request_selector)
  request_btn.click()
  time.sleep(0.1)

def select_date(date):  
  print('')
  print('============> Date : {}'.format(date))
  
  tr_idx = 4    
  # 날짜 선택
  date_selector = "#cal > tbody > tr:nth-child(" + str(tr_idx) + ") > td:nth-child(" + str(days[date]) + ") > a > span.label"
  date_btn = browser.find_element(By.CSS_SELECTOR, date_selector)
  print("가능여부 : {}".format(date_btn.get_attribute('innerHTML')))
  if date_btn.get_attribute('innerHTML') == "가능 0건": 
    return False
  
  date_btn.click()
  time.sleep(0.1)
  return True
  
def select_time():
  print('')
  print('============> Time')
        
  # 하단 스크롤
  some_tag = browser.find_element(By.ID, 'time_con')
  action = ActionChains(browser)
  action.move_to_element(some_tag).perform()
  
  # 예약 가능한 가장 빠른 시간 클릭
  time_section_list = browser.find_element(By.CLASS_NAME, 'list_time')
  time_element_list = time_section_list.find_elements(By.TAG_NAME, "li")
  #time_element_list = map(lambda time_section: time_section.find_elements(By.TAG_NAME, "li"), time_section_list)
  #flatten_time_element_list = [y for x in list(time_element_list) for y in x]
  
  select_flag = False
  select_cnt = 0
  for idx, time_element in enumerate(time_element_list): 
    # 색상
    elem = time_element.find_element(By.TAG_NAME, 'label')
    time_element_color = elem.value_of_css_property('color')
    # 오전9시 이후로 예약
    if time_element_color == "rgba(34, 34, 34, 1)": 
      if idx >= 3:
        print("Select time : {}".format(idx))
        elem.click()
        select_cnt = select_cnt + 1
        if select_cnt >= 2:
          select_flag = True
          break
          
  if select_flag == False:
    select_cnt = 0
    for idx, time_element in enumerate(time_element_list): 
      # 색상
      elem = time_element.find_element(By.TAG_NAME, 'label')
      time_element_color = elem.value_of_css_property('color')
      # 가장 빠른 시간으로 예약
      if time_element_color == "rgba(34, 34, 34, 1)": 
        if idx >= 0:
          elem.click()
          print("Select time : {}".format(idx))
          select_cnt = select_cnt + 1
          if select_cnt >= 2:
            break
  
  # 다른날로 변경
  if select_cnt > 0:
    return True
  return False
      
def select_court():
  time.sleep(0.2)
  print('')
  print('============> Court')

  available_court = "https://www.ksponco.or.kr/online/images/content/btn_tennis_court_off1.gif"
  
  # 하단 스크롤
  some_tag = browser.find_element(By.CLASS_NAME, 'time_conf')
  action = ActionChains(browser)
  action.move_to_element(some_tag).perform()
  
  court_section_list = browser.find_element(By.CLASS_NAME, 'tennis_court')
  court_flag = False
  
  # 실내코트 먼저 예약
  for idx in [5, 6, 7, 8]:
    in_court = court_section_list.find_element(By.CLASS_NAME, 't_list' + str(idx))
    elem = in_court.find_element(By.TAG_NAME, 'a')
    img_elem = in_court.find_element(By.TAG_NAME, 'img')
    court_element_img = img_elem.get_attribute('src')
    # 첫번째 코트로 예약
    if court_element_img == available_court: 
      print("Select in-court : {}".format(img_elem.get_attribute('alt')))
      elem.click()
      court_flag = True
      break
    
  # 예약 가능한 첫번째 코트로 예약
  if court_flag == False:
    court_element_list = court_section_list.find_elements(By.TAG_NAME, "li") 
    for court_element in court_element_list: 
      # 이미지
      elem = court_element.find_element(By.TAG_NAME, 'a')
      img_elem = court_element.find_element(By.TAG_NAME, 'img')
      court_element_img = img_elem.get_attribute('src')
      # 첫번째 코트로 예약
      if court_element_img == available_court: 
        print("Select out-court : {}".format(img_elem.get_attribute('alt')))
        elem.click()
        court_flag = True
        break
      
  result_elem = browser.find_element(By.CSS_SELECTOR, '#captcha')
  result_elem.click()
  return court_flag
    
def solve_captcha():
  print('')
  print('Solve Captcha ============>')

  # 하단 스크롤
  some_tag = browser.find_element(By.CLASS_NAME, 'captchaImg_wrap')
  action = ActionChains(browser)
  action.move_to_element(some_tag).perform()
  
  start = time.time()
  # 캡챠 스크린샷을 captcha.png 파일로 쓴다.  
  captcha_png = browser.find_element(By.CSS_SELECTOR, '#captchaImg').screenshot_as_png
  with open('captcha.png', 'wb') as file:
      file.write(captcha_png)

  # 2Captcha 서비스에 캡챠 해결을 요청한다.
  api_key = properties['API']['key']
  solver = TwoCaptcha(api_key)
  try:
      result = solver.normal('captcha.png')
      result_code = result['code']
      print(result_code)

  except Exception as e:
      browser.close()
      sys.exit(e)

  print("captcha solve time :", time.time() - start)

  # 위에서 가져온 Captcha 값을 작성한다.
  result_elem = browser.find_element(By.CSS_SELECTOR, '#captcha')
  result_elem.click()
  #pyperclip.copy(result_code)
  #pyautogui.hotkey("ctrl", "v")
  result_elem.send_keys(result_code)
  
  # 확인
  confirm_elem = browser.find_element(By.CSS_SELECTOR, '#date_confirm')
  confirm_elem.click()
  time.sleep(0.1)
  
  # alert창 확인
  browser.switch_to.alert.accept()
  
def main():
  date_list = properties['DAY']['day'].split(',')
  
  move_login_page()
  do_login()
  request_book()
  
  a = datetime.datetime.today().weekday()
    
  book_flag = False
  for d in date_list:
    if select_date(d):
      if select_time():
        if select_court():
          #solve_captcha()
          book_flag = True
          break
     
  print('')
  print("*"*20) 
  if book_flag:  
    print("SUCCESS !!!!")
  else:
    print("FAIL !!!!")
  print("*"*20)
  
  #browser.close()
  
if __name__ == "__main__":
  main()
  