from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pathlib
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.simplefilter('ignore')


def speak(text):
    engine = pyttsx3.init()
    Id = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    engine.setProperty('voice', Id)
    print("")
    print(f"==> Jarvis AI : {text}")
    print("")
    engine.say(text=text)
    engine.runAndWait()


def open_website_and_login(vtop_driver):
    # Your VTOP credentials
    username = "SHREYAS0650"
    password = "11November@2003"

    Xpath1 = '/html/body/div[1]/div/div/div/div[2]/div[1]/div/form/a/div/div[2]/button'
    vtop_driver.find_element(by=By.XPATH, value=Xpath1).click()

    Xpath2 = '/html/body/div[1]/div/div/div/div[2]/form/div[1]/input'
    vtop_driver.find_element(by=By.XPATH, value=Xpath2).send_keys(username)

    Xpath3 = '/html/body/div[1]/div/div/div/div[2]/form/div[2]/input'
    vtop_driver.find_element(by=By.XPATH, value=Xpath3).send_keys(password)

    speak("Please enter the captcha")

    while True:
        try:
            Xpath4 = '/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[1]/strong'
            vtop_driver.find_element(by=By.XPATH, value=Xpath4)
            break

        except:
            pass

    return vtop_driver


def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en")
        print(f"==> Shresth : {query}")
        return query.lower()

    except Exception as e:
        print(f"Error recognizing speech: {e}")
        return ""


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


ScriptDir = pathlib.Path().absolute()

# URLs for the websites
flowgpt_url = "https://flowgpt.com/chat"
vtop_url = "https://vtop.vit.ac.in/vtop/login"

# Chrome options for FlowGPT (headless)
user_agent_flowgpt = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"
flowgpt_chrome_option = Options()
flowgpt_chrome_option.add_argument(f"user-agent={user_agent_flowgpt}")
flowgpt_chrome_option.add_argument('--profile-directory=Default')
flowgpt_chrome_option.add_argument(f'user-data-dir={ScriptDir}\\chromedata')
flowgpt_chrome_option.add_argument("--headless")  # Enable headless mode for FlowGPT

flowgpt_service = Service(ChromeDriverManager().install())

# Chrome options for VTOP (non-headless)
user_agent_vtop = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"
vtop_chrome_option = Options()
vtop_chrome_option.add_argument(f"user-agent={user_agent_vtop}")
vtop_chrome_option.add_argument('--profile-directory=Default')
vtop_chrome_option.add_argument(f'user-data-dir={ScriptDir}\\chromedata')

vtop_service = Service(ChromeDriverManager().install())

# Initialize FlowGPT driver
flowgpt_driver = webdriver.Chrome(service=flowgpt_service, options=flowgpt_chrome_option)
flowgpt_driver.maximize_window()

# # Initialize VTOP driver
# vtop_driver = webdriver.Chrome(service=vtop_service, options=vtop_chrome_option)
# vtop_driver.maximize_window()

# Open FlowGPT in the first tab
flowgpt_driver.get(flowgpt_url)

ChatNumber = 3


def Checker():
    global ChatNumber
    for i in range(1, 1000):
        if i % 2 != 0:
            try:
                ChatNumber = str(i)
                Xpath = f"/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div[{ChatNumber}]/div/div/div/div[1]/p[1]"
                flowgpt_driver.find_element(by=By.XPATH, value=Xpath)
            except:
                print(f"The next chatnumber is : {i}")
                ChatNumber = str(i)
                break


def Websiteopener(driver):
    while True:
        try:
            xPATH = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div/div/div/p'
            driver.find_element(by=By.XPATH, value=xPATH)
            break

        except:
            pass


def SendMessage(Query):
    xPATH = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div[3]/textarea'

    # Wait for the element to be clickable
    element = WebDriverWait(flowgpt_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xPATH))
    )

    # Send keys to the element
    element.send_keys(Query)

    sleep(0.5)

    Xpath2 = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div[3]/button'
    flowgpt_driver.find_element(by=By.XPATH, value=Xpath2).click()


def Resultscrapper():
    global ChatNumber
    ChatNumber = str(ChatNumber)
    Xpath = f"/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div[{ChatNumber}]/div/div/div/div[1]/p[1]"

    Text = flowgpt_driver.find_element(by=By.XPATH, value=Xpath).text
    ChatNumberNew = int(ChatNumber) + 2
    ChatNumber = ChatNumberNew
    return Text


def waitfortheanswer():
    sleep(4)
    Xpath = '/html/body/div[1]/main/div[3]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div/button'
    while True:
        try:
            flowgpt_driver.find_element(by=By.XPATH, value=Xpath)
        except:
            break


def open_vit_and_restart_flowgpt():
    global flowgpt_driver
    # Close VTOP driver
    vtop_driver.quit()

    # Initialize FlowGPT driver
    flowgpt_driver = webdriver.Chrome(service=flowgpt_service, options=flowgpt_chrome_option)
    flowgpt_driver.maximize_window()

    # Open FlowGPT in the first tab
    flowgpt_driver.get(flowgpt_url)
    Websiteopener(flowgpt_driver)

    speak("Switching back to FlowGPT. Please wait.")

def open_vit():
    global vtop_driver
    # Initialize VTOP driver
    vtop_driver = webdriver.Chrome(service=vtop_service, options=vtop_chrome_option)
    vtop_driver.maximize_window()

    # Open VTOP in a new tab
    vtop_driver.get(vtop_url)

    speak("Opening V TOP. Please wait.")
    open_website_and_login(vtop_driver)
    speak("Login successful.")

    # Close VTOP after successful login and restart FlowGPT
    open_vit_and_restart_flowgpt()

# Initialize FlowGPT driver
flowgpt_driver = webdriver.Chrome(service=flowgpt_service, options=flowgpt_chrome_option)
flowgpt_driver.maximize_window()

# Open FlowGPT in the first tab
flowgpt_driver.get(flowgpt_url)
Websiteopener(flowgpt_driver)




# popupremover()
Checker()

while True:
    Query = speechrecognition()
    if len(str(Query)) < 3:
        pass
    elif Query == None:
        pass
    elif "time" in Query:
        current_time = get_current_time()
        speak(f"The current time is {current_time}")
    elif "open vit" in Query:
        open_vit()
        # vtop_driver = webdriver.Chrome(service=vtop_service, options=vtop_chrome_option)
        # vtop_driver.maximize_window()
        # vtop_driver.quit()
        # # # Initialize FlowGPT driver
        # # flowgpt_driver = webdriver.Chrome(service=flowgpt_service, options=flowgpt_chrome_option)
        # # flowgpt_driver.maximize_window()
        # # Open FlowGPT in the first tab
        # flowgpt_driver.get(flowgpt_url)

    else:
        SendMessage(Query=Query)
        waitfortheanswer()
        Text = Resultscrapper()
        speak(Text)

flowgpt_driver.quit()
# vtop_driver.quit()  # Uncomment this line if you uncomment the VTOP-related code
