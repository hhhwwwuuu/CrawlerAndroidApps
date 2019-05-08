# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerandroidItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	category = scrapy.Field()
	name = scrapy.Field()
	size = scrapy.Field()
	packName = scrapy.Field()
	appId = scrapy.Field()
	permissionList = scrapy.Field()
	info = scrapy.Field()
	downloadLink = scrapy.Field()
	detected = scrapy.Field()
	company = scrapy.Field()

class categoryItem(scrapy.Item):
	"""docstring for categoryItem"""
	categoryName = scrapy.Field()
	subLink = scrapy.Field()
	categoryId = scrapy.Field()
	maxPage = scrapy.Field()
	appNum = scrapy.Field()
	'''
	category = scrapy.Field()
	name = scrapy.Field()
	size = scrapy.Field()
	packName = scrapy.Field()
	appId = scrapy.Field()
	permissionList = scrapy.Field()
	info = scrapy.Field()
	downloadLink = scrapy.Field()
	detected = scrapy.Field()
	company = scrapy.Field()
	'''
