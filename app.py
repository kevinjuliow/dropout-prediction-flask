from flask import Flask, request, jsonify
import pickle
import numpy as np
from flaskext.mysql import MySQL
import os 

app = Flask(__name__)

# Load the saved model, scaler, and label encoder
with open('rf_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

try:
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    print("Scaler loaded successfully!")
except Exception as e:
    print(f"Error loading scaler: {e}")

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)
print("Classes in label encoder:", label_encoder.classes_)



mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('DATABASE_USERNAME')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DATABASE_NAME')
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route('/predict', methods=['POST'])
def predict():
    try:
     
        data = request.get_json()
        
        name = request.args.get('name')

        expected_features = [
            "marital_status", "application_mode", "course",
            "previous_qualification", "tuition_fees_up_to_date",
            "scholarship_holder", "age_at_enrollment",
            "curricular_units_1st_sem_credited",
            "curricular_units_1st_sem_enrolled",
            "curricular_units_1st_sem_evaluations",
            "curricular_units_1st_sem_approved",
            "curricular_units_1st_sem_grade",
            "inflation_rate"]


      
        missing_features = [feature for feature in expected_features if feature not in data]
        if missing_features:
            return jsonify({
                'success': False,
                'error': f"Missing features: {', '.join(missing_features)}"
            }), 400

        
        features = np.array([data[feature] for feature in expected_features]).reshape(1, -1)
        

        # Scale the features
        features_scaled = scaler.transform(features)

        # Predict the output
        prediction = rf_model.predict(features_scaled)
      
        prediction_decoded = prediction[0]  # Directly use the predicted label
        
       
        insert_to_database(name , features , features_scaled , prediction_decoded)

        return jsonify({
            'features' : features.tolist(),
            'Scaled features': features_scaled.tolist(),
            'name' : name,
            'prediction': prediction_decoded
        })
    except KeyError as e:
        return jsonify({
            'success': False,
            'error': f"Missing feature: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/connection', methods=['GET'])
def check_db_connection():
    try:
        # Create a cursor
        cursor = mysql.connect().cursor()

        cursor.execute("SELECT 1;") 
        result = cursor.fetchall() 

        if result:
            return jsonify({
                'success': True,
                'message': 'Database connection is successful!'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No result returned from the query.'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cursor.close()

@app.route('/history' , methods=['GET'])
def history() : 
    try : 
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM prediction_history
        """)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Convert rows to a list of dictionaries, formatting datetime
        result = [dict(zip(columns, row)) for row in rows]

        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def insert_to_database(name, feature, features_scaled, prediction_decoded):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO prediction_history (name, features, scaled_features, prediction)
            VALUES (%s, %s, %s, %s)
        """, (name, str(feature), str(features_scaled), prediction_decoded))

        conn.commit()
        print("Data inserted successfully!")
        return True
    except Exception as e:
        print(f"Error inserting data into database: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
