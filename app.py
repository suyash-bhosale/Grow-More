from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for
from flask_cors import CORS
import os
import ee
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
try:
    cred = credentials.Certificate('serviceAccount.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Warning: Firebase initialization failed: {e}")
    db = None

# Initialize Earth Engine
try:
    service_account = 'firebase-adminsdk-fbsvc@grow-more-analytics.iam.gserviceaccount.com'
    ee_credentials = ee.ServiceAccountCredentials(service_account, 'serviceAccount.json')
    ee.Initialize(ee_credentials)
except Exception as e:
    print(f"Warning: Earth Engine initialization failed: {e}")

# Import utilities after initialization
from firestore_utils import get_farm_data, save_farm_data
from gee_utils import calculate_indices
from gemini_utils import generate_farm_advisory
from report_generator import create_report_pdf

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

@app.route('/get-indices/<farmer_id>', methods=['GET'])
def get_indices(farmer_id):
    try:
        if db is None:
            return jsonify({'error': 'Database connection not available'}), 500
            
        farm_data = get_farm_data(farmer_id, db)
        if not farm_data:
            return jsonify({'error': 'Farm data not found'}), 404
        
        geometry = farm_data['coordinates']
        if not geometry:
            return jsonify({'error': 'Farm geometry not found'}), 404

        indices = calculate_indices(geometry)
        return jsonify(indices)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-report/<farmer_id>', methods=['GET'])
def generate_report(farmer_id):
    try:
        if db is None:
            return jsonify({'error': 'Database connection not available'}), 500
            
        farm_data = get_farm_data(farmer_id, db)
        if not farm_data:
            return jsonify({'error': 'Farm data not found'}), 404
        
        geometry = farm_data['coordinates']
        if not geometry:
            return jsonify({'error': 'Farm geometry not found'}), 404

        farmer_name = farm_data.get('name', 'Unknown Farmer')
        indices = calculate_indices(geometry)
        indices_lower = {k.lower(): v for k, v in indices.items()}
        advisory_text = generate_farm_advisory(indices_lower)

        pdf_path = f"/tmp/{farmer_id}_report.pdf"
        create_report_pdf(farmer_name, indices, advisory_text, pdf_path)

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{farmer_name.replace(' ', '_')}_report.pdf"
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save-farm', methods=['POST'])
def save_farm():
    try:
        if db is None:
            return jsonify({'error': 'Database connection not available'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        success = save_farm_data(data, db)
        if success:
            return jsonify({'message': 'Farm data saved successfully', 'farmer_id': data.get('phone')})
        else:
            return jsonify({'error': 'Failed to save farm data'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/monitoring')
def monitoring():
    return render_template('monitoring.html')

@app.route('/monitoring/<farmer_id>')
def monitoring_farmer(farmer_id):
    return render_template('monitoring.html')

@app.route('/health')
def health():
    return 'Grow More Analytics Backend is Active ✅'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
