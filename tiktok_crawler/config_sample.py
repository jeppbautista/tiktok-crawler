import os
    
class Dev:
    CRAWL_SCROLL_PAUSE_TIME = 0.5
    
class Prod:
    CRAWL_SCROLL_PAUSE_TIME = 2
    
class Config(Dev if 1==1 else Prod):
    CRAWL_ROOT_URL = "https://www.tiktok.com/foryou"
