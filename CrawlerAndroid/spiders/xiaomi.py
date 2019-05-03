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
    		yield scrapy.FormRequest(url= baseUrl,method='GET', callback=self.maxPage, formdata=formdata, dont_filter = True)

    	'''
    	self.allowed_domains.append("http://app.mi.com/category/26")
    	#print(self.allowed_domains)
    	formdata = {
    		"page": "0",
    		"categoryId": "26",
    		"pageSize": "30"
    	}
    	yield scrapy.FormRequest(url="http://app.mi.com/categotyAllListApi?",method='GET', callback=self.getCategoryPage, formdata=formdata, dont_filter = True)
    	'''


    def maxPage(self,response):
    	jsonBody = json.loads(response.body.decode('utf-8'))
    	maxPage = math.ceil(jsonBody['count'] / 30)
    	print(maxPage)
    	#return maxPage


    #divie into the detailed page for each category
    #get the maxium page number and each link of app
    def getCategoryPage(self, response):
    	print("===========================")

    	jsonBody = json.loads(response.body.decode('utf-8'))
    	appNums = jsonBody['count']
    	maxPage = math.ceil(appNums / 30)
    	print(maxPage)
    	models = jsonBody['data']
    	for each in models:
    		print(each['displayName'])
    	'''
    	item = response.meta['item']
    	#soup = BeautifulSoup(response.text, features="lxml")
    	#print(soup.prettify())
    	for each in response.xpath("//ul[@class='applist']/li/h5"):
    		link = each.xpath("a/@href").extract_first()
    		name = each.xpath("a/text()")
    		print(name, link)

    	#item['maxPage'] 
    	#soup = BeautifulSoup(response.text, features="lxml")
    	#print(maxPage)
    	
    	for pageNum in range(maxPage):
    		url = str(response.url) + '#page=' + pageNum
    		print(url)
    		#yield scrapy.Request(url, self.getAppLink)

    
    def getAppLink(self, response):

    	for each in response.xpath("//ul[@id='all-applist']//li"):
    		downLink = self.baseUrl + each.xpath("a/@href").extract_first()
    		appName = each.xpath("a/img/@alt").extract_first()
    		print(appName, downLink)
    		yield scrapy.Request(downLink, self.getAppInfo)

    def getAppInfo(self, response):
    	pass
    '''
