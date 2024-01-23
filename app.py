from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

with open('Transport_Hops_Model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # แปลงข้อมูลเป็น DataFrame
    data_df = pd.DataFrame(data, index=[0])
    # ทำนายผลลัพธ์
    prediction = model.predict(data_df)
    return jsonify({'prediction': list(prediction)})

if __name__ == '__main__':
    app.run(debug=True)
