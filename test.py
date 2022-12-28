from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from tiktok_crawler.config import Config
from tiktok_crawler.crawler import Crawler
from tiktok_crawler.driver import Driver

driver = Driver().get_driver()
driver.get(Config.CRAWL_ROOT_URL)
driver.implicitly_wait(20)
root = driver.find_element(By.XPATH, """//*[@id="app"]""")

crawl = Crawler()
item_containers = crawl.get_tiktok_videos(root)
keyword = input("enter a character or press enter to continue")

# ff = root.find_element(By.XPATH, Config.CRAWL_XPATH_CONTENTDIV)
# print(ff.find_elements(By.XPATH, "//div[1]//div"))

# content_div = driver.get_content_div(By.XPATH, Config.CRAWL_XPATH_CONTENTDIV)
# item_containers = content_div.get_item_containers_div(By.XPATH, "//div[1]//div")

# for item_container in item_containers:
#     print(item_container.id)

# height = element.size.get("height")
# print(height)
# driver.execute_script(f"window.scrollTo(0, {height})")
# time.sleep(10)

# counter = 5

# while counter > 0:
#     driver.execute_script("window.scrollTo(0, .);")
#     time.sleep(conf.CRAWL_SCROLL_PAUSE_TIME)
    
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == height:
#         break
    
#     height = new_height
#     counter = counter - 1
    

