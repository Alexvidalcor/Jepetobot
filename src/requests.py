from selenium import webdriver

def GetSubs():
    video_url = 'https://www.youtube.com/c/BorrueyZ/about'
    driver = webdriver.Firefox()
    driver.get(video_url)
    subCounter = driver.find_element_by_id("subscriber-count").text
    driver.close()
    return subCounter
