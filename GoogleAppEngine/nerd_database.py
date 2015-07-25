# -*- coding: utf-8 -*-

class cheatcode:
    def __init__(self):
        self.db = {u'food':      {u'گشنمه', u'گرسنمه', u'غذا', u'غذای ایرانی', u'غذا ی ایرانی'},
                   u'wiki_en':   {u'w', u'wiki', u'wiki_en'}}
    def find(self, word):
        for cheat_cat in self.db:
            if word in self.db[cheat_cat]:
                return cheat_cat
        return None
    
class reserved_code:
    def __init__(self):
        self.db = {u'/start':           u'سلام میتونی من رو امتحان کنی. واسه شروع یه کلمه واسم بفرست تا خیلی کوتاه درموردش واست توضیح بدم :)',
                   u'/help':            u'سلام میتونی من رو امتحان کنی. واسه شروع یه کلمه واسم بفرست تا خیلی کوتاه درموردش واست توضیح بدم :)',
                   
                   u'a4fr':             u'علی نجفی بابای این ربات :))',
                   u'علی نجفی':         u'علی نجفی بابای این ربات :))',
                   u'ali najafi':       u'علی نجفی بابای این ربات :))',
                   u'سلام':             u'سلام :)',
                   u'کمک':              u'سلام میتونی من رو امتحان کنی. واسه شروع یه کلمه واسم بفرست تا خیلی کوتاه درموردش واست توضیح بدم :)',
                   u'ممنون':            u'خواهش میکنم :)',
                   u'خوبی':            u'ممنون :)',
                   u'خوبی؟':            u'ممنون :)',
                   u'خوبی ؟':         u'ممنون :)',
                   u'خوبی؟؟':        u'ممنون :)',
                   u'خوبی ؟؟':        u'ممنون :)',
                   u'خدافظ':         u'خدا نگهدار :)',
                   u'خدا فظ':         u'خدا نگهدار :)',
                   u'خداحافظ':      u'خدا نگهدار :)',
                   u'خدا حافظ':     u'خدا نگهدار :)'}
    def find(self, word):
        if word in self.db:
            return self.db[word]
        return None

class blacklist:
    def __init__(self):
        self.db = {u'گوزو'}
    def find(self, word):
        if word in self.db:
            return word
        return None
      
class iranian_foods:
    def __init__(self):
        self.db = [u"آلبالوپلو", u"استانبولی", u"باقلاپلو", u"پلو زعفرانی", u"پتله پلو", u"ته‌چین", u"چلو", u"چلو کره", u"دمپختک", u"رشته‌پلو", u"زرشک‌پلو", u"سبزی‌پلو", u"شویدباقلا", u"شیرین‌پلو", u"عدس‌پلو", u"قابلی", u"قیمه‌نثار", u"کته", u"کلم‌پلو", u"دمپختک باقلا", u"لوبیاپلو", u"ماش‌پلو", u"مرصع‌پلو", u"نخودپلو", u"هویج‌پلو", u"والک‌پلو", u"ته دیگ", u"آذربایجان", u"بامیه", u"به با آلو", u"چشم‌بلبلی", u"چغاله بادام", u"دال عدس", u"ریواس", u"فسنجان", u"قلیه‌ماهی", u"قلیه‌میگو", u"قورمه‌سبزی", u"قیمه", u"بادمجان", u"قیمه بادمجان", u"قیمه بوشهری", u"قیمه گیلان", u"قیمه‌نثار", u"قیمه یزد", u"کدوبادمجان", u"کرفس", u"کنگر", u"گوجه سبز", u"لوبیا سفید", u"ماست", u"مرغ ترش", u"مسمای مرغ", u"هویج", u"خلال بادام", u"اکبر جوجه", u"بختیاری", u"برگ", u"نان و کباب", u"بره درسته", u"بلغاری", u"بناب‌کباب", u"تابه‌ای", u"جوجه‌کباب", u"چنجه", u"شیشلیک", u"کوبیده", u"شامی کباب", u"آب‌گوشت", u"آب‌دوغ خیار", u"انواع آش", u"اشکنه", u"چغور پغور", u"دیزی", u"سیرابی شیردان", u"کله‌پاچه", u"شامی", u"شله مشهدی", u"شیربرنج", u"عدسی", u"انواع کوفته", u"تاس‌کباب", u"آب پیازک", u"اشپل", u"باسترما", u"باقلاقاتوق", u"بریانی اسفناج", u"ترشی‌تره", u"ترخینه", u"دلمه", u"حلیم بادمجان", u"حلیم بوقلمون", u"دوپیازه آلو", u"خاگینه", u"دلمه", u"سمبوسه", u"فلافل", u"کاچی", u"کاله‌جوش", u"کتلت", u"کشک بادنجان", u"کوکو", u"گیپا", u"لونگی", u"میرزاقاسمی", u"نازخاتون", u"نرگسی", u"لواش", u"سنگک", u"بربری", u"تافتون", u"ساجی", u"قرابیه", u"سوجوق", u"باسلوق", u"رشته‌ختایی", u"نوقا", u"اریس", u"میرزاقاسمی", u"ترش تره", u"باقلاقاتوق", u"ماهی فویج", u"فسنجان", u"اناربیج", u"کولی غورابیج", u"سیر قلیه", u"گل در چمن", u"کال کباب", u"مرغ ترش", u"اناربیج", u"مرغ لاکو", u"فسنجان", u"میرزا قاسمی", u"ترش تره", u"سیرقلیه", u"باقلاقاتوق", u"سیرابیج", u"نازخاتون", u"لونگی", u"کولی غورابیج", u"واویشکا", u"شامی", u"آش سبزی", u"آش ماست", u"آش دوغ", u"آب پیازک", u"پاچه پلو", u"قنبرپلو", u"رنگینک", u"سالاد شيرازي", u"دوپیازه", u"یخنی نخود", u"رب پلو", u"کلم پلو", u"بادام سوخته", u"یخنی عدس کلم", u"شکر پنیر", u"شامی", u"کوفته هلو", u"کوفته سبزی", u"حلوای کاسه", u"حلیم بادمجان", u"حاجی بادام", u"دوای آرد و روغن", u"شکر پلو", u"آش انار"]
    
    def suggest(self):
        import random
        rand = random.randint(1, len(self.db)-1)
        return  self.db[rand]
