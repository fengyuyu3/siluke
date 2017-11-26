# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from siluke.items import SilukeItem
import re

class SsilukeSpider(RedisSpider):
    name = 'ssiluke'
    # start_urls = ['http://www.siluke.tw']
    redis_key = "ssiluke:start_urls"
    def parse(self, response):
        node_list = response.xpath('//div[@class="nav"]//li')
            # compile = re.compile(r"/ny_\d+/",re.S)
            # node_list = re.findall(compile,response.text)
        for node in node_list:
           # name = node.xpath('./a/text()').extract()[0]
            url = node.xpath('./a/@href').extract()[0]
            match = re.compile(r"/ny_\d+/", re.S)
            is_urls = re.findall(match, url)
            for my_url in is_urls:
                if len(my_url) != 0:
                    host_url = 'http://www.siluke.tw'+my_url
                    yield scrapy.Request(host_url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        node_list = response.xpath('//dt')
        for node in node_list:
            # story_author = node.xpath('./span/text()').extract()[0] #作者
            # story_name = node.xpath('./a/text()').extract()[0] #小说名字
            story_link = 'http://www.siluke.tw'+node.xpath('./a/@href').extract()[0]  #小说链接
            yield scrapy.Request(story_link, callback=self.parse_child_contents)
            # print (story_link)
        node_list1 = response.xpath('//li/span[@class="s2"]')
        for node1 in node_list1:
            story_link1 = 'http://www.siluke.tw'+node1.xpath('./a/@href').extract()[0] #小说链接
            print(story_link1)
            yield scrapy.Request(story_link1, callback=self.parse_child_contents)

    def parse_child_contents(self, response):
        story_section = response.xpath('//dd/a/@href')
        story_link = 'http://www.siluke.tw' + story_section[0].extract()
        print(story_link)
        yield scrapy.Request(story_link, callback=self.parse_child_contents_details)

    def parse_child_contents_details(self, response):
        item = SilukeItem()
        section_name = response.xpath('//div[@class="con_top"]/a/text()')#标题
        item["name"] = section_name.extract()[2]
        section_title = response.xpath('//div[@class="bookname"]/h1/text()')  # 章节名字
        item["title"] = section_title.extract()[0]
        section_content = response.xpath('//div[@id="content"]/text()').extract()  # 章节内容
        section_next_link = response.xpath('//div[@class="bottem1"]/a/@href')

        text1 = "\n" + section_title.extract()[0] + "\n"
        text2 = ""
        for text in section_content:
            text2 = text2+text+"\n"
        item["content"] = text1 + text2
        yield item

        if section_next_link.extract()[2] != section_next_link.extract()[1]:
            print(section_next_link.extract()[2] + "   " + section_next_link.extract()[1])
            yield scrapy.Request('http://www.siluke.tw' + section_next_link.extract()[2],
                                 callback=self.parse_child_contents_details)