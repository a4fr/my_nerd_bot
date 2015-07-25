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
        return(0, u'There is no Page')
    
        
        
'''
    Suggest an Iranian food
    @return
        * <str> name of food
        * -1    for Error
'''
class iranian_food:
    def suggest(self):
        return nerd_database.iranian_foods().suggest()



        
    
