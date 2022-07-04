from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

USERNAME = 'klamchukmoney@gmail.com'
PASSWORD = 'muxtar15'

chrome_driver_path = "/Users/arturmacos/Downloads/chromedriver"
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

driver.get("https://tinder.com/")
cookie1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button')
cookie1.click()

sleep(2)
login_button = driver.find_element(By.XPATH, '//*[@id="q1028785088"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a')
login_button.click()

sleep(2)
facebook_auth = driver.find_element(By.XPATH, '//*[@id="q-699595988"]/div/div/div[1]/div/div/div[3]/span/div[2]/button')
facebook_auth.click()


cookie2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[1]')
cookie2.click()

sleep(2)
login_email = driver.find_element(By.ID, 'email')
login_email.send_keys(USERNAME)

login_pass = driver.find_element(By.ID, 'pass')
login_pass.send_keys(PASSWORD)


#Allow location
allow_location_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
allow_location_button.click()

#Disallow notifications
notifications_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notifications_button.click()

#Allow cookies
cookies = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookies.click()

#
#
# sleep(2)
# login_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/header/div[1]/div[2]/div/button')
# login_button.click()
#
# sleep(2)
# fb_login = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
# fb_login.click()
#
# #Switch to Facebook login window
# sleep(2)
# base_window = driver.window_handles[0]
# fb_login_window = driver.window_handles[1]
# driver.switch_to.window(fb_login_window)
# print(driver.title)
#
# #Login and hit enter
# email = driver.find_element(By.XPATH, '//*[@id="email"]')
# password = driver.find_element(By.XPATH, '//*[@id="pass"]')
# email.send_keys(USERNAME)
# password.send_keys(PASSWORD)
# password.send_keys(Keys.ENTER)
#
# #Switch back to Tinder window
# driver.switch_to.window(base_window)
# print(driver.title)


