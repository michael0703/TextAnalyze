
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import json
import datetime
import time
class Crawler():
    
    def __init__(self):
        
        self.forum_domain = {'ptt':'https://www.ptt.cc/', 'udn':'https://udn.com', 'setn':'https://www.setn.com'}
        self.index_url = {'ptt':'https://www.ptt.cc/bbs/{}/index.html', 'udn':'https://udn.com/news/breaknews/1', 'udn-lazyupload':'https://udn.com/news/get_breaks_article/{}/1/0?_={}', 
                             'setn':'https://www.setn.com/ViewAll.aspx?p={}'
                         }
        requests.adapters.DEFAULT_RETRIES = 5


    def GetPTTNewsMeta(self, section, limit):

        count = 0
        Round = 0
        page_url = self.index_url['ptt'].format(section)
        news_meta = []
        
        while count <= limit:

            r = requests.get(page_url)
            r.keep_alive = False    
            if section == "Gossiping":
                r = requests.post(r.url, data = {'yes':'yes'})
                
            r.encoding = 'utf-8'
            soup = bs(r.text, 'html.parser')

            news_block = soup.find_all('div', class_='r-ent')
            for new_block in news_block:
                try:
                    new_url = new_block.find('a').get('href')
                    new_title = new_block.find('a').text
                    new_time = new_block.find('div', class_='date').text.strip()
                    news_meta.append({'new_url':new_url, 'new_title':new_title, 'new_time':new_time})
                except:
                    pass
            
            page_url = soup.find_all('a', class_='btn wide')[1].get('href')
            page_url = self.forum_domain['ptt'] + page_url
            
            if Round % 5 == 0:
                print("Finish Round:{}".format(Round))
            count += len(news_block)
            Round += 1
       
        if len(news_meta) > limit:
            news_meta = news_meta[:limit]

        return news_meta
    
    def datefilter(self, meta):
        
        current_year = datetime.datetime.now().strftime("%Y")
        new_time_InStr = current_year+"/"+meta['new_time']
        new_time_InDate = datetime.datetime.strptime(new_time_InStr, "%Y/%m/%d").date()
        return new_time_InDate == datetime.datetime.now().date()
        
        
    def GetPTTPageContent(self, section, newsmeta):
        
        news_detail = []
        
        for meta in newsmeta:
            if meta['new_title'].find('[公告]') != -1:
                continue
            
            r = requests.get(self.forum_domain['ptt']+meta['new_url'])
            r.keep_alive = False
            if section == 'Gossiping':
                r = requests.post(r.url, data={'yes':'yes'})
            
            soup = bs(r.text, 'html.parser')
            
            main_content = soup.find('div', {"id":"main-content"})
            removes = main_content.find_all('div', class_='article-metaline')
            removes += main_content.find_all('span', class_='f2')
            removes += main_content.find_all('div', class_='push')
            for tag in removes:
                tag.extract()
            
            new_content = main_content.text
            meta['new_content'] = new_content
            news_detail.append(meta)
            
        return news_detail 
    
    def GetUDNNewsMeta(self, limit):
        
        count = 0
        Round = 0
        news_meta = []
        page_url = self.index_url['udn']
        
        while count <= limit:
            
            if Round == 0:
                r = requests.get(page_url)
                r.keep_alive = False
                soup = bs(r.text, 'html.parser')

                break_news = soup.find('div', {'id':'breaknews_body'})

                removes = []
                removes += break_news.find_all('div', {'id':'ranking_bar'})
                removes += break_news.select('dt.only_mobile')

                for tag in removes:
                    tag.extract()

                news_block = break_news.find_all('dt')
                for new_block in news_block:
                    try:
                        new_title = new_block.find('h2').text
                        new_url = new_block.find_all('a')[0].get('href')
                        new_time = "{0[0]}/{0[1]}".format(new_block.find('div', {'class':'dt'}).text.split()[0].split('-'))
#                         print(new_title, new_url, new_time)
                        news_meta.append({'new_title':new_title, 'new_url':new_url, 'new_time':new_time})
                    except:
                        pass
                
            else:
                r = requests.get(page_url)
                soup = bs(r.text, 'html.parser')
                news_block = soup.find_all('dt', class_="lazyload")
                for new_block in news_block:
                    try:
                        new_title = new_block.find('h2').text
                        new_url = new_block.find_all('a')[0].get('href')
                        new_time = "{0[0]}/{0[1]}".format(new_block.find('div', {'class':'dt'}).text.split()[0].split('-'))
#                         print(new_title, new_url, new_time)
                        news_meta.append({'new_title':new_title, 'new_url':new_url, 'new_time':new_time})
                    except:
                        pass
            
            if Round % 5 == 0:
                print("Finish Round:{} len: {}".format(Round, len(news_meta)))
            count += len(news_block)
            Round += 1
            page_url = self.index_url['udn-lazyupload'].format(Round+1, int(time.time()))
            
        if len(news_meta) > limit:
            news_meta = news_meta[:limit]
        return news_meta
            
    def GetUDNPageContent(self, newsmeta):
        
        newsdetailmeta = []
        for meta in newsmeta:
            r = requests.get(self.forum_domain['udn']+meta['new_url'])
            r.keep_alive = False
            soup = bs(r.text, 'html.parser')
            
            story_body = soup.find('div', {"id":"story_body_content"})
            removes = []
            removes += story_body.find_all('div', {"id":"story_bar"})
            removes += story_body.find_all('div', {"id":"story_bady_info"})
            removes += story_body.find_all('div', class_='only_mobile')
            removes += story_body.find_all('figure, a')
            
            for tag in removes:
                tag.extract()
            meta['new_content'] = story_body.text
            newsdetailmeta.append(meta)
            
        return newsdetailmeta
    
    def GetSETNNewsMeta(self, limit):
        
        count = 0
        Round = 0
        news_meta = []
        page_url = self.index_url['setn'].format(Round+1)
        
        while count <= limit:
            
            r = requests.get(page_url)
            r.keep_alive = False
            soup = bs(r.text, 'html.parser')
            
            newList = soup.find('div', class_='row NewsList')
            news_block = newList.find_all('div', class_='col-sm-12')
            
            for new in news_block:
                
                new_time = "{0[0]}/{0[1]}".format((new.find('time').text.split()[0].split('/')))
                new_title = (new.find('h3').text)
                new_url = new.find('h3').find('a').get('href')
                
                news_meta.append({'new_title':new_title, 'new_url':new_url, 'new_time':new_time})
                
            
            if Round % 5 == 0:
                print("Finish Round:{} len: {}".format(Round, len(news_meta)))
            count += len(news_block)
            Round += 1
            page_url = self.index_url['setn'].format(Round+1)
            
        if len(news_meta) > limit:
            news_meta = news_meta[:limit]
        return news_meta
        
    def GetSETNPageContent(self, newsmeta):
        
        newsdetailmeta = []
        
        for meta in newsmeta:
            
            if meta['new_url'][1] == 'e':
                meta['new_url'] = '/' + meta['new_url'][2:]
            
            r = requests.get(self.forum_domain['setn']+meta['new_url'])
            soup = bs(r.text, 'html.parser')
            
            new_content = soup.find("div", {'id':'Content1'}).text
            meta['new_content'] = new_content
            
            newsdetailmeta.append(meta)
            
        return newsdetailmeta
        
        
    def GetNews(self, forum="ptt", section="WomenTalk", limit=20):
        '''
        This is the main for getting news from all forum
        '''

        if forum == "ptt":
            newsmeta = self.GetPTTNewsMeta(section, limit)        
            newsdetailmeta = self.GetPTTPageContent(section, newsmeta)
        if forum == 'udn':
            newsmeta = self.GetUDNNewsMeta(limit)
            newsdetailmeta = self.GetUDNPageContent(newsmeta)
        if forum == 'setn':
            newsmeta = self.GetSETNNewsMeta(limit)
            newsdetailmeta = self.GetSETNPageContent(newsmeta)
            
        print(newsdetailmeta)
        return newsdetailmeta
            
