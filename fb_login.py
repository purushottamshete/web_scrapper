from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options 

driver = webdriver.Chrome()
driver.get("https://www.facebook.com")
print('Opened the facebook')
sleep(2)

username_box = driver.find_element(by=By.ID, value='email')
username_box.send_keys('purushottamshete@gmail.com')
print ("Email Id entered")
sleep(1)

password_box = driver.find_element(by=By.ID, value='pass')
password_box.send_keys('')
print ("Password entered")
sleep(2)

login_box = driver.find_element(by="class name", value="login")
login_box.click()
print ("Done")

print(driver.page_source)