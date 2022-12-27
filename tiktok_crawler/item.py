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
    
@dataclass
class Tags:
    link: str
    text: str
    element: WebElement
    
    def __eq__(self, obj) -> bool:
        return (self.text == obj.text) \
            and (self.link == obj.link)
    
@dataclass
class Caption:
    text: str
    tags: list[Tags]
    element: WebElement

@dataclass
class Music:
    text: str
    link: str
    element: WebElement
    def __eq__(self, obj) -> bool:
        return (self.text == obj.text) \
            and (self.link == obj.link)

@dataclass
class ItemContainer:
    
    id: str
    author: Author
    caption: Caption
    music: Music
    element: WebElement   

    def __eq__(self, obj) -> bool:
        return self.id == obj.id
