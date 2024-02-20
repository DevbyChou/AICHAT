
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import pickle
from statsmodels.tsa.statespace.sarimax import SARIMAXResults

app = Flask(__name__)

with open('model\Transport_sugar_model.pkl', 'rb') as file:
    model: SARIMAXResults = pickle.load(file)

def process_input_data(data):
    processed_data = pd.DataFrame(data)
    
    processed_data['date'] = pd.to_datetime(processed_data['date'], dayfirst=True)
    processed_data.set_index('date', inplace=True)
        
    return processed_data

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        processed_data = process_input_data(data)
        
        forecast = model.forecast(steps=len(processed_data))
        
        response = {'forecast': forecast.tolist()}
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
