# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

class SaveLinksAsyncPipeline:
    def open_spider(self, spider):
        self.links = set()

    def process_item(self, item, spider):
        if 'url' in item:
            self.links.add(item['url'])
        return item

    def close_spider(self, spider):
        with open('output.txt', 'w') as f:
            for link in self.links:
                f.write(link + '\n')
