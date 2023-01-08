from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tiktok_crawler.crawler import Crawler
from tiktok_crawler import exception
from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.entities import Author, Caption, Media, Metrics, Music, Tag, Tiktok
from tiktok_crawler.xpath import foryoupage

import logging
import time
from urllib.parse import quote_plus

class CrawlerForYouPage(Crawler):
    """Handles the web crawling of videos from the **For You** page.
    
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
        self.root = self._get_root(Config.CRAWL_ROOT_URL)
    
    def get_tiktok_videos(self) -> list[Tiktok]:
        """Downloads videos and metadata from the **for you** page of Tiktok.

        Returns:
            list[Tiktok]: list of `tiktok_crawler.entities.Tiktok`
        """
        self._load_tiktok_videos()
        tiktoks = []
                
        for element in self.root.find_elements(By.XPATH, foryoupage.ContainerItem.CONTAINERS)[:self.limit]:
            logging.info("Scrolling to Element...")
            self.driver.execute_script("arguments[0].scrollIntoView()", element)
            time.sleep(Config.CRAWL_SCROLL_PAUSE_TIME)
            tiktok = self._get_tiktok(element)
            tiktoks.append(tiktok)
            
        return tiktoks
    
    def _get_root(self, url:str) -> WebElement:
        """Extracts the root element of the page. This is done to remove unnecessary HTML elements such as the *head*, *script* and *style*.

        Args:
            url (str): The url of the page to be extracted.

        Returns:
            WebElement:  Returns a Selenium web element which is the extracted root element of the page.
        """
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, foryoupage.Root.ROOT)
        
        return root
    
    def _load_tiktok_videos(self) -> None:
        """Pre-loads tiktok videos by scrolling down until `self.limit` is exceeded or reached.
        """
        def _is_limit_reached() -> bool:
            """Checks if the number of elements in `xpath.ContainerItem.CONTAINERS` has reached or exceeded `self.limit`

            Returns:
                bool: `self.limit` <= the number of elements in `xpath.ContainerItem.CONTAINERS`
            """
            element_count = len([element for element in self.root.find_elements(By.XPATH, foryoupage.ContainerItem.CONTAINERS)])
            logging.info(f"Element count: {element_count}")
            return self.limit <= element_count
        
        while not _is_limit_reached():
            logging.info("Scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(Config.CRAWL_SCROLL_PAUSE_TIME)

    ### Get entities
      
    def _get_author(self, item_container: WebElement) -> Author:
        """Extracts the information about the account who posted the Tiktok video.

        Args:
            item_container (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video.

        Returns:
            Author: Returns a `tiktok_crawler.entities.Author` instance.
        """
        uniqueid = item_container.find_element(By.XPATH, foryoupage.Author.UNIQUEID).text
        avatar = item_container.find_element(By.XPATH, foryoupage.Author.AVATAR).get_attribute("src")
        link = item_container.find_element(By.XPATH, foryoupage.Author.LINK).get_attribute("href")
        nickname = item_container.find_element(By.XPATH, foryoupage.Author.NICKNAME).text
        
        author = Author(
            uniqueid=uniqueid,
            avatar=avatar,
            link=link,
            nickname=nickname,
            element=item_container
        )
        
        return author
    
    def _get_caption(self, item_container: WebElement) -> Caption:
        """Extracts the caption attached with the Tiktok video.

        Args:
            item_container (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video. 

        Returns:
            Caption: Returns a `tiktok_crawler.entities.Caption` instance.
        """
        video_description = item_container.find_element(By.XPATH, foryoupage.Caption.CONTAINER)
        video_text = video_description.find_element(By.XPATH, foryoupage.Caption.TEXT).text
        
        tags = self._get_tags(video_description)
            
        caption = Caption(
            text=video_text,
            tags=tags,
            element=video_description
        )
            
        return caption
    
    def _get_media(self, item_container: WebElement) -> Media:
        """Extracts the Tiktok video.

        Args:
            item_container (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video. 

        Returns:
            Media: Returns a `tiktok_crawler.entities.Media` instance.
            
        Raises:
            MediaNotFoundException: if the crawler was unable to download the Tiktok video.
        """
        media_container = item_container.find_element(By.XPATH, foryoupage.Media.CONTAINER)
        try:
            link = WebDriverWait(media_container, 10).until(
                EC.presence_of_element_located((By.XPATH, f"{foryoupage.Media.LINK}|{foryoupage.Media.LINK_ALT}"))
            ).get_attribute("src")
        except TimeoutException:
            try:
                link = WebDriverWait(media_container, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"{foryoupage.Media.LINK}|{foryoupage.Media.LINK_ALT}"))
                ).get_attribute("src")
            except TimeoutException:  
                raise exception.MediaNotFoundException("Unable to find Media")
        
        media = Media(
            link=link,
            element=media_container
        )
        
        return media
    
    def _get_metrics(self, item_container: WebElement) -> Metrics:
        """Extracts the metrics of the Tiktok video.

        Args:
            item_container (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video. 

        Returns:
            Metrics: Returns a `tiktok_crawler.entities.Metrics` instance.
        """
        metrics_container = item_container.find_element(By.XPATH, foryoupage.Metrics.CONTAINER)
        
        likes = metrics_container.find_element(By.XPATH, foryoupage.Metrics.LIKES).text
        comments = metrics_container.find_element(By.XPATH, foryoupage.Metrics.COMMENTS).text
        shares = metrics_container.find_element(By.XPATH, foryoupage.Metrics.SHARES).text
        
        metrics = Metrics(
            likes=likes,
            comments=comments,
            shares=shares,
            element=metrics_container
        )
        
        return metrics
    
    def _get_music(self, item_container: WebElement) -> Music:
        """Extracts the music of the Tiktok video.

        Args:
            item_container (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video. 

        Returns:
            Music: Returns a `tiktok_crawler.entities.Music` instance.
        """
        music_container = item_container.find_element(By.XPATH, foryoupage.Music.CONTAINER)
        
        title = music_container.find_element(By.XPATH, foryoupage.Music.TITLE).text
        link = music_container.find_element(By.XPATH, foryoupage.Music.LINK).get_attribute("href")
        
        music = Music(
            title=title,
            link=link,
            element=music_container
        )
        
        return music

    def _get_tags(self, video_description: WebElement) -> list[Tag]:
        """Extracts the tags in the caption of the Tiktok video.

        Args:
            video_description (WebElement): Accepts a Selenium web element which is the extracted video container (see `_get_caption()`) of a Tiktok video. 

        Returns:
            list[Tag]: List of `tiktok_crawler.entities.Tag`
        """
    
        _tags = []
        for tag in video_description.find_elements(By.XPATH, foryoupage.Caption.TAGS):
            link = tag.get_attribute("href")
            text = tag.find_element(By.XPATH, foryoupage.Tag.TEXT).text
            
            _tags.append(
                Tag(
                    link=link,
                    text=text,
                    element=tag
                )
            )
            
        return _tags
