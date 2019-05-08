
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import os
import csv
import scrapy
from CrawlerAndroid.items import categoryItem, CrawlerandroidItem


class CrawlerandroidPipeline(object):

	dup_itm = set()
	app_dup = set()

	#the location of csv file
	filePath = 'xiaomi.csv' 

	# open the file
	
	writer = csv.writer(open(filePath, 'w', newline='', encoding='utf-8-sig'))
	#writer.writeheader("categoryName", "categoryId", "subLink", "maxPage", "appNum")
	writer.writerow(["categoryName", "categoryId", "subLink", "maxPage", "appNum"])

	appList_file = 'appList.csv'
	app_writer = csv.writer(open(appList_file, 'w', newline='', encoding='utf-8-sig'))
	#writer.writeheader("categoryName", "categoryId", "subLink", "maxPage", "appNum")
	app_writer.writerow(["appId", "name", "category", "size", "packName", "permissionList", "info", "downloadLink", "company", "detected"])


	def process_item(self, item, spider):
		if isinstance(item,categoryItem):
			if item['categoryId'] not in self.dup_itm:
				self.dup_itm.add(item['categoryId'])
				self.writer.writerow([item['categoryName'],item['categoryId'], item['subLink'],item['maxPage'],item['appNum']])
			else:
				raise DropItem("Duplicate item found:%s" %item)
		elif isinstance(item, CrawlerandroidItem):
			if item['appId'] not in self.app_dup:
				self.app_dup.add(item['appId'])
				self.app_writer.writerow([item['appId'], item['name'], item['category'], item['size'], item['packName'], item['permissionList'], item['info'], item['downloadLink'][0], item['company'], item['detected']])
			else:
				raise DropItem("Duplicate apps %s" % item)
		return item



		'''
		if item['categoryId'] not in self.dup_itm:
			self.dup_itm.add(item['categoryId'])
		#self.writer.writeheader()
			self.writer.writerow([item['categoryName'],item['categoryId'], item['subLink'],item['maxPage'],item['appNum']])
			#return item
		#if item['appId'] in self.app_dup:
		#	raise DropItem("Duplicate apps %s" % item)
		#else:
		#	self.app_dup.add(item['appId'])
		self.app_writer.writerow([item['appId'], item['name'], item['category'], item['size'], item['packName'], item['permissionList'], item['info'], item['downloadLink'][0], item['company'], item['detected']])
			#return item
			'''
'''
class ApplicationPipeline(object):
	"""docstring for ApplicationPipeline"""
	

	def __init__(self, arg):
		super(ApplicationPipeline, self).__init__()
		self.arg = arg
	
	dup_itm = set()

	filePath = 'appList.csv'
	writer = csv.writer(open(filePath, 'w', newline='', encoding='utf-8-sig'))
	writer.writerow(["appId", "name", "category", "size", "packName", "permissionList", "info", "downloadLink", "company", "detected"])


	def process_item(self, item, info):
		if isinstance(item, CrawlerandroidItem):
			if item['appId'] in self.dup_itm:
				raise DropItem("Duplicate item found:%s" %item)
			else:
				self.dup_itm.add(item['categoryId'])
				self.writer.writerow([item['appId'], item['name'], item['category'], item['size'], item['packName'], item['permissionList'], item['info'], item['downloadLink'], item['company'], item['detected']])
				return item
'''






