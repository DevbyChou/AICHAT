from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import re
import numpy as np
import pickle
import pandas as pd

app = Flask(__name__)

line_bot_api = LineBotApi('J3oheb486dMEMFNobxECJe0nCw8MoxyqdfFEVavVb3v55kvb8ehgKSsBTstSvnspj3mFXzF4/DrpQKRyeib8fN53xEQ2J48Odr8hGZhUwiSIkZKnT1Cs6ypUmljGQ5XOMBNFyHFC15Oqjm4FAxMs/wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2fdc5534dead9ae2d5140e44be70ab45')

model = pickle.load(open('./model/Transport_sugar_model.pkl', 'rb'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(403)
    return 'OK'


def calculate_forecasted_sumnet(years_ahead):
    steps = years_ahead * 365  
    forecast_values = model.get_forecast(steps=steps).predicted_mean
    total_sumnet = forecast_values.sum()
    return total_sumnet

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    match = re.search(r"forecast (\d+) years", user_message)
    if match:
        years_ahead = int(match.group(1))
        total_sumnet = calculate_forecasted_sumnet(years_ahead)
        response_message = f"Forecasted total SumNet for the next {years_ahead} years: {total_sumnet:.4f}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Please ask for a forecast in the format "forecast X years".')
        )

if __name__ == "__main__":
    app.run()
