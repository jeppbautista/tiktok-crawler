from selenium.webdriver.common.by import By
from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.item import Author
from tiktok_crawler.xpath import ContainerItem

class Crawler:
    def get_item_containers(self, root):
        for element in root.find_elements(By.XPATH, ContainerItem.CONTAINERS):
            self._get_author(element)
            print("="*25)
        
    def _get_author(self, item_container):
        uniqueid = item_container.find_element(By.XPATH, ContainerItem.UNIQUEID).text
        avatar = item_container.find_element(By.XPATH, ContainerItem.AVATAR).get_attribute("src")
        link = item_container.find_element(By.XPATH, ContainerItem.AVATAR).get_attribute("href")
        nickname = item_container.find_element(By.XPATH, ContainerItem.NICKNAME).text
        
        author = Author(
            uniqueid=uniqueid,
            avatar=avatar,
            link=link,
            nickname=nickname,
            element=item_container
        )
        
        return author
        
    def _get_avatar():
        pass