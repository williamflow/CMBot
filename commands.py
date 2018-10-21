from random import randint
import subprocess
import os
import traceback
import telegram
from tarot import *
import re

class Commands:
    def __init__(self, bot):
        self.bot = bot
        
    def callback(self, bot, update):
        try:
            cmd = update.message.text.split(' ')[0].split('@')[0]
            if cmd == "/card":
                self.card(bot, update)
        except:
            traceback.print_exc()
        self.youtube(bot, update)
            
    def card(self, bot, update):
        print("Card")
        #print update.message
        n = randint(0, 155)
        self.sendtyping(update)
        self.replyphoto(update, "deck/"+str(n)+".jpg")
         
    def youtube(self, bot, update):
        matchObj = re.match( r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?', update.message.text, re.M|re.I)
        if matchObj:
            try:
                subprocess.Popen('youtube-dl -f bestaudio --extract-audio --embed-thumbnail --add-metadata --output "%(title)s.%(ext).s" "' + matchObj.group() + '"', shell=True)
                title = subprocess.Popen('youtube-dl -f bestaudio --extract-audio --embed-thumbnail --add-metadata --output "%(title)s.%(ext).s" --get-filename "' + matchObj.group() + '"', shell=True, stdout=subprocess.PIPE).stdout.read()
                self.sendaudio(update, title)
                subprocess.Popen('rm "' + title + '"', shell=True)
            except:
                traceback.print_exc()
    
    def send(self, chat, text):
        return self.bot.send_message(chat, text, parse_mode="markdown")
    
    def sendtyping(self, update):
        return self.bot.send_chat_action(chat_id=self.getchatid(0, update), action=telegram.ChatAction.TYPING)
        
    def reply(self, update, text):
        self.send(self.getchatid(0, update), text)
        #return update.message.reply_text(text, parse_mode="markdown")
        
    def sendphoto(self, chat, filename):
        #self.bot.send_photo(chatid=chat, photo="https://beyondthestarsastrology.files.wordpress.com/2013/12/smaug.jpg")
        return self.bot.send_photo(chat_id=chat, photo=open(filename, 'rb'))
    
    def sendaudio(self, update, filename):
        return self.bot.send_audio(chat_id=self.getchatid(update), audio=open(filename, 'rb'))
    
    def sendphotourl(self, chat, url):
        return self.bot.send_photo(chatid=chat, photo=url)
        
    def replyphoto(self, update, filename):
        self.sendphoto(self.getchatid(0,update), filename)
        #return update.message.reply_photo(photo=open(filename, 'rb'))
        #return self.bot.send_photo(self.getchatid(0, update), photo=open(filename, 'rb'))
        
    def getchatid(self, bot, update):
        return int(update.message.chat.id)

