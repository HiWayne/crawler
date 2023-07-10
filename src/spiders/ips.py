from time import sleep
import requests
import scrapy

from src.items import IpItem


class IpsSpider(scrapy.Spider):
    start_page = 400
    current_page = start_page
    end_page = 1000
    name = "ips"
    allowed_domains = ["kuaidaili.com"]
    start_urls = [f"https://www.kuaidaili.com/free/inha/{start_page}/"]

    def parse(self, response):
        sel = scrapy.Selector(response)
        trs = sel.css(
            "table.table.table-b.table-bordered.table-striped > tbody > tr")
        for ip_element in trs:
            ip = ip_element.css("td[data-title=IP]::text").get()
            port = ip_element.css("td[data-title=PORT]::text").get()
            anonymity = ip_element.css("td[data-title=匿名度]::text").get()
            type = ip_element.css("td[data-title=类型]::text").get()
            address = ip_element.css("td[data-title=位置]::text").get()
            speed = ip_element.css("td[data-title=响应速度]::text").get()
            try:
                proxy_ip = {
                    "http": f"{ip}:{port}",
                    "https": f"{ip}:{port}"
                }
                response_text = requests.get(
                    "http://www.baidu.com", proxies=proxy_ip, timeout=5).text
                if response_text is not None:
                    item = IpItem()
                    item["ip"] = ip
                    item["port"] = port
                    item["anonymity"] = anonymity
                    item["type"] = type
                    item["address"] = address
                    item["speed"] = speed
                    item["active"] = True
                    yield item
                else:
                    print(f'当前IP无效(返回空): {ip}:{port}')
                    item = IpItem()
                    item["ip"] = ip
                    item["port"] = port
                    item["anonymity"] = anonymity
                    item["type"] = type
                    item["address"] = address
                    item["speed"] = speed
                    item["active"] = False
                    yield item
            except Exception as e:
                print(f'当前IP无效: {ip}:{port}')
                item = IpItem()
                item["ip"] = ip
                item["port"] = port
                item["anonymity"] = anonymity
                item["type"] = type
                item["address"] = address
                item["speed"] = speed
                item["active"] = False
                yield item
        self.current_page += 1
        if self.current_page <= self.end_page:
            next_url = sel.css(
                "ul.v3__pagination.param-type-1 > li.v3__pagination-next > a::attr('href')").get()
            if next_url is not None:
                yield response.follow(next_url, self.parse)
