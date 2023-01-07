class Root:
    ROOT = """//*[@id="app"]"""
    SEARCH_BAR = f"""{ROOT}/div[2]/div/div[1]/div/form/input""" 

class ContainerItem(Root):
    TIKTOK_VIDEOS = f"""{Root.ROOT}/div[3]/div[2]/div[2]/div[1]/div/div/div[1]/div/div/a"""
    LOAD_MORE_BUTTON = f"""{Root.ROOT}/div[3]/div[2]/div[2]/div[2]/button"""
    
class TiktokVideo(Root):
    CONTAINER = f"""{Root.ROOT}/div[3]/div[2]/div[1]/div[2]/div[1]"""
    
class Author(TiktokVideo):
    UNIQUEID = ".//div[2]/div/a[2]/span[1]"
    AVATAR = ".//div[2]/div/a[1]/div/span/img"
    LINK = ".//div[2]/div/a[1]"
    NICKNAME = ".//div[2]/div/a[2]/span[2]/span[1]"

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