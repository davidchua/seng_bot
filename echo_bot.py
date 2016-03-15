import telebot
import requests
import json

bot = telebot.TeleBot('180585798:AAFmLPn8yupJ--M9_i7bqdyYve0gTFPvvbw')
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

    deviateMessage = tempDeviate(min_temp, max_temp)
    temperatureMessage = tempVerdict(temp)

    bot.reply_to(message, "{deviateMessage}{temperatureMessage} with a relative huminity of {rh}.".format(deviateMessage=str(deviateMessage),
                    temperatureMessage=str(temperatureMessage), 
                    rh=str(rh)))


    #bot.reply_to(message, "Lat Long" + str(message.location.longitude) + ":" +
     #       str(message.location.latitude) + " chat_id:" + str(message.chat.id))

@bot.message_handler(func=lambda m: True)
def nope(message):
    if message.text == "psi":
        bot.reply_to(message, "The PSI today is over 9000")

#   @bot.message_handler(func=lambda m: True)
#   def echo_all(message):
#           bot.reply_to(message, message.text)

def tempDeviate(min_temp, max_temp):
    if (max_temp - min_temp >= 5):
        return "The weather might fluctuate a little between {min_temp} and {max_temp}. Prepare for the worst! ".format(min_temp=str(min_temp),max_temp=str(max_temp), temp=str(temp))
    else:
        return ""

def tempVerdict(temp):
    if (temp < 6):
        return "It is going to freezing cold today around {temp}.".format(temp=str(temp))
    elif (6 <= temp <= 12):
        return "It be a bit a little chilly today around {temp}.".format(temp=str(temp))
    elif (12 < temp<= 28):
        return "It is going to be cool and comfortable today around {temp}.".format(temp=str(temp))
    else:
        return "It is going to be warm and hot around {temp}".format(temp=str(temp))

bot.polling()
