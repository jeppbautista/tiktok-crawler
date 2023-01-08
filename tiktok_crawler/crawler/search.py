from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tiktok_crawler.crawler import Crawler
from tiktok_crawler.exception import CaptchaTimeoutException, MediaNotFoundException, NoElementsFound
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
        self.search = quote_plus(search)
        search_url = f"{Config.CRAWL_SEARCH_URL}q={self.search}"
        self.root = self._get_root(search_url)     
        
    def get_tiktok_videos(self) -> list[Tiktok]:
        """Downloads videos and metadata from the **search results** page of Tiktok.

        Returns:
            list[Tiktok]: list of `tiktok_crawler.entities.Tiktok`
        """
        self._wait_for_captcha()
        self._load_tiktok_videos()
        tiktok_links = self._get_tiktok_links()
        tiktoks = []
        for tiktok_link in tiktok_links:
            try:
                self.driver.get(tiktok_link)
                tiktok_container = self.driver.find_element(By.XPATH, search.TiktokVideo.CONTAINER)
                tiktoks.append(self._get_tiktok(tiktok_container))
            except StaleElementReferenceException:
                logging.error("Stale Element")
        
        return tiktoks
    
    def _get_tiktok_links(self) -> list[WebElement]:
        return [element.get_attribute("href") for element in self.root.find_elements(By.XPATH, search.ContainerItem.TIKTOK_VIDEOS)][:self.limit]
    
    def _get_root(self, url: str) -> WebElement:
        logging.info(f"Loading: {url}")
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, search.Root.ROOT)
        
        return root
    
    def _load_tiktok_videos(self) -> None:   
        """Loads TikTok videos by scrolling and clicking the 'Load More' button.
    
        The function will keep scrolling and loading more TikTok videos until it has reached the limit specified in the `self.limit` attribute. 
        If no elements are found using the XPATH specified in `search.ContainerItem.TIKTOK_VIDEOS`, a `NoElementsFound` exception is raised.
        """
        tiktok_links = []
        while len(tiktok_links) < self.limit:
            logging.info("Scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            tiktok_links = tiktok_links + self.root.find_elements(By.XPATH, search.ContainerItem.TIKTOK_VIDEOS)
            if len(tiktok_links) == 0:
                raise NoElementsFound(f"No elements found from given XPATH: {search.ContainerItem.TIKTOK_VIDEOS}")
            
            logging.info(f"Element count: {len(tiktok_links)}")
            load_more_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, search.ContainerItem.LOAD_MORE_BUTTON))
            )
            load_more_button.click()
            time.sleep(Config.CRAWL_SCROLL_PAUSE_TIME)
            
    def _wait_for_captcha(self):
        """Waits for the user to solve a captcha, if present.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, search.ContainerItem.CAPTCHA))
            )
            
            logging.warning("Process will timeout in 60 seconds if captcha is not solved.")
            logging.warning("Waiting for user to solve captcha...")
            
            WebDriverWait(self.driver, 60).until_not(
                EC.presence_of_element_located((By.XPATH, search.ContainerItem.CAPTCHA))
            )
            
            logging.info("Captcha Solved. Proceeding to crawl...")
            time.sleep(5)
        except TimeoutException:
            raise CaptchaTimeoutException("Captcha needs to be solved within 60 seconds")

    ### Get entities
            
    def _get_author(self, item_container: WebElement) -> Author:
        """Extracts the information about the account who posted the Tiktok video.

        Args:
            item_container (WebElement): Accepts a Selenium web element which is the extracted container of a Tiktok video.

        Returns:
            Author: Returns a `tiktok_crawler.entities.Author` instance.
        """
        uniqueid = item_container.find_element(By.XPATH, search.Author.UNIQUEID).text
        avatar = ""
        link = item_container.find_element(By.XPATH, search.Author.LINK).get_attribute("href")
        nickname = item_container.find_element(By.XPATH, search.Author.NICKNAME).text
        
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
        video_description = item_container.find_element(By.XPATH, search.Caption.CONTAINER)
        video_text = video_description.find_element(By.XPATH, search.Caption.TEXT).text
        
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
        media_container = item_container.find_element(By.XPATH, search.Media.CONTAINER)
        try:
            link = WebDriverWait(media_container, 10).until(
                EC.presence_of_element_located((By.XPATH, f"{search.Media.LINK}|{search.Media.LINK_ALT}"))
            ).get_attribute("src")
        except TimeoutException:
            try:
                link = WebDriverWait(media_container, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"{search.Media.LINK}|{search.Media.LINK_ALT}"))
                ).get_attribute("src")
            except TimeoutException:  
                raise MediaNotFoundException("Unable to find Media")
        
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
        metrics_container = item_container.find_element(By.XPATH, search.Metrics.CONTAINER)
        
        likes = metrics_container.find_element(By.XPATH, search.Metrics.LIKES).text
        comments = metrics_container.find_element(By.XPATH, search.Metrics.COMMENTS).text
        shares = metrics_container.find_element(By.XPATH, search.Metrics.SHARES).text
        
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
        music_container = item_container.find_element(By.XPATH, search.Music.CONTAINER)
        
        title = music_container.find_element(By.XPATH, search.Music.TITLE).text
        link = music_container.find_element(By.XPATH, search.Music.LINK).get_attribute("href")
        
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
        for tag in video_description.find_elements(By.XPATH, search.Caption.TAGS):
            link = tag.get_attribute("href")
            text = tag.find_element(By.XPATH, search.Tag.TEXT).text
            
            _tags.append(
                Tag(
                    link=link,
                    text=text,
                    element=tag
                )
            )
            
        return _tags
    