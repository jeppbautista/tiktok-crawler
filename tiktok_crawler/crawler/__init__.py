import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tiktok_crawler import exception
from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.item import Author, Caption, Media, Metrics, Music, Tag, Tiktok
from tiktok_crawler import xpath

import time

class Crawler:
    def __init__(
        self, 
        limit:int = 15,
        driver_options:list = None
    ) -> None:
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.limit = limit
        self.root = self.get_root(Config.CRAWL_ROOT_URL)
        
    def get_root(self, url):
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, xpath.Root.ROOT)
        
        return root
    
    def load_tiktok_videos(self):
        def _is_limit_reached() -> bool:
            element_count = len([element for element in self.root.find_elements(By.XPATH, xpath.ContainerItem.CONTAINERS)])
            logging.info(f"Element count: {element_count}")
            return self.limit <= element_count
        
        while not _is_limit_reached():
            logging.info("Scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
    
    def get_foryou_tiktok_videos(self):
        self.load_tiktok_videos()
        tiktoks = []
                
        for element in self.root.find_elements(By.XPATH, xpath.ContainerItem.CONTAINERS)[:self.limit]:
            logging.info("Scrolling to Element...")
            self.driver.execute_script("arguments[0].scrollIntoView()", element)
            time.sleep(1)
            tiktok = self.get_tiktok(element)
            tiktoks.append(tiktok)
            
        print([f"{i}\n" for i in tiktoks])
        
    def get_tiktok(self, element : WebElement) -> Tiktok:
        try:
            logging.info("Extracting")
            author = self._get_author(element)
            caption = self._get_caption(element)
            media = self._get_media(element)
            metrics = self._get_metrics(element)
            music = self._get_music(element)
                
            tiktok = Tiktok(
                id = element.id,
                author=author,
                caption=caption,
                media=media,
                metrics=metrics,
                music=music,
                element=element
            )
                
        except exception.MediaNotFoundException as e:
            logging.warning(e)
            tiktok = Tiktok(
                id = element.id,
                author=author,
                caption=caption,
                media=media,
                metrics=None,
                music=None,
                element=element,
                status="MediaNotFoundException"
            )
                
        logging.info("DONE Extracting element")
        return tiktok
        
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
        def _is_playing():
            pass
        
        media_container = item_container.find_element(By.XPATH, xpath.Media.CONTAINER)
        try:
            link = WebDriverWait(media_container, 10).until(
                EC.presence_of_element_located((By.XPATH, f"{xpath.Media.LINK}|{xpath.Media.LINK_ALT}"))
            ).get_attribute("src")
        except TimeoutException:
            try:
                link = WebDriverWait(media_container, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"{xpath.Media.LINK}|{xpath.Media.LINK_ALT}"))
                ).get_attribute("src")
            except TimeoutException:  
                raise exception.MediaNotFoundException("Unable to find Media")
        
        media = Media(
            link=link,
            element=media_container
        )
        
        return media
    
    def _get_metrics(self, item_container):
        metrics_container = item_container.find_element(By.XPATH, xpath.Metrics.CONTAINER)
        
        likes = metrics_container.find_element(By.XPATH, xpath.Metrics.LIKES).text
        comments = metrics_container.find_element(By.XPATH, xpath.Metrics.COMMENTS).text
        shares = metrics_container.find_element(By.XPATH, xpath.Metrics.SHARES).text
        
        metrics = Metrics(
            likes=likes,
            comments=comments,
            shares=shares,
            element=metrics_container
        )
        
        return metrics
    
    def _get_music(self, item_container):
        music_container = item_container.find_element(By.XPATH, xpath.Music.CONTAINER)
        
        title = music_container.find_element(By.XPATH, xpath.Music.TITLE).text
        link = music_container.find_element(By.XPATH, xpath.Music.LINK).get_attribute("href")
        
        music = Music(
            title=title,
            link=link,
            element=music_container
        )
        
        return music

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
    