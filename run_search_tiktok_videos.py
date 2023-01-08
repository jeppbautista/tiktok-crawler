from tiktok_crawler.crawler.search import SearchCrawler

# driver_options = ["start-maximized"]

crawl = SearchCrawler(limit=100, search="test")
tiktoks = crawl.get_tiktok_videos()
for tiktok in tiktoks:
    tiktok.save(path="./output")

