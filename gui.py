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

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Manga_Recover")

        self.iconbitmap(pathfinder + "\\icon.ico")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with Dev info
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Manga_Recover", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Manga URL")
        self.entry.grid(row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.URL_button_event)
        self.main_button_1.grid(row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        ## creates login
        self.username = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.password = customtkinter.CTkEntry(self, placeholder_text="Password")
        self.password.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.login_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text="Login", text_color=("gray10", "#DCE4EE",), command=self.login_button_event)
        self.login_button.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.insert("0.0", "1. Login\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.")
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")



    def login_button_event(self):
        if ((os.path.isfile((os.path.dirname(os.path.realpath(__file__))) + "\\.env")) == False) or (os.path.getsize(((os.path.dirname(os.path.realpath(__file__))) + "\\.env")) == 0):
            print("Login started")
            sourceFile = open((os.path.dirname(os.path.realpath(__file__))) + "\\.env", 'w', encoding="utf-8")
            print("user_name=" + self.username.get(), file = sourceFile)
            print("pass_word=" + self.password.get(), file = sourceFile)
            sourceFile.close()


    def URL_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()

