import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time 
import getpass
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

time.sleep(2) 
passwordF = driver.find_element(By.ID, "password") 
passwordF.send_keys(password) 

try:
    driver.find_element(By.NAME, "loginBtn").click() 
except:
    driver.find_element(By.ID, "recaptchaLoginBtn").click() 


time.sleep(2) 
driver.get("https://global.bookwalker.jp/holdBooks/") 
time.sleep(2) 
myName = driver.find_element(By.XPATH, "//*[@id='pc-hold-books-react-root']")
 

sourceFile = open('C:\\Users\\' + getpass.getuser() + '\\Downloads\\New folder\\export\\test.html', 'w', encoding="utf-8")
print(myName.get_attribute("innerHTML"), file = sourceFile)
sourceFile.close()
print(myName.get_attribute, "book-item fn-book-status")
driver.close()