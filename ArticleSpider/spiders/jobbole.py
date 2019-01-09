# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
	name = 'jobbole'
	allowed_domains = ['blog.jobbole.com']
	start_urls = ['http://blog.jobbole.com/all-posts/']
	
	def parse(self, response):
		"""
		1. 获取文章列表页面的文章url交给scrapy下载并进行解析
		2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
		"""
		post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
		for post_url in post_urls:
			yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
			
		next_url = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href').extract_first("")
		if next_url:
			yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
		
		
	
	def parse_detail(self, response):
		# 提取文章的具体信息
		title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
		create_time = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract_first("").strip().replace('·', '').strip()
		praise_nums = response.xpath('//*[@id="110287votetotal"]/text()').extract_first("")
		fav_nums = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/span[2]/text()').extract_first("")
		match_re = re.match(".*?(\d+).*", fav_nums)
		if match_re:
			fav_nums = match_re.group(1)
		else:
			fav_nums = 0
		
		comment_nums = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/a/span/text()').extract_first("")
		match_re = re.match(".*?(\d+).*", comment_nums)
		if match_re:
			comment_nums = match_re.group(1)
		else:
			comment_nums = 0
		
		content = response.xpath('//div[@class="entry"]').extract_first("")
		tag_list = response.xpath('//*[@id="post-110287"]/div[2]/p/a/text()').extract()
		tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
		tags = ','.join(tag_list)
