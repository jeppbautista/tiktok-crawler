import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.item import Author, Caption, Media, Tag
from tiktok_crawler import xpath

import time

class Crawler:
    def __init__(self) -> None:
        self.driver = Driver().get_driver()
    
    def get_item_containers(self, root):
        for element in root.find_elements(By.XPATH, xpath.ContainerItem.CONTAINERS):
            
            logging.info("Scrolling to Element")
            self.driver.execute_script("arguments[0].scrollIntoView()", element)
            time.sleep(5)
            
            try:
                logging.info("Extracting")
                # author = self._get_author(element)
                # caption = self._get_caption(element)
                media = self._get_media(element)
                print(media)
            except TimeoutException as e:
                logging.warning(e)
                
            logging.info("DONE Extracting element")
        
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
        video_description = item_container.find_element(By.XPATH, xpath.Caption.CONTAINER)
        video_text = video_description.find_element(By.XPATH, xpath.Caption.TEXT).text
        
        tags = self._get_tags(video_description)
            
        caption = Caption(
            text=video_text,
            tags=tags,
            element=video_description
        )
            
        return caption
    
    def _get_media(self, item_container):
        media_container = item_container.find_element(By.XPATH, xpath.Media.CONTAINER)
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            link = WebDriverWait(media_container, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath.Media.LINK))
            ).get_attribute("src")
        except TimeoutException:
            raise TimeoutError("Unable to find Media")
        
        media = Media(
            link=link,
            element=media_container
        )
        
        return media

    
    def _get_tags(self, video_description):
        _tags = []
        for tag in video_description.find_elements(By.XPATH, xpath.Caption.TAGS):
            link = tag.get_attribute("href")
            text = tag.find_element(By.XPATH, xpath.Tag.TEXT).text
            
            _tags.append(
                Tag(
                    link=link,
                    text=text,
                    element=tag
                )
            )
            
        return _tags
    