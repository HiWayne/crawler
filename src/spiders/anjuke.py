import scrapy

from src.items import HousePriceCrawlerItem

# json 121 lines
class AnjukeSpider(scrapy.Spider):
    page = 3
    name = "anjuke"
    allowed_domains = ["shanghai.anjuke.com"]
    start_urls = [f"https://shanghai.anjuke.com/sale/p{page}/"]

    def parse(self, response):
        sel = scrapy.Selector(response)
        houseLi = sel.css("section.list > div.property")
        for house in houseLi:
            item = HousePriceCrawlerItem()
            item["name"] = house.css(
                "p.property-content-info-comm-name::text").get()
            item["price"] = house.css(
                "p.property-price-average::text").extract()[0]
            item["address"] = "上海市{}{}{}".format(house.css(
                'p.property-content-info-comm-address > span:nth-child(1)::text').get(), house.css('p.property-content-info-comm-address > span:nth-child(2)::text').get(), house.css('p.property-content-info-comm-address > span:nth-child(3)::text').get())
            item["construction_time"] = house.css(
                "div.property-content-detail section > div.property-content-info > p.property-content-info-text:nth-child(5)::text").extract()[0]
            yield item
        self.page += 1
        yield response.follow(f"https://shanghai.anjuke.com/sale/p{self.page}/", self.parse)
