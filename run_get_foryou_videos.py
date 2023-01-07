from tiktok_crawler.crawler.foryoupage import CrawlerForYouPage

crawl = CrawlerForYouPage(limit=5)
tiktoks = crawl.get_tiktok_videos()
for tiktok in tiktoks:
    tiktok.save(path="./output")
