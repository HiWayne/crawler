import base64
import re
from time import sleep
import requests
import scrapy

from src.items import IpItem


class IpsSpider(scrapy.Spider):
    start_page = 1
    current_page = start_page
    end_page = 52
    name = "ips"
    allowed_domains = ["89ip.cn"]
    start_urls = [
        f"https://www.89ip.cn/index_{current_page}.html"]

    def parse(self, response):
        sel = scrapy.Selector(response)
        trs = sel.css(
            "div.layui-row.layui-col-space15 table.layui-table > tbody > tr")
        index = 0
        for ip_element in trs:
            if (index != 0):
                ip = ip_element.css("td:nth-child(1)::text").get().strip()
                port = ip_element.css("td:nth-child(2)::text").get().strip()
                anonymity = ""
                type = "http"
                address = ip_element.css("td:nth-child(3)::text").get().strip()
                speed = ""
                try:
                    if (type == "socks5" or type == "SOCKS5"):
                        print("is matching socks5")
                        proxy_ip = {
                            "http": f"sock5://{ip}:{port}",
                            "https": f"sock5://{ip}:{port}"
                        }
                    else:
                        proxy_ip = {
                            "http": f"{ip}:{port}",
                            "https": f"{ip}:{port}"
                        }
                    if (type == "http" or type == "HTTP"):
                        response_text = requests.get(
                            "http://www.baidu.com", proxies=proxy_ip, timeout=10).text
                    elif (type == "https" or type == "HTTPS"):
                        response_text = requests.get(
                            "https://www.baidu.com", proxies=proxy_ip, timeout=10).text
                    else:
                        response_text = requests.get(
                            "http://www.baidu.com", proxies=proxy_ip, timeout=10).text
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
            index += 1
        self.current_page += 1
        if self.current_page <= self.end_page:
            # try:
            #     next_url = sel.css(
            #         "ul.pagination > li:last-child > a::attr('href')").get()
            #     if next_url is not None:
            #         yield response.follow(next_url, self.parse)
            #     else:
            #         print("no href, end")
            # except:
            #     print("no a, end")
            yield response.follow(f"https://www.89ip.cn/index_{self.current_page}.html", self.parse)

# ip3366代理
# class IpsSpider(scrapy.Spider):
#     start_page = 1
#     current_page = start_page
#     end_page = 7038
#     name = "ips"
#     allowed_domains = ["ip3366.net"]
#     start_urls = [
#         f"https://proxy.ip3366.net/free/?action=china&page={current_page}"]

#     def parse(self, response):
#         sel = scrapy.Selector(response)
#         trs = sel.css(
#             "section#content table > tbody > tr")
#         index = 0
#         for ip_element in trs:
#             if (index != 0):
#                 ip = ip_element.css("td:nth-child(1)::text").get()
#                 port = ip_element.css("td:nth-child(2)::text").get()
#                 anonymity = ip_element.css(
#                     "td:nth-child(3)::text").get()
#                 type = ip_element.css(
#                     "td:nth-child(4)::text").get()
#                 address = ip_element.css("td:nth-child(5)::text").get()
#                 speed = ip_element.css("td:nth-child(6)::text").get()
#                 try:
#                     if (type == "socks5" or type == "SOCKS5"):
#                         print("is matching socks5")
#                         proxy_ip = {
#                             "http": f"sock5://{ip}:{port}",
#                             "https": f"sock5://{ip}:{port}"
#                         }
#                     else:
#                         proxy_ip = {
#                             "http": f"{ip}:{port}",
#                             "https": f"{ip}:{port}"
#                         }
#                     if (type == "http" or type == "HTTP"):
#                         response_text = requests.get(
#                             "http://www.baidu.com", proxies=proxy_ip, timeout=10).text
#                     elif (type == "https" or type == "HTTPS"):
#                         response_text = requests.get(
#                             "https://www.baidu.com", proxies=proxy_ip, timeout=10).text
#                     else:
#                         response_text = requests.get(
#                             "http://www.baidu.com", proxies=proxy_ip, timeout=10).text
#                     if response_text is not None:
#                         item = IpItem()
#                         item["ip"] = ip
#                         item["port"] = port
#                         item["anonymity"] = anonymity
#                         item["type"] = type
#                         item["address"] = address
#                         item["speed"] = speed
#                         item["active"] = True
#                         yield item
#                     else:
#                         print(f'当前IP无效(返回空): {ip}:{port}')
#                         item = IpItem()
#                         item["ip"] = ip
#                         item["port"] = port
#                         item["anonymity"] = anonymity
#                         item["type"] = type
#                         item["address"] = address
#                         item["speed"] = speed
#                         item["active"] = False
#                         yield item
#                 except Exception as e:
#                     print(f'当前IP无效: {ip}:{port}')
#                     item = IpItem()
#                     item["ip"] = ip
#                     item["port"] = port
#                     item["anonymity"] = anonymity
#                     item["type"] = type
#                     item["address"] = address
#                     item["speed"] = speed
#                     item["active"] = False
#                     yield item
#             index += 1
#         self.current_page += 1
#         if self.current_page <= self.end_page:
#             # try:
#             #     next_url = sel.css(
#             #         "ul.pagination > li:last-child > a::attr('href')").get()
#             #     if next_url is not None:
#             #         yield response.follow(next_url, self.parse)
#             #     else:
#             #         print("no href, end")
#             # except:
#             #     print("no a, end")
#             yield response.follow(f"https://proxy.ip3366.net/free/?action=china&page={self.current_page}", self.parse)

# 66ip代理
# class IpsSpider(scrapy.Spider):
#     start_page = 1
#     current_page = start_page
#     end_page = 3133
#     name = "ips"
#     allowed_domains = ["66ip.cn"]
#     start_urls = [f"http://www.66ip.cn/{current_page}.html"]

#     def parse(self, response):
#         sel = scrapy.Selector(response)
#         trs = sel.css(
#             "div#main div.layui-row.layui-col-space15 table > tr")
#         index = 0
#         for ip_element in trs:
#             if (index != 0):
#                 ip = ip_element.css("td:nth-child(1)::text").get()
#                 port = ip_element.css("td:nth-child(2)::text").get()
#                 anonymity = ip_element.css(
#                     "td:nth-child(4)::text").get()
#                 type = "http"
#                 address = ip_element.css("td:nth-child(3)::text").get()
#                 speed = ""
#                 try:
#                     if (type == "socks5" or type == "SOCKS5"):
#                         print("is matching socks5")
#                         proxy_ip = {
#                             "http": f"sock5://{ip}:{port}",
#                             "https": f"sock5://{ip}:{port}"
#                         }
#                     else:
#                         proxy_ip = {
#                             "http": f"{ip}:{port}",
#                             "https": f"{ip}:{port}"
#                         }
#                     response_text = requests.get(
#                         "http://www.baidu.com", proxies=proxy_ip, timeout=10).text
#                     if response_text is not None:
#                         item = IpItem()
#                         item["ip"] = ip
#                         item["port"] = port
#                         item["anonymity"] = anonymity
#                         item["type"] = type
#                         item["address"] = address
#                         item["speed"] = speed
#                         item["active"] = True
#                         yield item
#                     else:
#                         print(f'当前IP无效(返回空): {ip}:{port}')
#                         item = IpItem()
#                         item["ip"] = ip
#                         item["port"] = port
#                         item["anonymity"] = anonymity
#                         item["type"] = type
#                         item["address"] = address
#                         item["speed"] = speed
#                         item["active"] = False
#                         yield item
#                 except Exception as e:
#                     print(f'当前IP无效: {ip}:{port}')
#                     item = IpItem()
#                     item["ip"] = ip
#                     item["port"] = port
#                     item["anonymity"] = anonymity
#                     item["type"] = type
#                     item["address"] = address
#                     item["speed"] = speed
#                     item["active"] = False
#                     yield item
#             index += 1
#         self.current_page += 1
#         if self.current_page <= self.end_page:
#             # try:
#             #     next_url = sel.css(
#             #         "ul.pagination > li:last-child > a::attr('href')").get()
#             #     if next_url is not None:
#             #         yield response.follow(next_url, self.parse)
#             #     else:
#             #         print("no href, end")
#             # except:
#             #     print("no a, end")
#             yield response.follow(f"http://www.66ip.cn/{self.current_page}.html", self.parse)

# 小幻代理
# class IpsSpider(scrapy.Spider):
#     start_page = 1
#     current_page = start_page
#     end_page = 1000
#     name = "ips"
#     allowed_domains = ["ihuan.me"]
#     start_urls = [f"https://ip.ihuan.me/?page=came0299"]

#     def parse(self, response):
#         sel = scrapy.Selector(response)
#         trs = sel.css(
#             "table.table.table-hover.table-bordered > tbody > tr")
#         for ip_element in trs:
#             ip = ip_element.css("td:nth-child(1) > a::text").get()
#             port = ip_element.css("td:nth-child(2)::text").get()
#             anonymity = ip_element.css(
#                 "td:nth-child(7) > small::text").get()
#             type = "https" if ip_element.css(
#                 "td:nth-child(5) > small::text").get() == "支持" else "http"
#             address = ip_element.css("td:nth-child(3) > a::text").get()
#             speed = ip_element.css("td:nth-child(8)::text").get()
#             try:
#                 if (type == "socks5" or type == "SOCKS5"):
#                     print("is matching socks5")
#                     proxy_ip = {
#                         "http": f"sock5://{ip}:{port}",
#                         "https": f"sock5://{ip}:{port}"
#                     }
#                 else:
#                     proxy_ip = {
#                         "http": f"{ip}:{port}",
#                         "https": f"{ip}:{port}"
#                     }
#                 response_text = requests.get(
#                     "http://www.baidu.com", proxies=proxy_ip, timeout=5).text
#                 if response_text is not None:
#                     item = IpItem()
#                     item["ip"] = ip
#                     item["port"] = port
#                     item["anonymity"] = anonymity
#                     item["type"] = type
#                     item["address"] = address
#                     item["speed"] = speed
#                     item["active"] = True
#                     yield item
#                 else:
#                     print(f'当前IP无效(返回空): {ip}:{port}')
#                     item = IpItem()
#                     item["ip"] = ip
#                     item["port"] = port
#                     item["anonymity"] = anonymity
#                     item["type"] = type
#                     item["address"] = address
#                     item["speed"] = speed
#                     item["active"] = False
#                     yield item
#             except Exception as e:
#                 print(f'当前IP无效: {ip}:{port}')
#                 item = IpItem()
#                 item["ip"] = ip
#                 item["port"] = port
#                 item["anonymity"] = anonymity
#                 item["type"] = type
#                 item["address"] = address
#                 item["speed"] = speed
#                 item["active"] = False
#                 yield item
#         self.current_page += 1
#         if self.current_page <= self.end_page:
#             try:
#                 next_url = sel.css(
#                     "ul.pagination > li:last-child > a::attr('href')").get()
#                 if next_url is not None:
#                     yield response.follow(next_url, self.parse)
#                 else:
#                     print("no href, end")
#             except:
#                 print("no a, end")

# 站大爷

# class IpsSpiderZDaYe(scrapy.Spider):
#     start_page = 1
#     current_page = start_page
#     end_page = 1000
#     name = "ips"
#     allowed_domains = ["zdaye.com"]
#     start_urls = [f"https://www.zdaye.com/dayProxy/ip/335035/"]

#     def parse(self, response):
#         sel = scrapy.Selector(response)
#         trs = sel.css(
#             "table#ipc > tbody > tr")
#         for ip_element in trs:
#             ip = re.sub(r'[^\d.]', "", ip_element.css(
#                 "td:nth-child(1)::text").get())
#             port = re.sub(r'[^\d]', "", ip_element.css(
#                 "td:nth-child(2)::text").get())
#             anonymity = ip_element.css("td:nth-child(4)::text").get()
#             type = ip_element.css("td:nth-child(3)::text").get()
#             address = ip_element.css("td:nth-child(5)::text").get()
#             speed = ""
#             try:
#                 proxy_ip = {
#                     "http": f"{ip}:{port}",
#                     "https": f"{ip}:{port}"
#                 }
#                 response_text = requests.get(
#                     "http://www.baidu.com", proxies=proxy_ip, timeout=5).text
#                 if response_text is not None:
#                     item = IpItem()
#                     item["ip"] = ip
#                     item["port"] = port
#                     item["anonymity"] = anonymity
#                     item["type"] = type
#                     item["address"] = address
#                     item["speed"] = speed
#                     item["active"] = True
#                     yield item
#                 else:
#                     print(f'当前IP无效(返回空): {ip}:{port}')
#                     item = IpItem()
#                     item["ip"] = ip
#                     item["port"] = port
#                     item["anonymity"] = anonymity
#                     item["type"] = type
#                     item["address"] = address
#                     item["speed"] = speed
#                     item["active"] = False
#                     yield item
#             except Exception as e:
#                 print(f'当前IP无效: {ip}:{port}')
#                 item = IpItem()
#                 item["ip"] = ip
#                 item["port"] = port
#                 item["anonymity"] = anonymity
#                 item["type"] = type
#                 item["address"] = address
#                 item["speed"] = speed
#                 item["active"] = False
#                 yield item
#         self.current_page += 1
#         if self.current_page <= self.end_page:
#             try:
#                 next_url = sel.css(
#                     "div.page > a.layui-btn.layui-btn-xs[title=下一页]::attr('href')").get()
#                 if next_url is not None:
#                     yield response.follow(next_url, self.parse)
#                 else:
#                     print("no href, end")
#             except:
#                 print("no a, end")
