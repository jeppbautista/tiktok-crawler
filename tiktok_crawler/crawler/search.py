from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tiktok_crawler.crawler import Crawler
from tiktok_crawler import exception
from tiktok_crawler.config import Config
from tiktok_crawler.driver import Driver
from tiktok_crawler.entities import Author, Caption, Media, Metrics, Music, Tag, Tiktok
from tiktok_crawler.xpath import search

import logging
import random
import time
from urllib.parse import quote_plus

class SearchCrawler(Crawler):
    """Handles the web crawling of videos from the **Search results** page.
    
    Args:
        search (str): The raw search term.
        limit (int): Defines how many videos to download.
        driver_options (list): Implements the chromium command line switches. See here: https://peter.sh/experiments/chromium-command-line-switches/
    """
    
    def __init__(
        self, 
        search,
        limit:int = 15,
        driver_options:list = None
    ) -> None:
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.limit = limit
        self.search = search
        self.root = self._get_root(Config.CRAWL_ROOT_URL)
        
        self._search()
        
        
    def _search(self):
        search_bar = self.driver.find_element(By.XPATH, search.Root.SEARCH_BAR)
        search_bar.send_keys(self.search)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(10)
        
    def get_tiktok_videos(self) -> list[Tiktok]:
        """Downloads videos and metadata from the **search results** page of Tiktok.

        Returns:
            list[Tiktok]: list of `tiktok_crawler.entities.Tiktok`
        """
        
        self._load_tiktok_videos()
        
    def _get_root(self, url: str) -> WebElement:
        logging.info(f"Loading: {url}")
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, search.Root.ROOT)
        
        return root
    
    def _load_tiktok_videos(self) -> None:
        def _is_limit_reached() -> bool:
            element_count = len([element for element in self.root.find_elements(By.XPATH, search.ContainerItem.TIKTOK_VIDEOS)])
            logging.info(f"Element count: {element_count}")
            if element_count == 0:
                time.sleep(20)
            return self.limit <= element_count
        
        while not _is_limit_reached():
            logging.info("Scrolling...")
            
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
    
    def _get_tiktok(self, element: WebElement) -> Tiktok:
        return super()._get_tiktok(element)
    