import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time, getpass, os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()
username = os.getenv('user_name') 
password = os.getenv('pass_word')

version_main = int(chromedriver_autoinstaller.get_chrome_version().split(".")[0])
chromeOptions = uc.ChromeOptions() 
chromeOptions.add_argument("--headless=new")
driver = uc.Chrome(uc.ChromeOptions())
driver.get("https://member.bookwalker.jp/app/03/login") 
uname = driver.find_element(By.ID, "mailAddress") 
uname.send_keys(username)  

time.sleep(5) 
passwordF = driver.find_element(By.ID, "password") 
passwordF.send_keys(password) 
time.sleep(2) 
try:
    driver.find_element(By.NAME, "loginBtn").click() 
except:
    driver.find_element(By.ID, "recaptchaLoginBtn").click() 
time.sleep(15) 
##program workaround for captcha

time.sleep(2) 
driver.get("https://global.bookwalker.jp/holdBooks/") 
time.sleep(2)  
myName = driver.find_element(By.CSS_SELECTOR, "div.md-book-list")

sourceFile = open((os.path.dirname(os.path.realpath(__file__))) + '\\export\\test.html', 'w', encoding="utf-8")
print(myName.get_attribute("innerHTML"), file = sourceFile)
sourceFile.close()
## if needed to check html functionality print(myName.get_attribute("innerHTML"))
driver.close()