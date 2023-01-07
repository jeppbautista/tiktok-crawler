from tiktok_crawler.crawler.search import SearchCrawler

driver_options = ["start-maximized"]

crawl = SearchCrawler(limit=5, search="test", driver_options=driver_options)
tiktoks = crawl.get_tiktok_videos()
# # # for tiktok in tiktoks:
# # #     tiktok.save(path="./output")
