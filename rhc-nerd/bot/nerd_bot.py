import os
import time
import telebot
from nerd_module import wikipedia, database, google_translate, iranian_food
import nerd_config




class message_handler:
    '''
        ::message <TeleBot message>
        ::received_time <float> unix time
    '''
    def __init__(self, message, received_time):
        self.message = message
        if message.content_type == 'text': self.command = message.text.lower().strip()
        else: self.command = ''
        self.received_time = received_time
        self.cheat_code      = None
        self.cheat_cat       = None
        self.cheat_input     = None
        self.reserved_answer = None
        self.in_lod_id       = None
        self.in_log()
        self.out_log_done    = False
    
    
    def is_in_blacklist(self):
        result =  database().find('blacklist', {'code':self.command})
        if result.count() > 0: return True
        return False
    
    
    def is_reserved_code(self):
        result = database().find('reserved_code', {'code': self.command})
        if result.count() > 0:
            #convert to list - type of result is <pymongo.cursor.Cursor>
            result = [i for i in result]
            self.reserved_answer = result[0]['answer']
            return True
        return False
        
        
    '''
        Cheat Code: it's a reserved word that command starts with
            * without space, tab, newLine, or other space char
    '''
    def is_cheatcode(self):
        result = database().find('cheatcode', {'cheat-code': self.command}, limit=1)
        if result.count() > 0:
            result = [i for i in result]
            self.cheat_cat   = result[0]['cheat-cat']
            self.cheat_code  = self.command
            self.cheat_input = ''
            return True
        comm = self.command.split()[0].lower()
        result = database().find('cheatcode', {'cheat-code': comm}, limit=1)
        if result.count() > 0:
            #convert to list - type of result is <pymongo.cursor.Cursor>
            result = [i for i in result]
            self.cheat_cat   = result[0]['cheat-cat']
            self.cheat_code  = comm
            self.cheat_input = self.command[len(comm)+1:].strip()
            return True
        return False
        
            
    '''
        Run cheat code
        ::tb <TeleBot> telegram_bot_handler 
        @return
            * 0    No result
            * -1   Error
            * <str> string result or path of image
    '''
    def do_cheat_code(self, tb):
        if self.cheat_cat == 'translator':    return self.cheat_code_translate(tb)
        elif self.cheat_cat == 'find image':  return self.cheat_code_find_image(tb)
        elif self.cheat_cat == 'food':        return self.cheat_code_food(tb)
        elif self.cheat_cat == 'wiki_en':     return self.do_wiki(tb, lang='en')
        else: return (-1, 'Cheat Code: No Function Defined!')
            
    
    def cheat_code_food(self, tb):
        food = iranian_food().suggest()
        if food == 0 or food == None:    return (0, 'Cheat Code: %s' % self.cheat_cat)
        elif food == -1:                 return (-1, 'Cheat Code: %s' % self.cheat_cat)
        #there is a suggestion
        suggest = 'پیشنهاد من یک غذای ایرانی هست به اسم "%s"' % food
        wiki = wikipedia().summary(food)
        if wiki[0]: suggest += "\n\n" + wiki[1]
        tb.send_chat_action(self.message.from_user.id, 'typing')
        tb.reply_to(self.message, suggest)
        return (1, suggest)
    
    
    def cheat_code_translate(self, tb):
        result = google_translate().translate(self.cheat_input)
        if result == -1:
            return (-1, 'Cheat Code: %s' % self.cheat_cat)
        elif result == None:
            return (0, 'Cheat Code: %s' % self.cheat_cat)
        else:
            tb.send_chat_action(self.message.from_user.id, 'typing')
            tb.reply_to(self.message, result)
            return (1, result)
    
    
    def cheat_code_find_image(self, tb):
        result = wikipedia().find_image_binary(self.cheat_input)
        if result[0] == -1:
            return (-1, 'Cheat Code: %s' % str(result[1]))
        elif result[0] == None: return(0, 'Cheat Code: %s' % result[1])
        else:
            try:
                tb.send_chat_action(self.message.from_user.id, 'upload_photo')
                tb.send_photo(self.message.from_user.id, result[1], caption=self.cheat_input)
                result[1].close()
            except:  return (-1, 'Cheat Code: Error in tb.send_photo')
            os.remove(result[1].name) #remove image from system
            img_name = result[1].name[result[1].name.rfind('/')+1:]
            return (1, img_name)
            return(1, result[1].name)
        
        
    '''
        Search in wikipedia
        ::tb <TeleBot> telegram_bot_handler 
        @return
            * 0    No result
            * -1   Error from wikipedia
            * -2   internet Error
            * <str> string result or path of image
    '''
    def do_wiki(self, tb, lang='fa'):
        if self.cheat_cat:  wiki = wikipedia().summary(self.cheat_input, lang=lang)
        else:               wiki = wikipedia().summary(self.command, lang='fa')
        if wiki[0] == 0:             return(0, 'Wiki: %s' % wiki[1])
        elif wiki[0] in {-1, -2}:    return(-1,  'Wiki: %s' % wiki[1])
        else:
            tb.send_chat_action(self.message.from_user.id, 'typing')
            tb.reply_to(self.message, wiki[1])
            return(1, wiki[1])
        return(-1, 'Wiki: UnExpected Error')
        
        
    '''
        Update 'in' type log and return _id for save in 'out' type log and debugging
        @return <mongo _id>
    '''
    def in_log(self):
        user_fname =    self.message.from_user.first_name
        user_lname =    self.message.from_user.last_name
        user_id =       self.message.from_user.id
        user_username = self.message.from_user.username
        log_data = {'type':             'in',
                    'time':             self.received_time,
                    'user-fname':       user_fname,
                    'user-lname':       user_lname,
                    'user-id':          user_id,
                    'user-username':    user_username,
                    'detail':           self.command}
        #print(user_fname, ' [%s] ' % user_id, self.command)
        log_id = database().add_log(log_data)
        self.in_lod_id = log_id
        
        
    def out_log(self, ok_code, detail):
        if detail in {'', None}:         raise('Detail is Empty')
        if type(ok_code) != type(int()): raise('Error in "ok" code')
        log_data = {'type':   'out',
                    'ok':     ok_code,
                    'rel':    self.in_lod_id,
                    'detail': str(detail)}
        database().add_log(log_data)
        self.out_log_done = True


        
        
        
        
        
        
'''
    TeleBot thread run this function After i handle the messages
    ::messages <list> list of new messages
'''
def listener(messages):
    ### Note:received_time must be before of for-loop for calculate response time
    receive_time = time.time()
    ###
    for m in messages:
        message = message_handler(m, receive_time)
        if message.command == '':
            message.out_log(0, 'Empty Command')
        elif message.is_in_blacklist():
            message.out_log(0, 'Black List')
        elif message.is_reserved_code():
            tb.send_chat_action(m.from_user.id, 'typing')
            tb.send_message(m.from_user.id, message.reserved_answer)
            message.out_log(1, message.reserved_answer)
        elif message.is_cheatcode():
            result = message.do_cheat_code(tb)
            message.out_log(result[0],  result[1])
        else:
            result = message.do_wiki(tb)
            message.out_log(result[0],  result[1])
        if not message.out_log_done:
            message.out_log(0, 'Magic Code!')
        

TOKEN = nerd_config.TOKEN
tb = telebot.TeleBot(TOKEN)
tb.set_update_listener(listener) #register listener
tb.polling()

while True: # Don't let the main Thread end.
    pass
