from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the saved model, scaler, and label encoder
with open('rf_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request body
        data = request.get_json()

        # Convert data into a NumPy array
        features = np.array(data['features']).reshape(1, -1)

        # Scale the features
        features_scaled = scaler.transform(features)

        # Predict the output
        prediction = rf_model.predict(features_scaled)

        # Decode the prediction to its original label
        prediction_decoded = label_encoder.inverse_transform(prediction)

        # Return the prediction as a JSON response
        return jsonify({
            'success': True,
            'prediction': prediction_decoded[0]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
        
@app.route('/' , methods=['GET'])
def test():
  return jsonify({
    'message' : 'this'
  })

if __name__ == '__main__':
    app.run(debug=True)
