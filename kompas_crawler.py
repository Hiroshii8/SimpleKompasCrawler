from bs4 import BeautifulSoup
import requests
import json

def SimpleCrawler(url):
	result = []
	req = requests.get(url)
	soup = BeautifulSoup(req.text, "lxml")

	#Iterate Every Page Until End
	paging = soup.find_all("div", {'class' : 'paging clearfix'})
	paging_link = paging[0].find_all('a',{'class' : 'paging__link'})
	last_page = int([item.get('href').split('/')[-1] for item in paging_link][-1])
	print(paging)
	
	for i in range(1, last_page):
		print(url+str(i))

		#find article link
		req = requests.get(url+str(i))
		soup = BeautifulSoup(req.text, "lxml")
		new_links = soup.find_all("div",{'class':'article__list clearfix'})

		
		for idx,news in enumerate(new_links):
			news_dict = {}

			#News Title
			title_news = news.find('a',
				{'class':'article__link'}).text
			
			#News URL
			url_news = news.find('a',
				{'class':'article__link'}).get('href')

			#News Link
			req_news = requests.get(url_news)
			soup_news = BeautifulSoup(req_news.text, "lxml")

			#News Content
			news_content = soup_news.find("div",
				{'class':'read__content'})
			p = news_content.find_all('p')
			content = ' '.join(item .text for item in p)
			news_content = content.encode('utf8','replace')

			#Indexing
			news_dict['id'] = idx
			news_dict['url'] = url_news
			news_dict['title'] = title_news
			news_dict['content'] = news_content
			result.append(news_dict)
	return result

Url = 'URL_KOMPAS'
res = SimpleCrawler(Url)
print(res)
