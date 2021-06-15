from rest_framework import serializers
import Constants as keys
from telegram.ext import *
import botResponses as Res
print("Bot started...")
import psycopg2

#connection
connection = psycopg2.connect(user = "#",
                                password = "#",
                                host = "#",
                                database = "#")
#cursor
cur=connection.cursor()

#query
cur.execute("SELECT * from backend_awards WHERE facultyid='#' and facultyname='#'")

#obtain
rows = cur.fetchall()
for i in rows:
    for j in range(6):
        print(i[j])
        if(j==1):
            facultyname=i[j]
        if(j==2):
            facultyid=i[j]
        if(j==3):
            dateawarded=i[j]
        if(j==4):
            awardname=i[j]
        if(j==5):
            awarddescription=i[j]

#Closing
connection.close()

def start_command(update,context):
    update.message.reply_text('Type something you want to get started!')

def help_command(update,context):
    update.message.reply_text('If you need further help try visiting our Website!')

def handle_message(update,context):
    text = str(update.message.text).lower()
    response = Res.sample_responses(text)
    response="Facultyname = "+facultyname+"\n"+"Facultyid = "+facultyid+"\n"+"Awardname = "+awardname+"\n"+"Date Awarded = "+str(dateawarded)+"\n"+"Award Description = "+awarddescription+"\n"
    update.message.reply_text(response)

def error(update,context):
    print(f"Update {update} casued error {context.error}")

def main():
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
main()
