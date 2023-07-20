import undetected_chromedriver as uc 
import chromedriver_autoinstaller
import time, os
from dotenv import load_dotenv
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import customtkinter


pathfinder = os.path.dirname(os.path.realpath(__file__))
version_main = int(chromedriver_autoinstaller.get_chrome_version().split(".")[0])
chromeOptions = uc.ChromeOptions() 
chromeOptions.add_argument("--headless=new")
driver = uc.Chrome(uc.ChromeOptions())
driver.minimize_window()


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Manga_Recover")

        self.iconbitmap(pathfinder + "\\icon.ico")
        self.textbox = customtkinter.CTkTextbox(self, width=420)
        

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with Dev info
        self.sidebar_frame = customtkinter.CTkFrame(self, width=280, corner_radius=0) 
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Manga_Recover", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.update_label = customtkinter.CTkLabel(self.sidebar_frame, text="0/0", font=customtkinter.CTkFont(size=15, weight="normal"))
        self.update_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.instruction_label = customtkinter.CTkLabel(self.sidebar_frame, text="1. Login\n\n" + "2. Hit Retrieve Data and Wait for list to appear\n\n" + "3. Enter URL\n\n" + "4. Click Scan and Wait for Completion", font=customtkinter.CTkFont(size=12, weight="normal"))
        self.instruction_label.grid(row=2, column=0, padx=20, pady=(80, 10))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Created by Silver0006", font=customtkinter.CTkFont(size=10, weight="normal"))
        self.logo_label.grid(row=5, column=0, padx=20, pady=(20, 10))


        # create textbox
        self.textbox.insert("0.0", "")
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        
        ## creates login
        self.username = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username.grid(row=1, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.password = customtkinter.CTkEntry(self, placeholder_text="Password")
        self.password.grid(row=2, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.login_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text="Login", text_color=("gray10", "#DCE4EE",), command=self.login_button_event)
        self.login_button.grid(row=3, column=1, padx=(20, 20), pady=(20, 20))
        self.retrieve_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text="Retrieve Data", text_color=("gray10", "#DCE4EE",), command=self.retrieve_button_event)
        self.retrieve_button.grid(row=3, column=2, padx=(20, 20), pady=(20, 20))
        

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Manga URL")
        self.entry.grid(row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.scan_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text="Scan", text_color=("gray10", "#DCE4EE"), command=self.URL_button_event)
        self.scan_button.grid(row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")



    def login_button_event(self):
        if ((os.path.isfile((os.path.dirname(os.path.realpath(__file__))) + "\\.env")) == False) or (os.path.getsize(((os.path.dirname(os.path.realpath(__file__))) + "\\.env")) == 0):
            print("Login started")
            sourceFile = open((os.path.dirname(os.path.realpath(__file__))) + "\\.env", 'w', encoding="utf-8")
            print("user_name=" + self.username.get(), file = sourceFile)
            print("pass_word=" + self.password.get(), file = sourceFile)
            sourceFile.close()
        else:
            self.textbox.delete(0, 'end')
            self.textbox.configure(state="normal")
            self.textbox.insert("0.0", "A Username and Password have been previously stored.\n\n" + "To change password delete .env file")
            self.textbox.configure(state="disabled")
        
    def retrieve_button_event(self): 
        driver.maximize_window()
        load_dotenv()
        username = os.getenv('user_name') 
        password = os.getenv('pass_word')

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
        self.textbox.delete(0, 'end')
        self.textbox.configure(state="normal")
        self.textbox.insert("0.0", table)
        self.textbox.configure(state="disabled")
        print("log should be displayed")
        time.sleep(2)

    def URL_button_event(self):
        driver.maximize_window()
        driver.get(self.entry.get()) 
        time.sleep(2) 

        try:   
            driver.find_element(By.PARTIAL_LINK_TEXT, 'Read on Browser').click() 
        except:
            driver.find_element(By.CSS_SELECTOR, "p.btn-read.m-b20").click() 
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
            print(str(str(i) + "/" + (str((page_count//2)+2))))
            self.update_label.configure(text=(str(i) + "/" + (str((page_count//2)+2))))
            self.update()
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
        self.update_label.configure(text="Complete")
        self.update()
        time.sleep(10) 
        driver.close()





if __name__ == "__main__":
    app = App()
    app.mainloop()

