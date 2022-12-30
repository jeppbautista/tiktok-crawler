from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tiktok_crawler import exception
from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.entities import Author, Caption, Media, Metrics, Music, Tag, Tiktok
from tiktok_crawler import xpath

import logging
import time

class Crawler:
    """Handles all the web crawling in Selenium. Acts as the controller of the whole project.
    
    Args:
        limit (int): Defines how many videos to download.
        driver_options (list): Implements the chromium command line switches. See here: https://peter.sh/experiments/chromium-command-line-switches/
    """
    def __init__(
        self, 
        limit:int = 15,
        driver_options:list = None
    ) -> None:
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.limit = limit
        self.root = self.__get_root(Config.CRAWL_ROOT_URL)
    
    def get_foryou_tiktok_videos(self) -> list[Tiktok]:
        """Downloads videos and metadata from the **for you** page of Tiktok.

        Returns:
            list[Tiktok]: list of `tiktok_crawler.entities.Tiktok`
        """
        self.__load_tiktok_videos()
        tiktoks = []
                
        for element in self.root.find_elements(By.XPATH, xpath.ContainerItem.CONTAINERS)[:self.limit]:
            logging.info("Scrolling to Element...")
            self.driver.execute_script("arguments[0].scrollIntoView()", element)
            time.sleep(Config.CRAWL_SCROLL_PAUSE_TIME)
            tiktok = self.__get_tiktok(element)
            tiktoks.append(tiktok)
            
        return tiktoks
        
        
    def __get_tiktok(self, element : WebElement) -> Tiktok:
        """Extracts metadata from the tiktok videos and creates `tiktok_crawler.entities` instance for all of them.

        Args:
            element (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video.

        Returns:
            Tiktok: Returns a `tiktok_crawler.entities.Tiktok` instance.
            
        Raises:
            MediaNotFoundException: if the crawler was unable to download the Tiktok video.
        """
        try:
            logging.info("Extracting")
            author = self.__get_author(element)
            caption = self.__get_caption(element)
            media = self.__get_media(element)
            metrics = self.__get_metrics(element)
            music = self.__get_music(element)
                
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
    
    def __get_root(self, url:str) -> WebElement:
        """Extracts the root element of the page. This is done to remove unecessary HTML elements such as the *head*, *script* and *style*.

        Args:
            url (str): _description_

        Returns:
            WebElement: _description_
        """
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, xpath.Root.ROOT)
        
        return root
    
    def __load_tiktok_videos(self):
        def _is_limit_reached() -> bool:
            element_count = len([element for element in self.root.find_elements(By.XPATH, xpath.ContainerItem.CONTAINERS)])
            logging.info(f"Element count: {element_count}")
            return self.limit <= element_count
        
        while not _is_limit_reached():
            logging.info("Scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(Config.CRAWL_SCROLL_PAUSE_TIME)
        
    def __get_author(self, item_container):
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
    
    def __get_caption(self, item_container):
        video_description = item_container.find_element(By.XPATH, xpath.Caption.CONTAINER)
        video_text = video_description.find_element(By.XPATH, xpath.Caption.TEXT).text
        
        tags = self.__get_tags(video_description)
            
        caption = Caption(
            text=video_text,
            tags=tags,
            element=video_description
        )
            
        return caption
    
    def __get_media(self, item_container):
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
    
    def __get_metrics(self, item_container):
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
    
    def __get_music(self, item_container):
        music_container = item_container.find_element(By.XPATH, xpath.Music.CONTAINER)
        
        title = music_container.find_element(By.XPATH, xpath.Music.TITLE).text
        link = music_container.find_element(By.XPATH, xpath.Music.LINK).get_attribute("href")
        
        music = Music(
            title=title,
            link=link,
            element=music_container
        )
        
        return music

    def __get_tags(self, video_description):
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
    