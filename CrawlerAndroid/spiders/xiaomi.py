# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from CrawlerAndroid.items import categoryItem, CrawlerandroidItem
from scrapy.http import Request
from scrapy_splash import SplashRequest
#from scrapy.http import FormRequest
import json
import codecs
import sys
import math


class XiaomiSpider(scrapy.Spider):
	name = 'xiaomi'
	allowed_domains = ['app.mi.com']
	start_urls = ['http://app.mi.com']
	category = {}
	

	def parse(self, response):
		#get the info of categories from main page
		#print(response.text)
		for each in response.xpath("//body//div/ul[@class='category-list']/li/a"):
			item = categoryItem()
			item['categoryName'] = each.xpath('text()').extract_first()
			item['subLink'] = each.xpath('@href').extract_first()
			item['categoryId'] = each.xpath('@href').re(r'\d+')[0]

			tmpLink = self.start_urls[0] + each.xpath('@href').extract_first() 		
			#print(tmpLink)
			#目前处于mock测试 后续要在此处对url进行遍历，而非下面的
			
			formdata = {
				"page": "0",
				"categoryId": item['categoryId'],
				"pageSize": "30"
			}
			baseUrl = "http://app.mi.com/categotyAllListApi?"
			yield scrapy.FormRequest(url= baseUrl,method='GET', callback=self.geteachpage, formdata=formdata, dont_filter = True, meta={'item':item})
			'''
		formdata = {
				"page": "0",
				"categoryId": "28",
				"pageSize": "30"
		}
		baseUrl = "http://app.mi.com/categotyAllListApi?"
		item = categoryItem()
		item['categoryName'] = "塔防迷宫"
		item['subLink'] = "category/28"
		item['categoryId'] = "28"
		yield scrapy.FormRequest(url= baseUrl,method='GET', callback=self.geteachpage, formdata=formdata, dont_filter = True, meta={'item':item})
		'''
			#print("===========================")
			#print(item['categoryName'], item['maxPage'])
			#print("===========================")


	def geteachpage(self,response):
		jsonBody = json.loads(response.body.decode('utf-8'))
		item = response.meta['item']
		item['maxPage'] = math.ceil(jsonBody['count'] / 30)
		item['appNum'] = int(jsonBody['count'])
		#print(item)
		#print(item['categoryName'], item['maxPage'])
		#print("===========================")
		
		for pageNum in range(item['maxPage']):
			formdata = {
				"page": str(pageNum),
				"categoryId": item['categoryId'],
				"pageSize": "30"
			}
			baseUrl = "http://app.mi.com/categotyAllListApi?"
			yield scrapy.FormRequest(url= baseUrl,method='GET', callback=self.getAppsFromPage, formdata=formdata, dont_filter = True, meta={'item':item})
		'''
		formdata = {
				"page": "0",
				"categoryId": item['categoryId'],
				"pageSize": "30"
			}
		baseUrl = "http://app.mi.com/categotyAllListApi?"
		yield scrapy.FormRequest(url= baseUrl,method='GET', callback=self.getAppsFromPage, formdata=formdata, dont_filter = True, meta={'item':item})
		#return item
		'''


	#divie into the detailed page for each category
	#get the maxium page number and each link of app
	def getAppsFromPage(self, response):
		#print("===========================")
		#print(response.url)
		jsonBody = json.loads(response.body.decode('utf-8'))
		models = jsonBody['data']
		#item = CrawlerandroidItem()
		#item = response.meta['item']
		#print(models)
		baseUrl = "http://app.mi.com/details?id="
		for each in models:
			#print(each['displayName'])
			#item['category'] = each['level1CategoryName']
			#item['name'] = each['displayName']
			packageName = each['packageName']
			#item['appId'] = each['appId']
			#print(item['packName'])
			yield scrapy.Request(baseUrl+packageName, callback = self.getAppInfo, dont_filter=True, meta={'categoryItem': response.meta['item']})

		
	def getAppInfo(self, response):
		item = CrawlerandroidItem()
		#print("===========================")
		item['name'] = response.xpath("//div[6]/div[1]/div[2]/div[1]/div/h3/text()").extract_first()
		item['category'] = response.xpath("//div[6]/div[1]/div[2]/div[1]/div/p[2]/text()[1]").extract_first()
		item['packName'] = response.xpath("//div[6]/div[1]/div[2]/div[2]/div/ul[1]/li[8]/text()").extract_first()
		item['appId'] = response.xpath("//div[6]/div[1]/div[2]/div[2]/div/ul[1]/li[10]/text()").extract_first()

		item['company'] = response.xpath("//div[@class='intro-titles']/p[1]/text()").extract_first()
		item['size'] = response.xpath("//div[@class='details preventDefault']//ul[@class=' cf']/li[2]/text()").extract_first()
		item['permissionList'] = response.xpath("//div[@class='details preventDefault']//ul[@class='second-ul']/li/text()").extract()
		#print(item['permissionList'])
		item['info'] = response.xpath("//div[6]/div[1]/div[4]/p/text()").extract()
		item['downloadLink'] = response.xpath("//div[@class='app-info-down']/a/@href").extract()
		item['detected'] = False
		#print(item)
		#print("===========================")
		#return item
		return item, response.meta['categoryItem']
