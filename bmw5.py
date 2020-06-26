# -*- coding: utf-8 -*-
import scrapy
from bmw.items import BmwItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html']
    rules = (
        #allow的是更多的链接地址，所以需要解析并且跟进，因为有可能有多页
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/65.+"),callback="parse_page",follow=True),
    )


    def parse_page(self, response):
        # 因为得到的第一个不需要，所以用[1:]
        # uiboxs = response.xpath("//div[@class='uibox']")[1:]
        # categorys=[]
        # for uibox in uiboxs:
        #     # get()只得到第一个text文本
        #     category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
        #     categorys.append(category)
        category=response.xpath("//div[@class='uibox']/div/text()").get()

        #class 有好几个所以用contains只要写出其中一个
        srcs=response.xpath("//div[contains(@class,'uibox-con')]/ul/li/a/img/@src").getall()
        srcs=list(map(lambda x:x.replace("240x180_0_q95_c42_",""),srcs))
        # urls=[]
        # for src in srcs:
        #     url=response.urljoin(src)
        #     urls.append(url)
        srcs=list(map(lambda x:response.urljoin(x),srcs))
        yield BmwItem(category=category,image_urls=srcs)


    '''
    def parse(self, response):
        注释的是传统方法，后来是scrapy自带的方法，
        现在的代码是获取高清图片的代码
        #返回的是一个SelectorList类型的列表
        #因为得到的第一个不需要，所以用[1:]
        uiboxs=response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            #get()只得到第一个text文本
            category=uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            # print(category)
            urls=uibox.xpath(".//ul/li/a/img/@src").getall()
            # print(urls)
            # for url in urls:
            #     #将url拼结成完整的网址
            #     # url="https:"+url   等价于下面的方法
            #     url=response.urljoin(url)
            #     print(url)
            #这个方法等价于上面的for循环，将urls转换成网址
            urls=list(map(lambda url:response.urljoin(url),urls))

            #传统的方法
            # item=BmwItem(category=category,urls=urls)

            #scrapy自带的方法
            item = BmwItem(category=category, image_urls=urls)
            yield item
    '''