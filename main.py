import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time, getpass, os, sys
from dotenv import load_dotenv
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

## Checks to see if login is saved
if (os.path.isfile((os.path.dirname(os.path.realpath(__file__))) + "\\.env")) == False:
    print("This program requires you to input your email and password only once.")
    print("To change email and password delete the .env that is created in the same directory as the program.")
    user_name = input("Enter your bookwalker Email: ")
    pass_word = input("Enter your bookwalker Password: ")
    sourceFile = open((os.path.dirname(os.path.realpath(__file__))) + "\\.env", 'w', encoding="utf-8")
    print("user_name=" + user_name, file = sourceFile)
    print("pass_word=" + pass_word, file = sourceFile)
    sourceFile.close()
    
## Loads email and password
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

print(table)
book_name = input("Enter your the link of the book you want: ")
driver.get(book_name) 
time.sleep(2) 

driver.find_element(By.PARTIAL_LINK_TEXT, 'Read on Browser').click() 
time.sleep(5)

page_count = int(str(driver.find_element(By.ID, 'pageSliderCounter').text).split('/')[1])
current_page_count = int(str(driver.find_element(By.ID, 'pageSliderCounter').text).split('/')[0])
print(page_count)

## Checks if export directory exists. If not it creates one.

if (os.path.exists((pathfinder) + "\\export")) == False:
    os.mkdir(str((pathfinder) + "\\export"))

if (os.path.exists((pathfinder) + "\\export")) == False:
    print("directory creation failed")
else:
    print("directory creation successful")

canvas = driver.find_element(By.CSS_SELECTOR, "#viewer")
action = ActionChains(driver)
element1 = driver.find_element(By.CSS_SELECTOR, "#menu")
element2 = driver.find_element(By.CSS_SELECTOR, "#pageSlider")
  
## Goes through manga and captures images

for i in range(1, ((int(str(current_page_count)))+2)):
    action.click(on_element = canvas)
    action.send_keys(Keys.PAGE_UP)
    action.perform()
    
for i in range(1, (((int(str(page_count)))//2)+2)):
    print(i)
    time.sleep(3)
    driver.save_screenshot(((pathfinder) + "\\export\\" + str(i) + ".png"))
    action.send_keys(Keys.PAGE_DOWN)
    action.perform()
else:
    print("Completed?")

## Makes Images into PDF

images = [
    Image.open(str(pathfinder) + "\\export\\" + str(f) + ".png").convert('RGB')
    for f in range(1, (((int(str(page_count)))//2)+1)) 
]

images[0].save(pathfinder + "\\manga.pdf", "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

time.sleep(10) 

driver.close()