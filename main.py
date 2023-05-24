import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time 
from selenium.webdriver.common.by import By
version_main = int(chromedriver_autoinstaller.get_chrome_version().split(".")[0])

username="insert-username"; 
password="insert-password" 
chromeOptions = uc.ChromeOptions() 
chromeOptions.headless = True 
driver = uc.Chrome()
driver.get("https://member.bookwalker.jp/app/03/login") 
uname = driver.find_element(By.ID, "mailAddress") 
uname.send_keys(username)  

time.sleep(5) 
passwordF = driver.find_element(By.ID, "password") 
passwordF.send_keys(password) 


driver.find_element(By.NAME, "loginBtn").click() 

##recaptchaLoginBtn

time.sleep(2) 
driver.get("https://global.bookwalker.jp/holdBooks/") 
time.sleep(2) 
myName = driver.find_element(By.NAME, "md-book-list md-series-list") 
 
print("Profile Name: " + myName.get_attribute("innerHTML")) 
driver.close()
