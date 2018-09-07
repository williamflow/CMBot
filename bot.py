#!/usr/bin/python

import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
from random import randint
from tarot import *
from private import TOKEN
import subprocess
import os
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
        self.dispatcher = self.updater.dispatcher
        self.filternull = FilterNull()
        self.dispatcher.add_handler(MessageHandler(self.filternull, self.callback))
        #self.dispatcher.add_handler(CommandHandler('chart', self.chart))
        self.updater.start_polling()
        print "Polling"
    
    def stop(self):
        self.updater.stop()
    
    def callback(self, bot, update):
        try:
            if len(update.message.new_chat_members) > 0:
                self.send(self.getchatid(0, update), "Welcome card!")
                self.card(bot, update)
        except:
            traceback.print_exc()
        try:
            cmd = update.message.text.split(' ')[0].split('@')[0]
            if cmd == "/tarot":
                self.tarot(bot, update)
            elif cmd == "/card":
                self.card(bot, update)
            elif cmd == "/wheel":
                self.wheel(bot, update)
            elif cmd == "/update":
                self.update(bot, update)
        except:
            traceback.print_exc()
    
    def tarot(self, bot, update):
        print "Tarot"
        text = update.message.text.split(' ')
        reply = []
        try:
            if int(text[1]) > 0:
                tot = int(text[1])
        except:
            tot = 1
        for i in range(0, tot):
            n = randint(0, 21)
            reply.append(tarot[n])
        self.reply(update, "```"+"\n".join(reply)+"```")
    
    def card(self, bot, update):
        print "Card"
        try:
            text = update.message.text.split(' ')
            self.replyphoto(update, card[int(text[1])])
        except:
            n = randint(0, 21)
            self.replyphoto(update, card[n])
            
    def wheel(self, bot, update):
        print "Wheel"
        # dd mm yyyy hh mm ss
        text = update.message.text.split(' ')
        try:
            name = str(randint(0,9999))
            self.sendtyping(update)
            result = subprocess.Popen("curl http://planetwatcher.com/chartwheel.php?date="+str(int(text[3]))+"-"+str(int(text[2]))+"-"+str(int(text[1]))+"%20"+str(int(text[4]))+":"+str(int(text[5]))+":"+str(int(text[6]))+"%20UTC -o "+name, shell=True, stdout=subprocess.PIPE).stdout.read()
            self.replyphoto(update, name)
            subprocess.Popen("rm "+name, shell=True)
        except:
            traceback.print_exc()
            
    def update(self, bot, update):
         result = subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()
         self.reply(update, result)
         subprocess.Popen("sudo service cmbot restart", shell=True)
            
    def chart(self, bot, update):
        print "Chart"
        #name dd mm yyy hh mm city
        text = update.message.text.split(' ')
        while self.driveravaible is False:
            pass
        self.driveravaible = False
        self.sendtyping(update)
        try:
            self.driver.get('https://www.astrotheme.com/horoscope_chart_sign_ascendant.php')
            element = self.driver.find_element_by_name("prenom")
            location = element.location
            self.driver.execute_script("window.scrollTo(0, %s);" % location["y"])
            element.send_keys(text[1])
            self.sendtoelement("date[d][d]", text[2])
            self.sendtoelement("date[F][F]", text[3])
            self.driver.execute_script("document.getElementsByName('date[Y]')[0].setAttribute('value', '"+text[4]+"')")
            self.sendtoelement("heure[H]", text[5])
            self.sendtoelement("heure[i]", text[6])
            try:
                cookie = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "fermeture_cookie"))
                )
                cookie.click()
            except:
                pass
            self.sendtoelement("ville", " ".join(text[7:]))
            self.clickelement(By.CLASS_NAME, "ui-menu-item")
            #ui = self.driver.find_element_by_class_name("ui-menu-item")
            self.clickelement(By.NAME, "_qf_s1_next")
            self.clickelement(By.NAME, "_qf_s2_next")
            #text = self.driver.execute_script("return document.getElementsByTagName('h2')[0].innerHTML") + "\n" + self.driver.execute_script("return document.getElementsByTagName('h2')[1].innerHTML")
            #self.reply(update, text)
            #self.driver.quit()
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "svg"))
            )
            location = element.location
            self.driver.execute_script("window.scrollTo(0, %s);" % location["y"])
            size = element.size
            png = self.driver.get_screenshot_as_png()
            self.driver.quit()
            im = Image.open(BytesIO(png))
            left = location['x']
            top = 0
            right = location['x'] + size['width']
            bottom = size['height']
            im = im.crop((left, top, right, bottom)) # defines crop points
            name = str(randint(0,9999))+".png"
            im.save(name)
            self.replyphoto(update, name)
        except:
            traceback.print_exc()
        subprocess.Popen("rm "+name, shell=True)
        self.driveravaible = True
        
    def send(self, chat, text):
        return self.bot.send_message(chat, text, parse_mode="markdown")
    
    def sendtyping(self, update):
        return self.bot.send_chat_action(chat_id=self.getchatid(0, update), action=telegram.ChatAction.TYPING)
        
    def reply(self, update, text):
        return update.message.reply_text(text, parse_mode="markdown")
        
    def sendphoto(self, chat, filename):
        return self.bot.send_photo(chat_id=chat, photo=open(filename, 'rb'))
    
    def sendphotourl(self, chat, url):
        return self.bot.send_photo(chatid=chat, photo=url)
        
    def replyphoto(self, update, filename):
        return self.bot.send_photo(self.getchatid(0, update), photo=open(filename, 'rb'))
        
    def getchatid(self, bot, update):
        return update.message.chat_id
    
    def sendtoelement(self, name, keys):
        element = self.driver.find_element_by_name(str(name))
        element.send_keys(str(keys))
            
    def clickelement(self, by, name):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, name))
        )
        element.click()

class FilterNull(BaseFilter):
    def filter(self, message):
        return True

if __name__ == "__main__":
    bot = Bot(TOKEN)
    x = raw_input()
    print "Stopping Bot..."
    bot.stop()
