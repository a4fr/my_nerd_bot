# -*- coding: utf-8 -*-

from flask import Flask, request
import logging
import telebot
import nerd_config
import nerd_bot

app = Flask(__name__)
app.config['DEBUG'] = True
tb = telebot.TeleBot(nerd_config.TOKEN, create_threads=False)




def listener(messages):
    nerd_bot.listener(messages, tb)



@app.route('/webhook', methods=['GET', 'POST'])
def webhook2():
    request_json = request.get_json()
    if request_json:
        logging.info('in_log:')
        logging.info(request_json['message'])
        tb.update_listener = [listener]
        new_message = telebot.types.Message.de_json(request_json['message'])
        
        tb.process_new_messages([new_message])
        return '1'
    return '0'

    
    