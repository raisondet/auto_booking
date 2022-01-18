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
days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

# 웹페이지 설정
user_id = properties['USER']['id']
user_pw = properties['USER']['pwd']

# web url
url = properties['WEB']['url']
print(url)

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
  print('Select Date ============>', days[date-1])
  
  tr_idx = 2
  if date == SUN:
    tr_idx = 4    
    
  # 날짜 선택
  date_selector = "#cal > tbody > tr:nth-child(" + str(tr_idx) + ") > td:nth-child(" + str(date) + ") > a > span.label"
  date_btn = browser.find_element(By.CSS_SELECTOR, date_selector)
  date_btn.click()
  time.sleep(0.1)
  
def select_time():
  print('')
  print('Select Time ============>')
        
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
  i = 0
  for time_element in time_element_list: 
    # 색상
    elem = time_element.find_element(By.TAG_NAME, 'label')
    time_element_color = elem.value_of_css_property('color')
    # 가장 오전9시 이후로 예약
    if time_element_color == "rgba(34, 34, 34, 1)": 
      if i >= 3:
        elem.click()
        print("Select time!!!")
        select_flag = True
        break
      else:
        i = i + 1
        
  i = 0    
  if select_flag == False:
    for time_element in time_element_list: 
      # 색상
      elem = time_element.find_element(By.TAG_NAME, 'label')
      time_element_color = elem.value_of_css_property('color')
      # 가장 빠른 시간으로 예약
      if time_element_color == "rgba(34, 34, 34, 1)": 
        if i >= 0:
          elem.click()
          print("Select time!!!")
          select_flag = True
          break
        else:
          i = i + 1  
  time.sleep(0.1)
  
  # 다른날로 변경
  if select_flag == False:
    return False
  return True
      
def select_court():
  print('')
  print('Select Court ============>')

  available_court = "https://www.ksponco.or.kr/online/images/content/btn_tennis_court_off1.gif"
  
  # 하단 스크롤
  some_tag = browser.find_element(By.CLASS_NAME, 'tennis_court')
  action = ActionChains(browser)
  action.move_to_element(some_tag).perform()
  time.sleep(0.1)
  
  # 예약 가능한 첫번째 코트로 예약
  court_section_list = browser.find_element(By.CLASS_NAME, 'tennis_court')
  court_element_list = court_section_list.find_elements(By.TAG_NAME, "li")
  
  for court_element in court_element_list: 
    # 이미지
    elem = court_element.find_element(By.TAG_NAME, 'a')
    court_element_img = court_element.find_element(By.TAG_NAME, 'img').get_attribute('src')
    # 첫번째 코트로 예약
    if court_element_img == available_court: 
      print("-------- click")
      elem.click()
      break
    
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
  date_list = [FRI, SAT, SUN]  
  
  move_login_page()
  do_login()
  request_book()
  
  a = datetime.datetime.today().weekday()
    
  book_flag = False
  for d in date_list:
    print(d)
    select_date(d)
    if select_time():
      select_court()
      solve_captcha()
      book_flag = True
      break
     
  print('')
  print("*"*20) 
  if book_flag:  
    print("SUCCESS !!!!")
  else:
    print("FAIL !!!!")
  print("*"*20)
  
  browser.close()
  
if __name__ == "__main__":
  main()
  