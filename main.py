import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time, getpass, os, sys
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

if (os.path.isfile((os.path.dirname(os.path.realpath(__file__))) + "\\.env")) == False:
    print("This program requires you to input your email and password only once.")
    print("To change email and password delete the .env that is created in the same directory as the program.")
    user_name = input("Enter your bookwalker Email: ")
    pass_word = input("Enter your bookwalker Password: ")
    sourceFile = open((os.path.dirname(os.path.realpath(__file__))) + "\\.env", 'w', encoding="utf-8")
    print("user_name=" + user_name, file = sourceFile)
    print("pass_word=" + pass_word, file = sourceFile)
    sourceFile.close()
    

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
table = []
myName = driver.find_elements(By.CSS_SELECTOR, ".md-book-list .book-tl-txt h2")

for myName2 in myName:
   table.append(myName2.get_attribute("innerHTML"))

sourceFile = open((os.path.dirname(os.path.realpath(__file__))) + '\\directory.html', 'w', encoding="utf-8")
print(table, file = sourceFile)
sourceFile.close()

print(table)
book_name = input("Enter your the link of the book you want: ")
driver.get(book_name) 
time.sleep(2) 

driver.find_element(By.PARTIAL_LINK_TEXT, 'Read on Browser').click() 
time.sleep(50) 

driver.close()