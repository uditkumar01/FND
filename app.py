import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import telegram

import os

import time

from googlesearch import search 
import requests 
from bs4 import BeautifulSoup 

from nltk.corpus import stopwords
import string
import nltk


fake_list = ["spurious","bogus","bait",'not', "neither", "no", "nope","forged","misinformation","disinformation","fraudulent","fictitious","reliability","counterfeit","make-believe","false","stories","fabricated","pretend","imitation","feign","fraud","falsify","artificial","simulate","forged","forge","forgery","phony","sham","fraudulent","faked","fraudulent","cheat","mock","spurious","feigned"]



def get_list(query):
    stop = set(stopwords.words('english'))
    all_stops = stop | set(string.punctuation)
    get_tokens = nltk.word_tokenize(query)
    # get_query_fake_words = []
    text_no_stop_words_punct = [t for t in get_tokens if t not in all_stops or t in fake_list]

    print(text_no_stop_words_punct)
    return set(text_no_stop_words_punct)



def getdata(url, query_dict): 

    try:
        with requests.session() as s:
            r = s.get(url) 
            percent = 0
            soup = BeautifulSoup(r.text, 'html.parser')
            img_tags = soup.find_all('img')
            image,link1 = "",url

            for img in img_tags:
                try:
                    image_link = img.get('src')
                    if image_link and 'static' not in image_link and 'http' in image_link and ('.jpg' in image_link or '.png' in image_link or 'webp' in image_link or '.JPG' in image_link or '.PNG' in image_link or 'jpeg' in image_link or 'JPEG' in image_link) :
                        image=str(image_link)
                        break
                        
                except:
                    pass
            z2 = soup.find_all("h1") + soup.find_all("h2") + soup.find_all("h3") + soup.find_all("h4") + soup.find_all("h5") + soup.find_all("h6") + soup.find_all("p")
            for data in z2:

                diff_l = query_dict - get_list(data.get_text())
                percent = (len(diff_l)/len(query_dict))*100
                for word in diff_l:
                    if word in fake_list:
                        percent = 0


        return [percent, image, link1]
        
    except:

        return -1


# to search 
def search_me(query, msg):
    # print(query)
    print(query)
    query_dict = get_list(query)
    total,total_count = 0,0
    image,link1 = "",""

    import time,math
    # time_now = time.time()
    # first_time = True
    for j in search(query+" is it true ?" ,num_results=10, lang="en"):

        per = total_count/10
        try:
            # time.sleep(1.5)
            if total_count==0 or total_count%4==0:
                diff = math.ceil(per*15)
                msg.edit_text("["+"●"*diff+"○"*(15-diff)+"]"+" "+str(math.ceil(per*100))+"%\n\n"+str(j))
        except:
            pass

        
        ans1 = getdata(j,query_dict)
        if ans1 == -1:
            pass
        else:
            if ans1[0] == 100:
                [round(100,2),image,link1]
            total+=ans1[0]
            if image=="":
                image = ans1[1]
            if link1=="":
                link1 = ans1[2]
            total_count+=1

    msg.edit_text("[●●●●●●●●●●●●●●●] 100%\n Hope u like it...")
    return [round(total/total_count,2),image,link1]

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
        try:
            urllib.request.urlretrieve(ans[1], "msg.jpg")
        except:
            urllib.request.urlretrieve("https://static.toiimg.com/thumb/imgsize-351883,msid-74902915,width-400,resizemode-4/74902915.jpg", "msg.jpg")
        with open('msg.jpg', 'rb') as my_picture:
            caption = "\n<strong>This news is "+ str(ans[0]) +"% true. To know more about it -> </strong> <em><a style='font-size:10px;' href='"+ans[2]+"'>learn more</a></em>\n<em style='color:green;'>Hope You like it ...</em>"
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
    updater = Updater("1335916148:AAEup9wHp5xuV3BpoAwKtxYl8X589CxBTlg", use_context=True)

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