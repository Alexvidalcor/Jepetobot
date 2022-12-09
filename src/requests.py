# Import libraries
import os

from selenium import webdriver  # Webscrapping bot

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from webdriver_manager.firefox import GeckoDriverManager

# Main vars
logPath = os.getcwd()
channelYT = ""
video_url = f'https://www.youtube.com/c/{channelYT}/about'

# Selenium config
ser = Service(executable_path=GeckoDriverManager().install(), log_path=f"{logPath}/geckodriver.log")
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")


# Requests
def GetSubs():
    driver = webdriver.Firefox(service=ser, options=options)
    driver.get(video_url)
    subCounter = driver.find_element_by_id("subscriber-count").text
    driver.close()
    return subCounter