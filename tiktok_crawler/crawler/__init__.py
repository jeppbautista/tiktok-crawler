from selenium.webdriver.remote.webelement import WebElement

from tiktok_crawler.entities import Author, Caption, Media, Metrics, Music, Tag, Tiktok

from abc import ABC, abstractmethod
import logging

from tiktok_crawler.exception import MediaNotFoundException

class Crawler(ABC):
    @abstractmethod
    def get_tiktok_videos(self) -> list[Tiktok]:
        ...
        
    @abstractmethod
    def _get_root(self, url:str) -> WebElement:
        ...
        
    @abstractmethod
    def _load_tiktok_videos(self) -> None:
        ...
        
    def _get_tiktok(self, element : WebElement) -> Tiktok:
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
                
        except MediaNotFoundException as e:
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
    
    @abstractmethod
    def _get_author(self, item_container: WebElement) -> Author:
        ...
        
    @abstractmethod
    def _get_caption(self, item_container: WebElement) -> Caption:
        ...
        
    @abstractmethod
    def _get_media(self, item_container: WebElement) -> Media:
        ...
        
    @abstractmethod
    def _get_metrics(self, item_container: WebElement) -> Metrics:
        ...
        
    @abstractmethod
    def _get_music(self, item_container: WebElement) -> Music:
        ...
        
    @abstractmethod    
    def _get_tags(self, video_description: WebElement) -> list[Tag]:
        ...
    