## wait until fixed causing distutils error 
import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time, os
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


try:
    os.mkdir(((os.path.expanduser('~')) + "\\AppData\\Roaming\\Manga_Recover\\"))
except:
    print("AppData Directory already created")

try:
    os.mkdir(((os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\'))
except:
    print("Download Directory already created")

## Checks to see if login is saved
if ((os.path.isfile((os.path.expanduser('~')) + "\\AppData\\Roaming\\Manga_Recover\\.env")) == False) or (os.path.getsize((os.path.expanduser('~')) + "\\AppData\\Roaming\\Manga_Recover\\.env")) == 0:
    print("This program requires you to input your email and password only once.")
    print("To change email and password delete the .env that is created in the same directory as the program.")
    user_name = input("Enter your bookwalker Email: ")
    pass_word = input("Enter your bookwalker Password: ")
    sourceFile = open(((os.path.expanduser('~')) + "\\AppData\\Roaming\\Manga_Recover\\.env"), 'w', encoding="utf-8")
    print("user_name=" + user_name, file = sourceFile)
    print("pass_word=" + pass_word, file = sourceFile)
    sourceFile.close()
else:
    print("A Username and Password have been previously stored in appdata.\n\n" + "To change password delete .env file")

## Loads email and password
load_dotenv((os.path.expanduser('~')) + "\\AppData\\Roaming\\Manga_Recover\\.env")
username = os.getenv('user_name') 
password = os.getenv('pass_word')


try:
    chromeOptions = uc.ChromeOptions() 
    chromeOptions.add_argument("--headless=new")
        # Adding argument to disable the AutomationControlled flag 
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    chromeOptions.add_experimental_option("useAutomationExtension", False) 
    driver = uc.Chrome(uc.ChromeOptions())
    browser_status=0
except:
    print("UC Chrome failed switching to Chrome")
    browser_status = 1
    try:
        chromeOptions = uc.ChromeOptions() 
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)
    except:
        print("Chrome failed switching to Firefox")
        browser_status = 2
        try:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        except:
            print("Firefox failed - All drivers have error")
        driver.minimize_window()


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
## need to program workaround for captcha

## Collects book list and displays it in console window

time.sleep(2) 
driver.get("https://global.bookwalker.jp/holdBooks/") 
time.sleep(2)  
table = []
myName = driver.find_elements(By.CSS_SELECTOR, ".md-book-list .book-tl-txt h2")
pathfinder = os.path.dirname(os.path.realpath(__file__))


for myName2 in myName:
   table.append(myName2.get_attribute("innerHTML"))

sourceFile = open((pathfinder) + '\\directory.html', 'w', encoding="utf-8")
print(table, file = sourceFile)
sourceFile.close()
driver.minimize_window()

driver.get(pathfinder + "\\directory.html") 
print(table)
time.sleep(2)
skipselect = input("Insert link to skip selection or leave empty to see selection")
if not skipselect:
    book_name = input("Enter the link of the book you want: ")
    driver.get(book_name) 
    time.sleep(2) 

    driver.maximize_window()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "gdpr-accept").click()
    try:   
        driver.find_element(By.PARTIAL_LINK_TEXT, 'Read on Browser').click() 
    except:
        driver.find_element(By.CSS_SELECTOR, ".a-read-on-btn").click() 
    time.sleep(5)
else:
    driver.get(skipselect) 
    time.sleep(2) 
    driver.maximize_window()
    time.sleep(5)
page_count = int(str(driver.find_element(By.ID, 'pageSliderCounter').text).split('/')[1])
current_page_count = int(str(driver.find_element(By.ID, 'pageSliderCounter').text).split('/')[0])
print(page_count)

## Checks if export directory exists. If not it creates one.

if (os.path.exists((os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\export')) == False:
    os.mkdir(str((os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\export'))

if (os.path.exists((os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\export')) == False:
    print("directory creation failed")
else:
    print("directory creation successful")

canvas = driver.find_element(By.CSS_SELECTOR, "#viewer")
action = ActionChains(driver)
element1 = driver.find_element(By.CSS_SELECTOR, "#menu")
element2 = driver.find_element(By.CSS_SELECTOR, "#pageSlider")
  
## Goes through manga and captures images
##make images and other stuff export to folder named after manga

for i in range(1, ((int(str(current_page_count)))+2)):
    action.click(on_element = canvas)
    action.send_keys(Keys.PAGE_UP)
    action.perform()
    
for i in range(1, (((int(str(page_count)))//2)+2)):
    print(i)
    time.sleep(3)
    ##way to get progress for bar (str(i) + "/" + (str((page_count//2)+2)) + "Pages"))
    driver.save_screenshot(((os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\export\\') + str(i) + ".png")
    ##make it set to page one instead of clicking through
    action.send_keys(Keys.PAGE_DOWN)
    action.perform()
else:
    print("Completed?")

## Makes Images into PDF

images = [
    Image.open((str(os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\export\\') + str(f) + ".png").convert('RGB')
    for f in range(1, (((int(str(page_count)))//2)+1)) 
    ]

images[0].save((str(os.path.expanduser('~')) + '\\Downloads\\Manga_Recover\\export\\') + "\\manga.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

time.sleep(10) 

driver.close()
