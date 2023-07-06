# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
import re
import requests


class HousePriceCrawlerPipeline:
    destination_lat = 31.240081
    destination_lng = 121.481176

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("price"):
            adapter["price"] = re.findall(r"\d+", adapter["price"])
        if adapter.get("construction_time"):
            adapter["construction_time"] = re.findall(
                r"\d+", adapter["construction_time"])
        if adapter.get("address"):
            r1 = requests.get(
                f"https://api.map.baidu.com/geocoding/v3/?address={adapter['address']}&output=json&ak=C9cevD681A0IdCYsASFZx3GN2RlA9cH5")
            json1 = r1.json()
            if json1["status"] == 0:
                location = json1["result"]["location"]
                # 经度值
                lng = location["lng"]
                # 纬度值
                lat = location["lat"]
                r2 = requests.get(
                    f"https://api.map.baidu.com/directionlite/v1/transit?origin={lat},{lng}&destination={self.destination_lat},{self.destination_lng}&ak=C9cevD681A0IdCYsASFZx3GN2RlA9cH5")
                json2 = r2.json()
                if json2["status"] == 0:
                    def compare_by_distance(item):
                        return item['distance']
                    min_item = min(json2["result"]["routes"],
                                   key=compare_by_distance)
                    adapter["distance"] = min_item["distance"]
        return item
