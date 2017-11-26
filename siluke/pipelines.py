# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class SilukePipeline(object):

    def process_item(self, item, spider):
        f = open(item["name"], "ab+")
        content = str(item["content"])
        # print(item["name"])
        f.write(content.encode("utf-8"))
        f.close()
        return item
