#!/usr/bin/python3

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
from tarot import *
from private import TOKEN
import commands
import traceback
#from pyvirtualdisplay import Display
#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from PIL import Image
#from cStringIO import StringIO
#from io import BytesIO

class Bot:
    def __init__(self, token):
        self.updater = Updater(token=token)
        #options = Options()
        #options.add_argument("--headless")
        #self.driver = webdriver.Firefox(firefox_options=options)
        #self.display = Display(visible=0, size=(1024, 768))
        #self.display.start()
        #options = Options()
        #options.add_argument("--headless")
        #self.driver = webdriver.Firefox(firefox_options=options)
        #self.driveravaible = True
        self.bot = self.updater.bot
        self.commands = commands.Commands(self.bot)
        self.dispatcher = self.updater.dispatcher
        self.filternull = FilterNull()
        self.dispatcher.add_handler(MessageHandler(self.filternull, self.callback))
        #self.dispatcher.add_handler(CommandHandler('chart', self.chart))
        self.updater.start_polling()
        print("Polling")
    
    def stop(self):
        self.updater.stop()
    
    def callback(self, bot, update):
        try:
            if len(update.message.new_chat_members) > 0:
                commands.send(commands.getchatid(0, update), "Welcome card!")
                commands.card(bot, update)
        except:
            traceback.print_exc()
        try:
            cmd = update.message.text.split(' ')[0].split('@')[0]
            if cmd == "/tarot":
                commands.tarot(bot, update)
            elif cmd == "/card":
                commands.card(bot, update)
            elif cmd == "/wheel":
                commands.wheel(bot, update)
            elif cmd == "/update":
                self.update(bot, update)
            elif cmd == "/help":
                commands.helpa(bot, update)
        except:
            traceback.print_exc()
            
     def update( bot, update):
        print("Update")
        result = subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()
        reply(update, result)
        reload(commands)
        self.commands = commands.Commands(self.bot)


class FilterNull(BaseFilter):
    def filter(self, message):
        return True

if __name__ == "__main__":
    bot = Bot(TOKEN)
    x = input()
    print("Stopping Bot...")
    bot.stop()
