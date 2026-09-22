# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class CleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        price = adapter.get("price")
        if isinstance(price, str):
            match = re.match(r"(\d+)\.(\d+)", price)
            if match:
                adapter["price"] = float(match.group())
            else:
                adapter["price"] = None

        if adapter.get("star_rating") is not None:
            adapter["star_rating"] = int(adapter["star_rating"])

        if adapter.get("number_available") is not None:
            adapter["number_available"] = int(adapter["number_available"])

        if adapter.get("description"):
            adapter["description"] = " ".join(adapter["description"].split())

        for champ in ("title", "category"):
            if adapter.get(champ):
                adapter[champ] = adapter[champ].strip()

        return item