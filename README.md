# @seng_bot source code

This is the source code to @seng_bot, a Telegram Bot that is hosted on AWS Lambda and Amazon API Gateway.

Its current functions are to:

* Return weather information based on a requestor's current location
* Return dengue cluster information based on a requestor's current location

If you want to deploy this bot on your own, you can [follow this guide](http://dchua.com/2016/03/22/writing-a-serverless-python-microservice-with-aws-lambda-and-aws-api-gateway/) which should provide a rough guide on deploying this app.

### Prerequisite

1. Make sure you have already created a Telegram Bot

### Pre-deployment checklist

1. Make sure you run

```bash
$ pip install -r requirements.txt -t .
# this is to make sure the modules will be able to be used by AWS Lambda
```

2. Add your telegram bot API key into a __.env__ file.

Your .env file should look like:

```
# .env
TELEGRAM_API_KEY=<APIKEY>
```

3. Zip up the files

```bash
$ zip -r py.zip *
$ zip -j py.zip .env
```

4. Upload the zip file into AWS Lambda

5. Setup your update-hook

```bash
# INVOKE_URL being your Amazon API Gateway Production URL
# ACCESS_TOKEN being your Telegram Bot API Key
$ curl --data "url=<INVOKE_URL>" "https://api.telegram.org/bot<ACCESS_TOKEN>/setWebhook"
```

### Pull Requests
Pull requests are greatly welcomed. Feel free to add in any stuff that you'd like the bot to do.

Seng Bot is already currently running, if you're on Telegram, please invite @seng_bot into your groups to try out his functions.

I'd like this bot to be a community bot so if you have any cool stuff you'd like to add, just pull request over and I'll deploy bot.

### Current Functions

@seng_bot currently only listens for Location messages. To test out his ability, share your location with the bot and he will return information like the following:

![Screenshot](https://cloud.githubusercontent.com/assets/68039/14183524/57066664-f7a3-11e5-88fd-9d1c517c6e77.png)
