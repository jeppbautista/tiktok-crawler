from selenium.webdriver.remote.webelement import WebElement

from tiktok_crawler.entities import Author, Caption, Media, Metrics, Music, Tag, Tiktok

from abc import ABC, abstractmethod

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
        
    @abstractmethod
    def _get_tiktok(self, element : WebElement) -> Tiktok:
        ...
    
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
    