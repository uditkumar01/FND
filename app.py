from apiclient.discovery import build

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import telegram

import os

import time

my_api_key = "AIzaSyCyMa_joKNbuNXSKHLXNFF1IL_YKArXqF8"
my_cse_id = "ff7b372992dbc2e95"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def check_news(query):
    try:
        
        results = google_search(
            query+' true or false', my_api_key, my_cse_id, num=10)
        print(results[0])
        fake_list = ["spurious","bogus","bait",'not',"forged","misinformation","disinformation","fraudulent","fictitious","reliability","counterfeit","make-believe","false","stories","fabricated","pretend","imitation","feign","fraud","falsify","artificial","simulate","forged","forge","forgery","phony","sham","fraudulent","faked","fraudulent","cheat","mock","spurious","feigned"]
        fake_count = 0
        image = []
        link1 = []
        for result in results:
            # print(result.get('link'))
            if (result.get('pagemap'))[0].get('src'):
                image.append((result.get('pagemap'))[0].get('src'))
            if result.get('link'):
                link1.append(result.get('link'))
            for word in fake_list:
                if word in result.get('title').lower().strip().split():
                    fake_count+=11
                    print(word)
            for word in fake_list:
                if word in result.get('snippet').lower().strip().split():
                    fake_count+=9
                    print(word)              
        
        percent = (fake_count/len(fake_list))*100
        if fake_count > 50:
            percent = 100
        if percent > 100:
            percent = 100
        



        print("fake "+str(percent)+" %")
        
        image.append("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTm4AK_Nm2YPvDLnkRY5zse95m9EbiNcP19dg&usqp=CAU")

        return [str(percent)+"% "+"fake", image[0], link1[0]]


    except KeyError:
        print("No Results")
        return ["No Results"]
    
    except:
        return ["queries quota exceeded"]

print(check_news("ronaldo is corona positive"))

# main bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Hi, this bot can help you in your homework.\nTo begin with it type "\convert"')

def convert(update, context):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Now, please send your txt file.')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! Use /start to begin.')

import urllib.request,urllib

def echo(update, context):
    """Echo the user message."""
    ans = check_news(update.message.text)
    print('ssssssssssssssssssssssssssssss',ans)
    
    chat_id = update.message.chat.id
    if len(ans) > 1:
        urllib.request.urlretrieve(ans[1], "msg.jpg")
        with open('msg.jpg', 'rb') as jordan_picture:
            caption = "<strong>This news is "+ ans[0] +".</strong> <em><a style='font-size:10px;' href='ans[2]'>learn more</a></em>"
            context.bot.send_photo(
                chat_id, 
                photo=jordan_picture, 
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
    updater = Updater("1335916148:AAH0LgIGZscF5ayCeVCTNvlSDqU19Kdkyck", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("convert", convert))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # dp.add_handler(MessageHandler(Filters.document.txt, read_pdf))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()