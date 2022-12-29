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
    LINK = ".//div/div[1]/div[1]/div[1]/video[1]/source[1]"
    LINK_ALT = ".//div/div[1]/div[1]/div[1]/video[1]"
    
    
class Metrics(ContainerItem):
    CONTAINER = ".//div[1]/div[2]/div[2]"
    LIKES = ".//button[1]/strong[1]"
    COMMENTS = ".//button[2]/strong[1]"
    SHARES = ".//button[3]/strong[1]"

class Tag(Caption):
    LINK = ".//"
    TEXT = ".//strong"

class Music(ContainerItem):
    CONTAINER = ".//div[1]/div[1]/h4[1]"
    LINK = ".//a[1]"
    TITLE = ".//a[1]"