from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--headless')

def GetSubs():
    channelYT = ""
    video_url = f'https://www.youtube.com/c/{channelYT}/about'
    driver = webdriver.Firefox(options = options)
    driver.get(video_url)
    subCounter = driver.find_element_by_id("subscriber-count").text
    driver.close()
    return subCounter
