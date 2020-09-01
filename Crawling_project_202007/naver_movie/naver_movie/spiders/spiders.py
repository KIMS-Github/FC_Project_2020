
import scrapy
import requests

from naver_movie.items import NaverMovieItem
from scrapy.http import TextResponse

class MovieSpider(scrapy.Spider):
    name = "NaverMovie"
    allow_domain = ["https://movie.naver.com"]
    start_urls = ["https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?genre=1"]
    
    # 페이지별 링크 만들기
    def parse(self, response):
        last_page = 2 #inpout last page
        for page in range(last_page + 1):
            page += 1
            link = response.url + "&page={}".format(page)
            yield scrapy.Request(link, callback=self.parse_page)
    
    # 각 영화별 상세페이지
    def parse_page(self, response):
        links = response.xpath('//*[@id="old_content"]/ul/li/a/@href').extract()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_page_contents)
    
    # 상세페이지에서 컨텐츠 가져오기 
    def parse_page_contents(self, response):
        item = NaverMovieItem()
        item["title"] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a[1]/text()').extract()[0]
        try:
            story = response.xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div/div/p/text()').extract()
            story = " ".join(story).replace("\r \xa0", "")
            item["story"] = story
        except:
            item["story"] = None
            
        yield item
