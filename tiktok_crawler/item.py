import datetime
from selenium.webdriver.remote.webelement import WebElement

from dataclasses import dataclass

@dataclass
class Author:
    uniqueid: str
    avatar: str
    link: str
    nickname: str
    element: WebElement
    
    def __eq__(self, obj) -> bool:
        return (self.uniqueid == obj.uniqueid) \
            and (self.link == obj.link)
            
    def __repr__(self):
        return f"Author(uniqueid={self.uniqueid}, nickname={self.nickname})"
    
@dataclass
class Tag:
    link: str
    text: str
    element: WebElement
    
    def __eq__(self, obj) -> bool:
        return (self.text == obj.text) \
            and (self.link == obj.link)
            
    def __repr__(self):
        return f"Tag(link={self.link}, text={self.text})"
    
@dataclass
class Caption:
    text: str
    tags: list[Tag]
    element: WebElement
    
    def __repr__(self):
        return f"Caption(text={self.text}, tags={self.tags})"

@dataclass
class Music:
    text: str
    link: str
    element: WebElement
    def __eq__(self, obj) -> bool:
        return (self.text == obj.text) \
            and (self.link == obj.link)
    
    def __repr__(self):
        return f"Music(text={self.text}, link={self.link})"

@dataclass
class Media:
    link: str
    element: WebElement
    
    def __repr__(self):
        return f"Media(link={self.link})"
    
@dataclass
class Metrics:
    likes: str
    comments: str
    shares: str
    element: WebElement
    as_of: datetime = datetime.datetime.now()
    
    def __repr__(self):
        return f"Metrics(likes={self.likes},\
                    comments={self.comments},\
                    shares={self.shares},\
                    as_of={self.as_of}\
                )"

@dataclass
class Tiktok:
    
    id: str
    author: Author
    caption: Caption
    music: Music
    media: Media
    metrics: Metrics
    element: WebElement   

    def __eq__(self, obj) -> bool:
        return self.id == obj.id
