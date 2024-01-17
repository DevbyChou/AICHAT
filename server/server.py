from flask import Flask, request, jsonify
import requests
from transformers import pipeline, set_seed
import joblib

app = Flask(__name__)

# Load the combined models
models = joblib.load("combined_models.joblib")
reg_model = models['regression_model']
clf_model = models['classification_model']

# Initialize the text generation model
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# Function to make a forecast (you'll need to customize this)
def make_forecast(input_data):
    return reg_model.predict([input_data])[0]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data['events'][0]['message']['text']

    if user_message.startswith("Generate:"):
        input_text = user_message[len("Generate:"):].strip()
        generated_text = generator(input_text, max_length=50, num_return_sequences=1)[0]['generated_text']
        response_message = generated_text
    elif user_message.startswith("Predict:"):
        input_data = user_message[len("Predict:"):].strip()
        forecast_result = make_forecast(input_data)
        response_message = f"Forecast result: {forecast_result}"
    else:
        response_message = "Sorry, I didn't understand that. Please use 'Generate:' or 'Predict:' to start your message."

    reply_token = data['events'][0]['replyToken']
    headers = {'Authorization': 'Bearer 10ALtNHVzTWxovzEoVbNhVs4MwqWsohjoq+f/4xMPMInHveQQ3dD42QLo6gRjh7rj3mFXzF4/DrpQKRyeib8fN53xEQ2J48Odr8hGZhUwiQOgCDt26zh80wH+etmhfuka1ohkV5kQ5EpqIDcKTjpTgdB04t89/1O/w1cDnyilFU='}
    reply_body = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': response_message}]
    }
    response = requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=reply_body)

    return jsonify(status=200)

if __name__ == '__main__':
    app.run()
