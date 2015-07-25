#! /usr/bin/python3
#from bottle import Bottle, run
from flask import Flask
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo
import time



import os
db_host = os.environ['OPENSHIFT_MONGODB_DB_HOST']
db_port   = os.environ['OPENSHIFT_MONGODB_DB_PORT']
database = MongoClient('mongodb://USERNAME:PASWWORD@%s:%s/' % (db_host, db_port)).nerd_bot



template_ajax = ''
template_no_ajax = ''
path = '/var/lib/openshift/55a8d90c4382ec526b00003b/app-root/repo/'
file = open(path+'templates/report_ajax.template', 'r')
template_ajax = file.read()
file.close()
file = open(path+'templates/report_no_ajax.template', 'r')
template_no_ajax = file.read()
file.close()


class long_in_out_report:
    def __init__(self):
        self.db = database
        
    '''
        Create a full table of last 1 hour logs
        ::title      Title of html page
        ::detail     Detail of table. shows in log report page
        ::limit_hour <float> Find last hour logs 
    '''
    def create_html(self,title, detail, limit_hour=1):
        rows = ''
        
        # convert last time to unix time
        day_limited = datetime.now() - timedelta(hours=limit_hour)
        time1 = time.mktime(day_limited.timetuple()) # last posible time
        logs = self.db.log.find({'type': 'in', 'time': {'$gt': time1}}).sort('time', pymongo.DESCENDING)
        
        for msg_in in logs:
            time_in = datetime.fromtimestamp(msg_in['time']).strftime('%Y-%m-%d %H:%M:%S')
            msg_out = self.db.log.find_one({'type':'out', 'rel': ObjectId(msg_in['_id'])})
            
            if msg_out == None:
                msg_out = dict()
                msg_out['ok'] = -10
                msg_out['detail'] = 'پروسه یا به تازگی ساخته شده و یا اینکه بخاطر یک خطای کنترل نشده terminate شده‌است.'
            
            user_name = msg_in['user-fname']
            if 'user-lname' in msg_in and msg_in['user-lname'] != None: user_name += ' %s' % msg_in['user-lname']
            
            out_stat = 'خروجی'
            if msg_out['ok'] == 1:
                out_tag = 'good'
                out_stat = 'خروجی'
                time_out = int(msg_out['time'] - msg_in['time'])
                time_out = 'بعد از %s ثانیه' % time_out
            elif msg_out['ok'] == 0:
                out_stat = 'بدون خروجی'
                out_tag = 'nothing'
                time_out = int(msg_out['time'] - msg_in['time'])
                time_out = 'بعد از %s ثانیه' % time_out
            elif msg_out['ok'] == -1:
                out_stat = 'بدون خروجی (بخاطر خطا)'
                out_tag = 'error'
                time_out = int(msg_out['time'] - msg_in['time'])
                time_out = 'بعد از %s ثانیه' % time_out
            elif msg_out['ok'] == -10:
                out_stat = 'مشخص نیست'
                out_tag = 'risk'
                time_out = '-'
                
            tr = '<td class=%s>%s</td>\n'
            tmp = '<tr>\n'
            tmp += tr % ('normal id=time', time_in)
            tmp += tr % ('normal', user_name)
            tmp += tr % ('normal', msg_in['user-id'])
            tmp += tr % ('notice', msg_in['detail'])
            tmp += tr % (out_tag, out_stat)
            tmp += tr % ('normal id=delay', time_out)
            tmp += tr % ('notice', msg_out['detail'])
            tmp += '</tr>\n'
            rows += tmp
        th = '''<th>زمان</th>
                <th>نام کاربر</th>
                <th>شناسه کاربر</th>
                <th>درخواست</th>
                <th>وضعیت خروجی</th>
                <th>فاصله درخواست تا پاسخ</th>
                <th>پاسخ</th>'''
        template = template_no_ajax
        template = template.replace('{{title}}', title)
        template = template.replace('{{detail}}', '%s<br/>%s'% (detail , datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        template = template.replace('{{th}}', th)
        template = template.replace('{{rows}}', rows)
        return template
        

class reserved_code:
    def __init__(self):
        self.db = database
    
    '''
        create a table of reserved code/answer
    '''
    def create_html(self, title, detail):
        codes = self.db.reserved_code.find().sort('code', pymongo.ASCENDING)

        
        rows = ''
        for code in codes:
            tmp = '<tr>\n'
            td = '<td class=%s>%s</td>\n'
            tmp += td % ('normal', code['code'])
            tmp += td % ('normal', code['answer'])
            tmp += '</tr>'
            rows += "\n %s" % tmp
        th = """<th>کد</th>
                <th>پاسخ</th>"""
        template = template_no_ajax
        template = template.replace('{{title}}', title)
        template = template.replace('{{detail}}', detail)
        template = template.replace('{{th}}', th)
        template = template.replace('{{rows}}', rows)
        return template        
        

class cheatcodes:
    def __init__(self):
        self.db = database
    
    '''
        create a table of ceatcodes
        ::category <str>
            * '' for show all cheat code categories
    '''
    def create_html(self, title, detail, categoty=''):
        if categoty == '' :  cheatcodes = self.db.cheatcode.find().sort('cheat-cat', pymongo.ASCENDING)
        else: cheatcodes = self.db.cheatcode.find({'cheat-cat': str(categoty)}).sort('cheat-cat', pymongo.DESCENDING)
        
        
        rows = ''
        for cheatcode in cheatcodes:
            tmp = '<tr>\n'
            td = '<td class=%s>%s</td>\n'
            tmp += td % ('normal', cheatcode['cheat-cat'])
            tmp += td % ('normal', cheatcode['cheat-code'])
            tmp += '</tr>'
            rows += "\n %s" % tmp
        th = """<th>دسته</th>
                <th>کد تقلب</th>"""
        template = template_no_ajax
        template = template.replace('{{title}}', title)
        template = template.replace('{{detail}}', detail)
        template = template.replace('{{th}}', th)
        template = template.replace('{{rows}}', rows)
        return template    


class blacklist:
    def __init__(self):
        self.db = database
    
    '''
        create a table of reserved code/answer
    '''
    def create_html(self, title, detail):
        codes = self.db.blacklist.find().sort('code', pymongo.ASCENDING)

        
        rows = ''
        for code in codes:
            tmp = '<tr>\n'
            td = '<td class=%s>%s</td>\n'
            tmp += td % ('normal', code['code'])
            tmp += '</tr>'
            rows += "\n %s" % tmp
        th = """<th>عبارت</th>"""
        template = template_no_ajax
        template = template.replace('{{title}}', title)
        template = template.replace('{{detail}}', detail)
        template = template.replace('{{th}}', th)
        template = template.replace('{{rows}}', rows)
        return template      
        

#app = Bottle()
app = Flask(__name__)

@app.route('/report/log')
def report_log():
    url = 'http://localhost:8080/report/log'
    limit_hour = 8
    title = 'گزارش ورودی/خروجی ربات'
    detail = 'گزارش %s ساعت گذشته ربات' % limit_hour
    report_1 = long_in_out_report().create_html(title, detail, limit_hour)
    return report_1.replace('{{url}}', url)

@app.route('/report/reserved_code')
def report_reserved_code():
    url = 'http://localhost:8080/report/reserved_code'
    title = 'درخواست و جواب های آماده ربات'
    detail = 'جدول درخواست و جواب های آماده ربات'
    report = reserved_code().create_html(title, detail)
    return report.replace('{{url}}', url)


@app.route('/report/cheatcode')
def report_cheatcode():
    url = 'http://localhost:8080/report/cheatcode'
    title = 'کد‌های تقلب'
    detail = 'جدول کدهای تقلب ربات'
    report = cheatcodes().create_html(title, detail)
    return report.replace('{{url}}', url)


@app.route('/report/blacklist')
def report_blacklist():
    url = 'http://localhost:8080/report/blacklist'
    title = 'لیست عبارات ممنوع'
    detail = 'لیست سیاه'
    report = blacklist().create_html(title, detail)
    return report.replace('{{url}}', url)


#run(app, host='localhost', port=8080, reloader=True, debug=True)
app.debug = True
if __name__ == "__main__":
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    host_name = os.environ['OPENSHIFT_GEAR_DNS']

    app.run(host_name, port=int(port))
       
