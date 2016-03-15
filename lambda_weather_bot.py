from __future__ import print_function
import telebot
import httplib,urllib
import requests
from telebot import types
from requests_futures.sessions import FuturesSession
import json

bot = telebot.AsyncTeleBot('115074314:AAEFfQ3zBcFOhcGqE_K1H0pfxdUeRVPy0zc')

def lambda_handler(event, context):
    """docstring for lambda_handler(event, context)"""
#   data = {"chat_id": '-139342007', 'text': event['body']['message']['text']}
    data = urllib.urlencode(event)
#   task = bot.send_message('-139342007', event['body']['message'])
#   result = task.wait()
#   session = FuturesSession()
#   session.post("http://telegram-dchua.pagekite.me/api/lambda", data)
#    requests.post("https://api.telegram.org/bot115074314:AAEFfQ3zBcFOhcGqE_K1H0pfxdUeRVPy0zc/sendMessage",data)
    process_commands(event)
        #    key = event['key1']
        #    return json
    return event


def process_commands(event):
    """docstring for process_commands(event)"""
    if event and event['body'] and event['body']['message']:
#        message = Struct(**(event['body']['message']))
        message = types.Message.de_json(event['body']['message'])
        print("test")
        print(message)
        print("test2")
        print(event)
        print("test3")
        print(event['body']['message'])
        if 'location' in event['body']['message']:
            weather = get_weather(message.location)
            task = bot.reply_to(message, ("""Looks like everything's going to be a nice and cool {temp} with a min-max of {min}-{max} celcius and a relative humidity of {rh}%.""").format(temp=str(weather['temp']),
                        rh=str(weather['rh']),
                        min=str(weather['min_temp']),
                        max=str(weather['max_temp'])
                        ))
            result = task.wait()
#            task = bot.reply_to(message, "dude, don't send me a location!")
       # else:
            #task =  bot.send_message('-139342007', message.text)
        return event



def get_weather(location):
    """docstring for get_weather"""
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?APPID=03e05da0618c06c5171779cfb79c9e46&lat={lat}&lon={lon}'.format(lat=location.latitude,lon=location.longitude))
    j = json.loads(r.text)
    max_temp = j['main']['temp_max'] - 273.15
    min_temp = j['main']['temp_min'] - 273.15
    temp = j['main']['temp'] - 273.15
    rh = j['main']['humidity']
    cloudy = j['clouds']['all']
    print(cloudy)
    result = {'max_temp': max_temp, 'min_temp': min_temp, 'temp': temp,
            'rh': rh, 'cloudy': cloudy}
    return result


#      @bot.message_handler(commands=['start', 'help'])
#      def send_welcome(message):
#          bot.reply_to(message, "Howdy, how are you doing?")

#    return event['body']['message']
#       @bot.message_handler(func=lambda msg: event.body.message, content_types=['location'])
#       def printout(message):
#           """docstring for printout"""
#           r = requests.get('http://api.openweathermap.org/data/2.5/weather?APPID=03e05da0618c06c5171779cfb79c9e46&lat={lat}&lon={lon}'.format(lat=message.location.latitude,lon=message.location.longitude))
#           j = json.loads(r.text)
#           max_temp = j['main']['temp_max'] - 273.15
#           min_temp = j['main']['temp_min'] - 273.15
#           temp = j['main']['temp'] - 273.15
#           rh = j['main']['humidity']
#           cloudy = j['clouds']['all']
#           bot.reply_to(message, "Looks like everything's going to be a nice and cool {temp} with a relative huminity of {rh}.".format(temp=str(temp), rh=str(rh)))

#       return true
#           #bot.reply_to(message, "Lat Long" + str(message.location.longitude) + ":" +
#        #       str(message.location.latitude) + " chat_id:" + str(message.chat.id))

#   @bot.message_handler(func=lambda m: True)
#   def nope(message):
#       if message.text == "psi":

#   @bot.message_handler(func=lambda m: True)
#   def echo_all(message):
#           bot.reply_to(message, message.text)
