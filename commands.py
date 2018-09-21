from random import randint
import subprocess
import os
import traceback
import telegram
from tarot import *

def helpa(bot, update):
    send(getchatid(0, update), "NO ONE IS GOING TO SAVE US!")
    send(getchatid(0, update), "LEAVE ALL HOPES BEHIND")

def tarot( bot, update):
    print("Tarot")
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
    reply(update, "```"+"\n".join(reply)+"```")

def card( bot, update):
    print("Card")
    #print update.message
    try:
        text = update.message.text.split(' ')
        replyphoto(update, card[int(text[1])])
    except:
        n = randint(0, 21)
        replyphoto(update, card[int(n)])
        
def wheel( bot, update):
    print("Wheel")
    # dd mm yyyy hh mm ss
    text = update.message.text.split(' ')
    try:
        name = str(randint(0,9999))
        sendtyping(update)
        result = subprocess.Popen("curl http://planetwatcher.com/chartwheel.php?date="+str(int(text[3]))+"-"+str(int(text[2]))+"-"+str(int(text[1]))+"%20"+str(int(text[4]))+":"+str(int(text[5]))+":"+str(int(text[6]))+"%20UTC -o "+name, shell=True, stdout=subprocess.PIPE).stdout.read()
        replyphoto(update, name)
        subprocess.Popen("rm "+name, shell=True)
    except:
        traceback.print_exc()
        
def chart( bot, update):
    print("Chart")
    #name dd mm yyy hh mm city
    text = update.message.text.split(' ')
    while driveravaible is False:
        pass
    driveravaible = False
    sendtyping(update)
    try:
        driver.get('https://www.astrotheme.com/horoscope_chart_sign_ascendant.php')
        element = driver.find_element_by_name("prenom")
        location = element.location
        driver.execute_script("window.scrollTo(0, %s);" % location["y"])
        element.send_keys(text[1])
        sendtoelement("date[d][d]", text[2])
        sendtoelement("date[F][F]", text[3])
        driver.execute_script("document.getElementsByName('date[Y]')[0].setAttribute('value', '"+text[4]+"')")
        sendtoelement("heure[H]", text[5])
        sendtoelement("heure[i]", text[6])
        try:
            cookie = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fermeture_cookie"))
            )
            cookie.click()
        except:
            pass
        sendtoelement("ville", " ".join(text[7:]))
        clickelement(By.CLASS_NAME, "ui-menu-item")
        #ui = driver.find_element_by_class_name("ui-menu-item")
        clickelement(By.NAME, "_qf_s1_next")
        clickelement(By.NAME, "_qf_s2_next")
        #text = driver.execute_script("return document.getElementsByTagName('h2')[0].innerHTML") + "\n" + driver.execute_script("return document.getElementsByTagName('h2')[1].innerHTML")
        #reply(update, text)
        #driver.quit()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "svg"))
        )
        location = element.location
        driver.execute_script("window.scrollTo(0, %s);" % location["y"])
        size = element.size
        png = driver.get_screenshot_as_png()
        driver.quit()
        im = Image.open(BytesIO(png))
        left = location['x']
        top = 0
        right = location['x'] + size['width']
        bottom = size['height']
        im = im.crop((left, top, right, bottom)) # defines crop points
        name = str(randint(0,9999))+".png"
        im.save(name)
        replyphoto(update, name)
    except:
        traceback.print_exc()
    subprocess.Popen("rm "+name, shell=True)
    driveravaible = True
    
def send( chat, text):
    return bot.send_message(chat, text, parse_mode="markdown")

def sendtyping( update):
    return bot.send_chat_action(chat_id=getchatid(0, update), action=telegram.ChatAction.TYPING)
    
def reply( update, text):
    send(getchatid(0, update), text)
    #return update.message.reply_text(text, parse_mode="markdown")
    
def sendphoto( chat, filename):
    #bot.send_photo(chatid=chat, photo="https://beyondthestarsastrology.files.wordpress.com/2013/12/smaug.jpg")
    return bot.send_photo(chat_id=chat, photo=open(filename, 'rb'))

def sendphotourl( chat, url):
    return bot.send_photo(chatid=chat, photo=url)
    
def replyphoto( update, filename):
    sendphoto(getchatid(0,update), filename)
    #return update.message.reply_photo(photo=open(filename, 'rb'))
    #return bot.send_photo(getchatid(0, update), photo=open(filename, 'rb'))
    
def getchatid( bot, update):
    return int(update.message.chat.id)

def sendtoelement( name, keys):
    element = driver.find_element_by_name(str(name))
    element.send_keys(str(keys))
        
def clickelement( by, name):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, name))
    )
    element.click() 
