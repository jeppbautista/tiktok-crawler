class Root:
    ROOT = """//*[@id="app"]"""

class ContainerItem(Root):
    CONTAINERS = f"""{Root.ROOT}/div[2]/div[2]/div[1]/div"""
    
class Author(ContainerItem):
    UNIQUEID = ".//div[1]/div[1]/div[1]/a[2]/h3"
    AVATAR = ".//div[1]/div[1]/div[1]/a[1]/div[1]/span[1]/img"
    LINK = ".//a[1]"
    NICKNAME = ".//div[1]/div[1]/div[1]/a[2]/h4"

class Caption(ContainerItem):
    CONTAINER = ".//div[1]/div[1]/div[2]"
    TEXT = ".//span[1]"
    
    TAGS = ".//a"
    
class Media(ContainerItem):
    CONTAINER = ".//div[1]/div[2]/div[1]"
    LINK = ".//div[1]/div[1]/div[1]/div[1]/video[1]/source[1]"
    
    
class Metrics(ContainerItem):
    CONTAINER = ".//div[1]/div[2]/div[2]"

class Tag(Caption):
    LINK = ".//"
    TEXT = ".//strong"
    