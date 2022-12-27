from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from tiktok_crawler.config import Config

class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Driver(metaclass=_Singleton):
    def __init__(self) -> None:
        options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_driver(self):
        return self.driver
        

