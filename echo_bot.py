import telebot
import requests
import json

bot = telebot.TeleBot('115074314:AAEFfQ3zBcFOhcGqE_K1H0pfxdUeRVPy0zc')
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['location'])
def printout(message):
    """docstring for printout"""
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?APPID=03e05da0618c06c5171779cfb79c9e46&lat={lat}&lon={lon}'.format(lat=message.location.latitude,lon=message.location.longitude))
    j = json.loads(r.text)
    max_temp = j['main']['temp_max'] - 273.15
    min_temp = j['main']['temp_min'] - 273.15
    temp = j['main']['temp'] - 273.15
    rh = j['main']['humidity']
    cloudy = j['clouds']['all']
    bot.reply_to(message, "Looks like everything's going to be a nice and cool {temp} with a relative huminity of {rh}.".format(temp=str(temp), rh=str(rh)))


    #bot.reply_to(message, "Lat Long" + str(message.location.longitude) + ":" +
     #       str(message.location.latitude) + " chat_id:" + str(message.chat.id))

@bot.message_handler(func=lambda m: True)
def nope(message):
    if message.text == "psi":
        bot.reply_to(message, "The PSI today is over 9000")

#   @bot.message_handler(func=lambda m: True)
#   def echo_all(message):
#           bot.reply_to(message, message.text)

bot.polling()
