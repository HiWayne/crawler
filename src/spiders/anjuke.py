import scrapy

from house_price_crawler.items import HousePriceCrawlerItem


class AnjukeSpider(scrapy.Spider):
    name = "anjuke"
    allowed_domains = ["shanghai.anjuke.com"]
    start_urls = ["https://shanghai.anjuke.com/sale"]

    def parse(self, response):
        sel = scrapy.Selector(response)
        houseLi = sel.css("section.list > div.property")
        for house in houseLi:
            item = HousePriceCrawlerItem()
            item["name"] = house.css(
                "p.property-content-info-comm-name::text").get()
            item["price"] = house.css(
                "p.property-price-average::text").extract_first()
            item["address"] = "上海市{}{}{}".format(house.css(
                'p.property-content-info-comm-address > span:nth-child(1)::text').get(), house.css('p.property-content-info-comm-address > span:nth-child(2)::text').get(), house.css('p.property-content-info-comm-address > span:nth-child(3)::text').get())
            item["construction_time"] = house.css(
                "div.property-content-detail section > div.property-content-info > p.property-content-info-text:nth-child(5)::text").extract_first()
            yield item
