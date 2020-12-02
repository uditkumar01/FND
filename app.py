import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import telegram

import os

import time

from googlesearch import search 
import requests 
from bs4 import BeautifulSoup 


fake_list = ["spurious","bogus","bait",'not', "neither", "no", "nope","forged","misinformation","disinformation","fraudulent","fictitious","reliability","counterfeit","make-believe","false","stories","fabricated","pretend","imitation","feign","fraud","falsify","artificial","simulate","forged","forge","forgery","phony","sham","fraudulent","faked","fraudulent","cheat","mock","spurious","feigned"]






def getdata(url, check_type = True): 

    with requests.session() as s:
        r = s.get(url) 
        fake_count = 0
        soup = BeautifulSoup(r.text, 'html.parser')
        img_tags = soup.find_all('img')
        image,link1 = "",url

        for img in img_tags:
            try:
                image_link = img.get('src')
                if image_link and 'static' not in image_link.lower() and 'qrcode' not in image_link.lower() and 'http' in image_link.lower() and ('.jpg' in image_link.lower() or '.png' in image_link.lower() or 'webp' in image_link.lower() or 'jpeg' in image_link.lower()) :
                    image=str(image_link)
                    break
                    
            except:
                pass

        for data in soup.find_all("p"): 
            if not data:
                break
            # print(data)
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        if fake_count > 50:
            percent = (fake_count/len(fake_list))*100
            if fake_count > 50:
                percent = 100
            if percent > 100:
                percent = 100

            if check_type:
                return [percent, image, link1]
            else:
                return [100-percent, image, link1]

        for data in soup.find_all("h1"): 
            if not data:
                break
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            # data = data.replace('\n',' ')
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        if fake_count > 50:
            percent = (fake_count/len(fake_list))*100
            if fake_count > 50:
                percent = 100
            if percent > 100:
                percent = 100

            if check_type:
                return [percent, image, link1]
            else:
                return [100-percent, image, link1]

        for data in soup.find_all("h2"): 
            if not data:
                break
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        if fake_count > 50:
            percent = (fake_count/len(fake_list))*100
            if fake_count > 50:
                percent = 100
            if percent > 100:
                percent = 100

            if check_type:
                return [percent, image, link1]
            else:
                return [100-percent, image, link1]
        
        for data in soup.find_all("h3"): 
            if not data:
                break
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        if fake_count > 50:
            percent = (fake_count/len(fake_list))*100
            if fake_count > 50:
                percent = 100
            if percent > 100:
                percent = 100

            if check_type:
                return [percent, image, link1]
            else:
                return [100-percent, image, link1]
        
        for data in soup.find_all("h4"):
            if not data:
                break 
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        if fake_count > 50:
            percent = (fake_count/len(fake_list))*100
            if fake_count > 50:
                percent = 100
            if percent > 100:
                percent = 100

            if check_type:
                return [percent, image, link1]
            else:
                return [100-percent, image, link1]
        
        for data in soup.find_all("h5"):
            if not data:
                break 
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        if fake_count > 50:
            percent = (fake_count/len(fake_list))*100
            if fake_count > 50:
                percent = 100
            if percent > 100:
                percent = 100

            if check_type:
                return [percent, image, link1]
            else:
                return [100-percent, image, link1]

        for data in soup.find_all("h5"): 
            if not data:
                break
            data = str(data)
            data = data.replace('<',' ')
            data = data.replace('>',' ')
            data = data.replace('\n',' ')
            for word in data.strip().split():
                if word in fake_list:
                    fake_count += 10

        percent = (fake_count/len(fake_list))*100
        if fake_count > 50:
            percent = 100
        if percent > 100:
            percent = 100

        if check_type:
            return [percent, image, link1]
        else:
            return [100-percent, image, link1]


# to search 
def search_me(query, msg):
    print(query)
    query = query.replace('\n',' ')
    check = True
    for word in query.strip().split():
        if word in fake_list:
            check = False
            break
    
    total,total_count = 0,0
    image,link1 = "",""
    import time,math
    # time_now = time.time()
    # first_time = True
    for j in search(query+" true or false " ,num_results=50, lang="en"):

        per = total_count/50
        try:
            # time.sleep(1.5)
            if total_count==0 or total_count%4==0:
                diff = math.ceil(per*15)
                msg.edit_text("["+"●"*diff+"○"*(15-diff)+"]"+" "+str(math.ceil(per*100))+"%\n\n"+str(j))
        except:
            pass

        ans1 = getdata(j,check)
        total+=ans1[0]
        if image=="":
            image = ans1[1]
        if link1=="":
            link1 = ans1[2]
        total_count+=1

    msg.edit_text("[●●●●●●●●●●●●●●●] 100%\n Hope u like it...")
    return [100-round(total/total_count,2),image,link1]

# main bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Hi, this bot can help you in your homework.\nTo begin with it type "/convert"')

def convert(update, context):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Now, please send your txt file.')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! Use /start to begin.')

import urllib.request,urllib

def echo(update, context):
    """Echo the user message."""
    chat_id = update.message.chat.id
    msg = update.message.reply_text("okay lemme check...")
    ans = search_me(update.message.text, msg)
    print('ssssssssssssssssssssssssssssss',ans)
    
    
    
    if len(ans) > 1:
        urllib.request.urlretrieve(ans[1], "msg.jpg")
        with open('msg.jpg', 'rb') as my_picture:
            caption = "\n<strong>This news is "+ str(ans[0]) +"% fake. To know more about it -> </strong> <em><a style='font-size:10px;' href='"+ans[2]+"'>learn more</a></em>\n<em style='color:green;'>Hope You like it ...</em>"
            context.bot.send_photo(
                chat_id, 
                photo=my_picture, 
                caption=caption,
                parse_mode=telegram.ParseMode.HTML
            )
    else:
        update.message.reply_text(ans[0])
    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ.get('TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("convert", convert))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo, run_async=True))

    # dp.add_handler(MessageHandler(Filters.document.txt, read_pdf))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()