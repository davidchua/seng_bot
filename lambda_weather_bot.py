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
bot = telebot.AsyncTeleBot(telegram_api_key)

def lambda_handler(event, context):
    """docstring for lambda_handler(event, context)"""
    data = urllib.urlencode(event)
    process_commands(event)
    return event


def process_commands(event):
    """docstring for process_commands(event)"""
    if event and event['body'] and event['body']['message']:
        message = types.Message.de_json(event['body']['message'])
        if 'location' in event['body']['message']:
            weather = get_weather(message.location)
            weatherMessage = get_weather_message(weather)
            task = bot.reply_to(message, weatherMessage)
            location = message.location
            result = requests.get("https://dengue-dchua.pagekite.me/near?lat={lat}&lng={lng}".format(lat=location.latitude,
            lng=location.longitude)).json()
            dengueMessage = get_dengue_message(result)
            task.wait()
            task = bot.reply_to(message, dengueMessage)
            task.wait()
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
