# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem
import re


class HrtencentSpider(scrapy.Spider):
    name = 'hrTencent3'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']
    offset = 0

    def parse(self, response):
        datas = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')

        for data in datas:
            item = TencentItem()
            content_url = 'http://hr.tencent.com/' + ''.join(data.xpath('./td[1]/a/@href').extract())
            item["publishTime"] = ''.join(data.xpath("./td[5]/text()").extract())
            meta = {'item': item}
            yield scrapy.Request(content_url, callback=self.parse_content, meta=meta)

        if self.offset < 1000:
            self.offset += 10
            newurl = 'https://hr.tencent.com/position.php?&start=' + str(self.offset) + '#a'
            yield scrapy.Request(newurl, callback=self.parse)

    def parse_content(self, response):
        item = response.meta['item']
        item['title'] = ''.join(response.xpath("//tr[@class='h']/td/text()").extract())

        # 把招聘要求和岗位职责拼接在一起
        content = ''.join(
            [job + '\n' for job in response.xpath("//tr[@class='c'][1]//text()").extract()] +
            [job + '\n' for job in response.xpath("//tr[@class='c'][2]//text()").extract()]).rstrip()
        print(content)
        # 去掉招聘信息里的空格/换行等
        item['content'] = content.replace("\r", '') \
            .replace("                \n", '').replace("            \n", '').replace('    ', '')

        item['workLocation'] = ''.join(response.xpath("//tr[@class='c bottomline']/td[1]/text()").extract())
        item['category'] = ''.join(response.xpath("//tr[@class='c bottomline']/td[2]/text()").extract())

        p_num = ''.join(response.xpath("//tr[@class='c bottomline']/td[3]/text()").extract())
        peopleNumber = re.findall('\d+', p_num)[0]
        item['peopleNumber'] = peopleNumber

        yield item
