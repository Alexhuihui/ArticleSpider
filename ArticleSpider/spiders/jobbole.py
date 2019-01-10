# -*- coding: utf-8 -*-
import datetime

import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.utils.common import get_md5

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader


class JobboleSpider(scrapy.Spider):
	name = 'jobbole'
	allowed_domains = ['blog.jobbole.com']
	start_urls = ['http://blog.jobbole.com/all-posts/']
	
	def parse(self, response):
		"""
		1. 获取文章列表页面的文章url交给scrapy下载并进行解析
		2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
		"""
		post_nodes = response.css("#archive .floated-thumb .post-thumb a")
		for post_node in post_nodes:
			image_url = post_node.css("img::attr(src)").extract_first("")
			post_url = post_node.css("::attr(href)").extract_first("")
			yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
			              callback=self.parse_detail)
		
		next_url = response.xpath('//*[@id="archive"]/div[21]/a[4]/@href').extract_first("")
		if next_url:
			yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
	
	def parse_detail(self, response):
		# 提取文章的具体信息
		# article_item = JobBoleArticleItem()
		#
		# title = response.css(".entry-header h1::text").extract_first("")
		# front_image_url = response.meta.get('front_image_url', '')
		# create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first("").strip().replace('·',
		#                                                                                                   '').strip()
		# praise_nums = response.css(".vote-post-up h10::text").extract_first("")
		# fav_nums = response.css(".bookmark-btn::text").extract_first("")
		# match_re = re.match(".*?(\d+).*", fav_nums)
		# if match_re:
		# 	fav_nums = match_re.group(1)
		# else:
		# 	fav_nums = 0
		#
		# comment_nums = response.css("a[href='#article-comment'] span::text").extract_first("")
		# match_re = re.match(".*?(\d+).*", comment_nums)
		# if match_re:
		# 	comment_nums = match_re.group(1)
		# else:
		# 	comment_nums = 0
		#
		# content = response.css("div.entry").extract_first("")
		# tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
		# tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
		# tags = ','.join(tag_list)
		#
		# article_item['url_object_id'] = get_md5(response.url)
		# article_item['title'] = title
		# article_item['url'] = response.url
		# try:
		# 	create_date = datetime.datetime.strtime(create_date, '%Y/%m/%d').date()
		# except Exception as e:
		# 	create_date = datetime.datetime.now().date()
		# article_item['create_date'] = create_date
		# article_item['front_image_url'] = [front_image_url]
		# article_item['praise_nums'] = praise_nums
		# article_item['comment_nums'] = comment_nums
		# article_item['fav_nums'] = fav_nums
		# article_item['tags'] = tags
		# article_item['content'] = content

		front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
		item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
		item_loader.add_css("title", ".entry-header h1::text")
		item_loader.add_value("url", response.url)
		item_loader.add_value("url_object_id", get_md5(response.url))
		item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
		item_loader.add_value("front_image_url", [front_image_url])
		item_loader.add_css("praise_nums", ".vote-post-up h10::text")
		item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
		item_loader.add_css("fav_nums", ".bookmark-btn::text")
		item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
		item_loader.add_css("content", "div.entry")

		article_item = item_loader.load_item()
		
		# 跳转到piplines中
		yield article_item
