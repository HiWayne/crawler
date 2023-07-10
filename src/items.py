# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousePriceCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 小区名
    price = scrapy.Field()  # 人民币/平方米
    address = scrapy.Field()  # 地点
    construction_time = scrapy.Field()  # 建造时间, 公元年
    distance = scrapy.Field()  # 到市中心的距离, m


class IpItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    active = scrapy.Field()  # 是否有效
    anonymity = scrapy.Field()  # 匿名度
    type = scrapy.Field()  # 类型 e.g. HTTP
    address = scrapy.Field()  # 位置
    speed = scrapy.Field()  # 响应速度
