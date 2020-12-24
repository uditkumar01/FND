import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import telegram

import os

import time

from googlesearch import search 
import requests 
from bs4 import BeautifulSoup 

# from nltk.corpus import stopwords
import time
import string
import nltk
try:
    nltk.download('all')
except:
    pass
    



fake_list = ["spurious","bogus","bait",'not','negative', "neither", "no", "nope","forged","misinformation","disinformation","fraudulent","fictitious","reliability","counterfeit","make-believe","false","stories","fabricated","pretend","imitation","feign","fraud","falsify","artificial","simulate","forged","forge","forgery","phony","sham","fraudulent","faked","fraudulent","cheat","mock","spurious","feigned"]
all_stops = {'hadn', 'this', 'during', 'does', 'over', 'between', 'any', 'under', "you're", 'if', 'where', 'it', 'weren', 'these', 'again', 'in', '.', 'have', 'not', 'mightn', '%', '}', "weren't", 's', 'so', 'against', 'while', 'few', 'now', 'with', 'into', 'doesn', 'than', '@', 'are', 'of', 'some', 'isn', 'she', 're', 'needn', 'you', "doesn't", 'your', 'yours', 'o', 't', '*', 'but', 'them', '+', 'too', "wasn't", 'do', "that'll", 'hasn', 'own', 'ourselves', 'most', "don't", 'same', "hasn't", '{', '&', 've', 'why', 'above', 'those', 'yourself', 'wasn', 'myself', 'he', "she's", 'by', ';', 'below', '[', "hadn't", 'before', 'which', 'for', '>', "wouldn't", 'there', 'an', 'm', 'me', "shan't", 'ain', '(', 'a', 'has', 'y', 'no', "shouldn't", 'down', 'about', "it's", "isn't", "needn't", 'other', 'the', '=', 'after', '|', "you'd", 'been', 'having', '$', 'themselves', "mustn't", 'herself', '/', ':', 'mustn', 'hers', 'from', 'is', 'can', 'll', '-', "you'll", "aren't", 'should', 'up', 'very', 'whom', 'being', 'then', 'theirs', 'shan', 'd', 'yourselves', '"', "'", 'when', 'was', ',', 'because', '_', "mightn't", 'both', 'nor', 'itself', "you've", 'such', 'their', 'at', 'don', '?', "won't", 'were', 'shouldn', 'am', '`', "should've", '!', 'until', 'just', "didn't", 'and', 'out', 'further', 'how', "haven't", 'won', '^', 'more', 'ours', 'wouldn', 'they', 'to', 'its', 'my', 'only', 'what', 'once', '\\', ')', 'did', 'her', 'here', 'through', 'ma', '~', 'had', 'his', 'haven', '<', 'who', 'aren', 'all', 'didn', 'himself', 'as', 'will', 'i', 'that', 'our', 'doing', 'be', 'him', 'couldn', 'each', '#', 'we', 'off', 'or', "couldn't", 'on', ']'}


def get_list(query):
    
    get_tokens = nltk.word_tokenize(query)
    # get_query_fake_words = []
    text_no_stop_words_punct = [t for t in get_tokens if t not in all_stops or t in fake_list]

    print(text_no_stop_words_punct)
    return set(text_no_stop_words_punct)



def getdata(url, query_dict,query): 
    start_time = time.time()
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
                if time.time() - start_time > 1:
                    return [percent, image, link1]
                html_text = data.get_text()
                if query in html_text:
                    return [100, image, link1]
                else:
                    diff_l = query_dict - get_list(html_text)
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
    for j in search(query ,num_results=20, lang="en"):

        per = total_count/20
        try:
            # time.sleep(1.5)
            if total_count==0 or total_count%4==0:
                diff = math.ceil(per*15)
                msg.edit_text("["+"●"*diff+"○"*(15-diff)+"]"+" "+str(math.ceil(per*100))+"%\n\n"+str(j))
        except:
            pass

        
        ans1 = getdata(j,query_dict,query)
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
    
    update.message.reply_text('Hi, this bot can help you to check if a news is fake or not.\n')

def convert(update, context):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Now, please send the news.')


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
            caption = "\n<strong>This news is "+ str(ans[0]) +"% true. To know more about it -> </strong> <em><a style='font-size:10px;' href='"+ans[2]+"'>learn more</a></em>\n\n<em style='color:rgb(0,255,255);'>Hope You like it ...</em>"
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
