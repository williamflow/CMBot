#!/usr/bin/python3

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
from private import TOKEN
import commands
import traceback
import subprocess
from importlib import reload

class Bot:
    def __init__(self, token):
        self.updater = Updater(token=token)
        self.bot = self.updater.bot
        self.commands = commands.Commands(self.bot)
        self.dispatcher = self.updater.dispatcher
        self.filternull = FilterNull()
        self.dispatcher.add_handler(MessageHandler(self.filternull, self.callback))
        self.updater.start_polling()
        print("Polling")
    
    def callback(self, bot, update):
        try:
            cmd = update.message.text.split(' ')[0].split('@')[0]
            if cmd == "/update":
                self.update(bot, update)
                return
        except:
            traceback.print_exc()
        self.commands.callback(bot, update)
    
    def stop(self):
        self.updater.stop()
            
    def update(self, bot, update):
        print("Update")
        result = subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE).stdout.read()
        print(str(result))
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
