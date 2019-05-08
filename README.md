# CrawlerAndroidApps
# Android应用爬虫
***
采用Python Scrapy框架对小米应用商城的app进行抓取。
抓取方式：
* 主页静态抓取所有app分类的下级目录
* FormRequest app分类的二级目录，可以获得动态数据：该分类的app总个数，该页面下的app的信息
* scrapy.Request 页面下每一个app的详情，将下载连接及所有文本保存在csv文件下
* app分类信息统计保存在csv文件下