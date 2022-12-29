from selenium.webdriver.remote.webelement import WebElement

from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import json
import os
import requests

class TiktokEntity(ABC):
    @abstractmethod
    def __post_init__(self):
        ...
        
    @abstractmethod
    def __repr__(self):
        ...
        
    @abstractmethod
    def to_dict(self):
        ...

@dataclass
class Author(TiktokEntity):
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
    
    def to_dict(self):
        return dict(
            uniqueid=self.uniqueid,
            nickname=self.nickname,
            link=self.link,
            avatar=self.avatar,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Tag(TiktokEntity):
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
    
    def to_dict(self):
        return dict(
            link=self.link,
            text=self.text,
            element=self.element.get_attribute("innerHTML")
        )
    
@dataclass
class Caption(TiktokEntity):
    text: str
    tags: list[Tag]
    element: WebElement

    def __post_init__(self):
        self.text = self.text.strip()
    
    def __repr__(self):
        return f"Caption(text={self.text}, tags={self.tags})"
    
    def to_dict(self):
        return dict(
            tags=[tag.to_dict() for tag in self.tags],
            text=self.text,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Music(TiktokEntity):
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
    
    def to_dict(self):
        return dict(
            title=self.title,
            link=self.link,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Media(TiktokEntity):
    link: str
    element: WebElement
    
    def __post_init__(self):
        self.link = self.link.strip()
    
    def __repr__(self):
        return f"Media(link={self.link})"
    
    def to_dict(self):
        return dict(
            link=self.link,
            element=self.element.get_attribute("innerHTML")
        )
    
@dataclass
class Metrics(TiktokEntity):
    likes: str
    comments: str
    shares: str
    element: WebElement
    as_of: datetime = datetime.datetime.now().isoformat()
    
    def __post_init__(self):
        self.likes = self.likes.strip()
        self.comments = self.comments.strip()
        self.shares = self.shares.strip()
    
    def __repr__(self):
        return f"Metrics(likes={self.likes}, comments={self.comments},shares={self.shares}, as_of={self.as_of} )"
    
    def to_dict(self):
        return dict(
            likes=self.likes,
            comments=self.comments,
            shares=self.shares,
            as_of=self.as_of,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Tiktok:
    
    id: str
    author: Author
    caption: Caption
    music: Music
    media: Media
    metrics: Metrics
    element: WebElement
    status: str = None
    
    def save(self, path:str = "./"):
        def _save_metadata(path):
            file_path = os.path.join(path, f"{self.id}.json")
            with open(file_path, 'w+') as file:
                json.dump(self.to_dict(), file)
                
        def _save_video(path):
            file_path = os.path.join(path, f"{self.id}.mp4")
            response = requests.get(self.media.link)
            with open(file_path, "wb") as file:
                file.write(response.content)
        
        _save_metadata(path)
        _save_video(path)
    
    def to_dict(self):
        return dict(
            id=self.id,
            Author=self.author.to_dict(),
            Caption=self.caption.to_dict(),
            Music=self.music.to_dict(),
            Media=self.media.to_dict(),
            Metrics=self.metrics.to_dict(),
            Element=self.element.get_attribute("innerHTML"),
            Status=self.status
        )

    def __eq__(self, obj) -> bool:
        return self.id == obj.id
    
    def __repr__(self) -> str:
        return f"Tiktok(id={self.id}, {self.status}, {self.author}, {self.caption}, {self.music}, {self.media}, {self.metrics})"
