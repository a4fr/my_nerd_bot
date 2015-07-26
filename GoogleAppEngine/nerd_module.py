# -*- coding: utf-8 -*-
import os
import time
import json
import random
import nerd_config
import nerd_database
from cgitb import text
import wikipedia as wkp
import requests.exceptions
from bs4 import BeautifulSoup


## for python 2.7
import urllib
import urllib2
from urlparse import urlparse
##




'''
    Prepare a description for a word
        * length of summary is about 300 char
        * an image in png, jpg or gif format
'''
class wikipedia:
    def __init__(self):
        self.word = None
        self.img_black_list = {u'Commons-logo.svg',
                              u'System-installer.svg',
                              u'Wiki letter w cropped.svg'}
        
        
    '''
        ::return
            * Text <str>
            *  0    For nothing result
            * -1    There is an Error in wikimedia server
            * -2    requests.exceptions.ConnectionError    Connection error in request module
    '''
    def summary(self, word, lang=u'fa'):
        word = word.strip()
        if word in {u'', None}:
            return(0, u'Word is empty')
        
        wiki = wkp
        wiki.set_lang(lang)
        try: 
            #page = wiki.page(result)
            #page = wiki.page(word)
            page = wiki.page(word, auto_suggest=False)
            #load the suggested page
            s = page.summary
            s = s.strip()
            pos = s.find(u'\n\n')
            if pos != -1 and pos <=100 : # 100 for trust 
                s = s[pos+2:]
                pos = 0
            pos1 = s[:301].rfind(".")
            pos2 = s[300:].find(".")
            if 300-pos1 < pos2:
                pos = pos1
            else:
                pos = 300+pos2
            s = s[:pos+1] #ended with "."
            return(1, s.strip())
        except wkp.exceptions.DisambiguationError as e:
            # Return a random exist Disambiguation
            random.shuffle(e.options)   #shuffle may_refer list for create new result in every same query
            for suggest in e.options:
                try:
                    page = wiki.page(suggest)
                    text = u'در مورد "%s" مطلب خاصی واسه گفتن ندارم ولی "%s" رو پیشنهاد میکنم:\n' % (word, suggest)
                    text += page.summary
                    return(1, text)
                except: continue
            return(0, u'There is no Page')
        except wkp.exceptions.PageError as e:             return(0, u'Page Error')
        except wkp.exceptions.WikipediaException as e:    return(-1, u'Wikipedia Server Error') 
        except requests.exceptions.ConnectionError as e:  return(-2, u'Connection Error')
        except:                                           return(0, u'There is no Page')
    
    '''
        find image of wikipedia page
        ::return
            * URL string, None(for nothing result)
            * None for nothing result
    '''
    def find_image(self, word):
        lang = 'fa'
        word = urllib.quote(word)
        url = u'http://%s.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles=%s' % (lang, word)
        try:
            result =  urllib2.urlopen(url).read()
            if len(result) > 0:
                result = result.decode('utf8')
            else:
                return(-1, u'Error in read from %s' % url)
        except: return(-1, u'Error in wikipedia server: %s' % url)
        result = json.loads(result)
        
        id = list(result['query']['pages'].keys())
        for i in id:
            if i=='-1': return(None, 'No image')
        if len(id) > 0:
            if 'images' not in result['query']['pages'][id[0]]: return(None, 'No image')
            images = result['query']['pages'][id[0]]['images']
            images_tmp = []
            for num in range(len(images)):
                images[num] =  images[num]['title']
                pos = images[num].find(':')
                if images[num][pos+1:] not in self.img_black_list:
                    images_tmp.append(images[num][pos+1:].replace(' ', '_'))
        else: return(None, 'No image')
        if len(images) == 0 : return(None, 'No image')
        else:
            rand = random.randint(0, len(images_tmp)-1)
            return(1, images_tmp[rand])
        
    '''
        ::return 
            * _IO class
            * None
            * -1
    '''
    def find_image_binary(self, word):
        if word == "": return(-1, 'Word is empty')
        result = self.find_image(word)
        if result[0] == None: return(None, str(result[1]))
        elif result[0] == -1: return(-1, str(result[1]))
        
        if not os.path.exists(nerd_config.find_img_path): os.makedirs(nerd_config.find_img_path) # create directories with their parents
        name = urllib.quote(result[1])
        url = u'http://commons.wikimedia.org/wiki/File:%s' % (name)
        try:
            html =  urllib2.urlopen(url).read()
            if len(html)>0:
                html = html.decode('utf8')
            else: return (-1, u'find_image_binary/urllib/read/%s' % url)
        except:   return (-1, u'find_image_binary/urllib/read/%s' % url)
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find('div', id='file')
        if tag != None:
            tag = tag.find('img')
        if tag != None:
            img_src = tag.get('src')
        else:   return (-1, u'find_image_binary/BeautifulSoup/Find image %s' % url)
        try:    img_bin = urllib2.urlopen(img_src).read()
        except: return(-1, 'Error in download image')

        file = open(u'images/%s' % name, 'wb')
        file.write(img_bin)
        file.close()
        return (1, open(u'images/%s' % name, 'rb'))
        #return(1, io.BytesIO(img_bin))
        

'''
    Abstract layer for MongoDB 2.4.x and 3.x
'''
class database:
    def __init__(self):
        self.db = nerd_config.mongo_db    # default database name is nerd_bot
    
    
    '''
        add a log to database
        ::data <dict>
            * type: "in" or "out"
              time: <unix time>
              user-fname
              user-id
              detail
              *rel <mongodb _id> make a relationship link with 'in' type log
              *ok  <int> 1,0,-1  (if sent result to user), (No result), (Error)
              <* for 'out' type>
        @return _id <ObjectId(inserted_id)>
    '''
    def add_log(self, data):
        if 'time' not in data:                      data['time'] = time.time()
        if data['type'] not in {'in', 'out'}:       raise Exception('Error in data["type"]')
        if data['type']=='out' and data['rel']=='': raise Exception('data["rel"] is empty')
        
        if nerd_config.mongo_version == 3:
            return self.db.log.insert_one(data).inserted_id
        elif nerd_config.mongo_version == 2:
            return self.db.log.insert(data)
    
    
    '''
        add a data to database for use in future
            * upsert is False so if you run add_knowledge many time
              no data removed or replace in data base
        ::data <dict>
        @return <mongodb _id> inserted_id
    '''
    def add_knowledge(self, data):
        if len(data) == 0 : raise Exception('Data is empty')
    
        if nerd_config.mongo_version == 3:
            return self.db.knowledge.insert_one(data).inserted_id
        elif nerd_config.mongo_version == 2:
            return self.db.knowledge.insert(data)
    
    
    '''
        add a cheat code to database
        ::data <dict>
            * cheat-code <str> string of cheat code
              cheat-cat  <str> cheat code category
        @return True/False
    '''
    def add_cheat_code(self, data):
        for key in {'cheat-code', 'cheat-cat'}:
            if key not in data:           raise Exception(u'%s not in data' % key)
            elif data[key] in {'', None}: raise Exception(u'Error in data[%s]' % key)
        
        if nerd_config.mongo_version == 3:
            self.db.cheatcode.replace_one({'cheat-code': data['cheat-code']}, data, upsert=True)
            return True
        elif nerd_config.mongo_version == 2:
            self.db.cheatcode.update({'cheat-code': data['cheat-code']}, {'$set': data}, upsert=True)
            return True
    
    
    '''
        add to blacklist to database
        ::data <dict>
            * code <str> string of blacklist code
        @return True/False
    '''
    def add_blacklist(self, data):
        for key in {'code'}:
            if key not in data:           raise Exception(u'%s not in data' % key)
            elif data[key] in {'', None}: raise Exception(u'Error in data[%s]' % key)
    
        if nerd_config.mongo_version == 3:
            self.db.blacklist.replace_one({'code': data['code']}, data, upsert=True)
            return True
        elif nerd_config.mongo_version == 2:
            self.db.blacklist.update({'code': data['code']}, data, upsert=True)
            return True

    '''
        add a reserved code to database
        ::data <dict>
            * code <str> string of blacklist code
            * answer <str> 
        @return True/False
    '''
    def add_reserved_code(self, data):
        for key in {'code', 'answer'}:
            if key not in data:           raise Exception(u'%s not in data' % key)
            elif data[key] in {'', None}: raise Exception(u'Error in data[%s]' % key)

        if nerd_config.mongo_version == 3:
            self.db.reserved_code.replace_one({'code': data['code']}, data, upsert=True)
            return True
        elif nerd_config.mongo_version == 2:
            self.db.reserved_code.update({'code': data['code']}, data, upsert=True)
            return True
    
    
    '''
        Delete data from database
        ::query <dict>
        ::type <str>
            * can be 'log', 'cheatcode', 'reserved_code', blacklist
            * this is for select database collection
        ::just_one <bool>
        @return True/False
    '''
    def remove(self, collection, query, just_one=True):
        if type == '': raise Exception('type is empty')
        
        
    
        if nerd_config.mongo_version == 3:
            if just_one == 1:  self.db[collection].delete_one(query)
            elif just_one > 1: self.db[collection].delete_many(query)
            return True
        elif nerd_config.mongo_version == 2:
            if just_one == 1:  self.db[collection].remove(query, 1)
            elif just_one > 1: self.db[collection].remove(query)
            return True
    
    '''
        Find and return a log or knowledge
        ::type 'log', 'reserved_code', 'cheatcode', blacklist
        ::qurey <dict> query for find log or knowledge
        ::limit <int>
            * max number of find result
            * 0 for no limit
        @return <pymongo.cursor.Cursor>
            * use in "for r in @return:"
            * @return.count() <int> number of results
    '''
    def find(self, collection, query, limit=1):
        if type == '': raise Exception('Collection is empty')
        
        if nerd_config.mongo_version in {3, 2}:
            if limit > 0 :   return self.db[collection].find(query, limit=limit)
            elif limit == 0: return self.db[collection].find(query)


        
    