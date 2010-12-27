#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import urllib2
import PyRSS2Gen
from BeautifulSoup import BeautifulSoup
import re
import datetime

def get_bodytext(link):
	global bodytext
	webcontent = urllib2.urlopen(link).read()

	#对内容进行解析
	soup = BeautifulSoup(webcontent)
	
	bodytext_soup = soup.find('div', {"id":"bodytext"}).findAll('p')
	for p in bodytext_soup:
		bodytext = bodytext + "<p>" + p.renderContents() + "</p>"

	pagination = soup.find('div', {"class":"pagination"}).renderContents()
	
	match=re.search('<a href="([^"]+)">下一页</a>', pagination)
	if match:
		nextpage_link = "http://www.ftchinese.com" + match.group(1)
		get_bodytext(nextpage_link)

def rss_generator(entries):
	items = []	
	for entry in entries:
		title = entry["title"]
		link = entry["link"]
		pubDate = entry["updated"]
		global bodytext
		bodytext = ""
		get_bodytext(link)
		
		items.append(PyRSS2Gen.RSSItem(
			title = title,
			link = link,
			description = bodytext.decode("UTF-8"),
			guid = PyRSS2Gen.Guid(link),
			pubDate = pubDate
		))

	feed_data = PyRSS2Gen.RSS2(
		title=u"FT中文网 - 每日新闻全文RSS输出",
		link="http://www.ftchinese.com",
		description=u"FT中文网每日新闻全文RSS输出 制作 by @easthero",
		lastBuildDate=datetime.datetime.now(),
		language="zh-cn",
		managingEditor="ftchinese.editor@ft.com (ftchinese)",
		webMaster="customer.service@ftchinese.com (ftchinese)",
		generator="ftchinese.com",
		ttl="86400",
		items = items
	)
	print 'Content-type:text/xml; charset=UTF-8'
	print '<?xml version="1.0" encoding="UTF-8"?>'
	print feed_data.to_xml(encoding="UTF-8")

rss_source = "http://www.ftchinese.com/rss/news"
if __name__ == "__main__":
	source = feedparser.parse(urllib2.urlopen(rss_source).read())
	entries = source["entries"]
	rss_generator(entries)
