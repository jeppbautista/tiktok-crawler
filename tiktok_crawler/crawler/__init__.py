from selenium.webdriver.common.by import By
from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.item import Author, Caption, Tag
from tiktok_crawler import xpath

class Crawler:
    def get_item_containers(self, root):
        for element in root.find_elements(By.XPATH, xpath.ContainerItem.CONTAINERS):
            # author = self._get_author(element)
            caption = self._get_caption(element)
            print(caption)
            print("="*25)
        
    def _get_author(self, item_container):
        uniqueid = item_container.find_element(By.XPATH, xpath.Author.UNIQUEID).text
        avatar = item_container.find_element(By.XPATH, xpath.Author.AVATAR).get_attribute("src")
        link = item_container.find_element(By.XPATH, xpath.Author.LINK).get_attribute("href")
        nickname = item_container.find_element(By.XPATH, xpath.Author.NICKNAME).text
        
        author = Author(
            uniqueid=uniqueid,
            avatar=avatar,
            link=link,
            nickname=nickname,
            element=item_container
        )
        
        return author
    
    def _get_caption(self, item_container):
        tags = []
        video_description = item_container.find_element(By.XPATH, xpath.Caption.CONTAINER)
        video_text = video_description.find_element(By.XPATH, xpath.Caption.TEXT).text
        
        for tag in video_description.find_elements(By.XPATH, xpath.Caption.TAGS):
            link = tag.get_attribute("href")
            text = tag.find_element(By.XPATH, xpath.Tag.TEXT).text
            
            tags.append(
                Tag(
                    link=link,
                    text=text,
                    element=tag
                )
            )
            
        caption = Caption(
            text=video_text,
            tags=tags,
            element=video_description
        )
            
        return caption
    