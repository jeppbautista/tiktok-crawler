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
from tiktok_crawler.xpath import hashtag

import logging
import time
from urllib.parse import quote_plus

class HashTagCrawler(Crawler):
    """Handles the web crawling of videos from hashtags.
    
    Args:
        hashtag (str): The hashtag to be searched.
        limit (int): Defines how many videos to download.
        driver_options (list): Implements the chromium command line switches. See here: https://peter.sh/experiments/chromium-command-line-switches/
    """
    
    def __init__(
        self, 
        tag:str,
        limit:int = 15,
        driver_options:list = None
    ) -> None:
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.limit = limit
        self.tag = tag
        
        search_url = Config.CRAWL_HASHTAG_URL + self.tag
        print(search_url)
        self.root = self._get_root(search_url)
        
        time.sleep(5)
        
    def get_tiktok_videos(self) -> list[Tiktok]:
        return super().get_tiktok_videos()
    
    def _get_root(self, url:str) -> WebElement:
        """Extracts the root element of the page. This is done to remove unnecessary HTML elements such as the *head*, *script* and *style*.

        Args:
            url (str): The url of the page to be extracted.

        Returns:
            WebElement:  Returns a Selenium web element which is the extracted root element of the page.
        """
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, hashtag.Root.ROOT)
        
        return root

    def _load_tiktok_videos(self) -> None:
        return super()._load_tiktok_videos()    
    
    def _get_author(self, item_container: WebElement) -> Author:
        return super()._get_author(item_container)
    
    def _get_caption(self, item_container: WebElement) -> Caption:
        return super()._get_caption(item_container)
    
    def _get_media(self, item_container: WebElement) -> Media:
        return super()._get_media(item_container)
    
    def _get_metrics(self, item_container: WebElement) -> Metrics:
        return super()._get_metrics(item_container)
    
    def _get_music(self, item_container: WebElement) -> Music:
        return super()._get_music(item_container)
    
    def _get_tags(self, video_description: WebElement) -> list[Tag]:
        return super()._get_tags(video_description)
    