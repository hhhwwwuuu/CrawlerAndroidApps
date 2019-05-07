
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import os
import csv
import scrapy


class CrawlerandroidPipeline(object):

	dup_itm = set()

	#the location of csv file
	filePath = 'xiaomi.csv' 

	# open the file
	
	writer = csv.writer(open(filePath, 'w', newline='', encoding='utf-8-sig'))
	#writer.writeheader("categoryName", "categoryId", "subLink", "maxPage", "appNum")
	writer.writerow(["categoryName", "categoryId", "subLink", "maxPage", "appNum"])


	def process_item(self, item, spider):
		if item['categoryId'] in self.dup_itm:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.dup_itm.add(item['categoryId'])
		#self.writer.writeheader()
		self.writer.writerow([item['categoryName'],item['categoryId'], item['subLink'],item['maxPage'],item['appNum']])
		return item


class ApplicationPipeline(object):
	"""docstring for ApplicationPipeline"""
	'''
	def __init__(self, arg):
		super(ApplicationPipeline, self).__init__()
		self.arg = arg
	'''
	dup_itm = set()

	filePath = 'appList.csv'
	writer = csv.writer(open(filePath, 'w', newline='', encoding='utf-8-sig'))
	writer.writerow(["appId", "name", "category", "size", "packName", "permissionList", "info", "downloadLink", "company", "detected"])


	def process_item(self, item, spider):
		if item['appId'] in self.dup_itm:
			raise DropItem("Duplicate item found:%s" %item)
		else:
			if float(item['size'][:-2]) > 200:
				raise DropItem("Large item found:%s" %item)
			else:
				self.writer.writerow([item['appId'], item['name'], item['category'], item['size'], item['packName'], item['permissionList'], item['info'], item['downloadLink'], item['company'], item['detected']])
				baseUrl = 'http://app.mi.com'
				yield scrapy.Request(baseUrl+item['downloadLink'])





