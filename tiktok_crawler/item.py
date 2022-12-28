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
    
    def __post_init__(self):
        self.uniqueid = self.uniqueid.strip()
        self.avatar = self.avatar.strip()
        self.link = self.link.strip()
        self.nickname = self.nickname.strip()
    
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
    
    def __post_init__(self):
        self.link = self.link.strip()
        self.text = self.text.strip()
    
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

    def __post_init__(self):
        self.text = self.text.strip()
    
    def __repr__(self):
        return f"Caption(text={self.text}, tags={self.tags})"

@dataclass
class Music:
    title: str
    link: str
    element: WebElement
    
    def __post_init__(self):
        self.title = self.title.strip()
        self.link = self.link.strip()
    
    def __eq__(self, obj) -> bool:
        return (self.title == obj.title) \
            and (self.link == obj.link)
    
    def __repr__(self):
        return f"Music(title={self.title}, link={self.link})"

@dataclass
class Media:
    link: str
    element: WebElement
    
    def __post_init__(self):
        self.link = self.link.strip()
    
    def __repr__(self):
        return f"Media(link={self.link})"
    
@dataclass
class Metrics:
    likes: str
    comments: str
    shares: str
    element: WebElement
    as_of: datetime = datetime.datetime.now()
    
    def __post_init__(self):
        self.likes = self.likes.strip()
        self.comments = self.comments.strip()
        self.shares = self.shares.strip()
    
    def __repr__(self):
        return f"Metrics(likes={self.likes}, comments={self.comments},shares={self.shares}, as_of={self.as_of} )"

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
    
    def __repr__(self) -> str:
        return f"Tiktok(id={self.id}, {self.author}, {self.caption}, {self.music}, {self.media}, {self.metrics})"
