from __future__ import print_function
import telebot
import httplib,urllib
import math
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from telebot import types
# from requests_futures.sessions import FuturesSession
import json


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

telegram_api_key = os.environ.get("TELEGRAM_API_KEY")
print("TELEGRAMMMM")
print(telegram_api_key)
bot = telebot.AsyncTeleBot(telegram_api_key)

def lambda_handler(event, context):
    """docstring for lambda_handler(event, context)"""
#   data = {"chat_id": '-139342007', 'text': event['body']['message']['text']}
    data = urllib.urlencode(event)
#   task = bot.send_message('-139342007', event['body']['message'])
#   result = task.wait()
#   session = FuturesSession()
#   session.post("http://telegram-dchua.pagekite.me/api/lambda", data)
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
            weatherMessage = get_weather_message(weather)
            task = bot.reply_to(message, weatherMessage)
            location = message.location
            result = requests.get("https://dengue-dchua.pagekite.me/near?lat={lat}&lng={lng}".format(lat=location.latitude,
            lng=location.longitude)).json()
            dengueMessage = get_dengue_message(result)
            print(result)
            task.wait()
            task = bot.reply_to(message, dengueMessage)
            task.wait()

#           task = bot.reply_to(message, ("""Looks like everything's going to be a nice and cool {temp} with a min-max of {min}-{max} celcius and a relative humidity of {rh}%.""").format(temp=str(weather['temp']),
#                       rh=str(weather['rh']),
#                       min=str(weather['min_temp']),
#                       max=str(weather['max_temp'])
#                       ))
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

def get_dengue_message(dengue):
    cases = dengue['cases']
    distance = math.ceil(dengue['distance_in_meters'])
    description = dengue['description']
    return "There are {cases} cases of dengue within {distance} meters from you."\
    "The cluster where it's happening is in {description}".format(cases=cases,
            distance=distance, description=description)

def get_weather_message(weather):
    min_temp = weather['min_temp']
    max_temp = weather['max_temp']
    rh = weather['rh']
    temp = weather['temp']

    deviateMessage = tempDeviate(min_temp, max_temp, temp)
    temperatureMessage = tempVerdict(temp)

    return "{deviateMessage}{temperatureMessage} with a relative humidity of {rh}.".format(deviateMessage=str(deviateMessage),
                    temperatureMessage=str(temperatureMessage), 
                    rh=str(rh))


def tempDeviate(min_temp, max_temp, temp):
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

