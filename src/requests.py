from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

def GetSubs():
    channelYT = ""
    video_url = f'https://www.youtube.com/c/{channelYT}/about'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(video_url)
    subCounter = driver.find_element_by_id("subscriber-count").text
    driver.close()
    return subCounter

