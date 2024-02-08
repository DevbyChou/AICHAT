from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

with open('model\Transport_Hops_Model.pkl', 'rb') as file:
    model = pickle.load(file)

def process_data(data_df):
    relevant_columns = ['i1_rcs_p', 'i1_rcs_e', 'i1_dep_1_p', 'i1_dep_1_e', 'i1_rcf_1_p', 'i1_rcf_1_e']
    data_df = data_df[relevant_columns]
    data_df = data_df.replace('?', np.nan).dropna().astype(float)
    return data_df

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # แปลงข้อมูลเป็น DataFrame
    data_df = process_data(pd.DataFrame(data, index=[0]))
    # ทำนายผลลัพธ์
    prediction = model.predict(data_df)
    return jsonify({'prediction': list(prediction)})

if __name__ == '__main__':
    app.run(debug=True)
