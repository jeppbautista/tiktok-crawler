from tiktok_crawler.crawler import Crawler

crawl = Crawler(limit=5)
tiktoks = crawl.get_foryou_tiktok_videos()
for tiktok in tiktoks:
    tiktok.save(path="../output")
