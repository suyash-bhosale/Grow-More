from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import ee
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Earth Engine
service_account = 'firebase-adminsdk-fbsvc@grow-more-analytics.iam.gserviceaccount.com'
ee_credentials = ee.ServiceAccountCredentials(service_account, 'serviceAccount.json')
ee.Initialize(ee_credentials)

# Import utilities after initialization
from firestore_utils import get_farm_data
from gee_utils import calculate_indices
from gemini_utils import generate_farm_advisory
from report_generator import create_report_pdf

app = Flask(__name__)
CORS(app)

@app.route('/get-indices/<farmer_id>', methods=['GET'])
def get_indices(farmer_id):
    try:
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

@app.route('/')
def home():
    return 'Grow More Analytics Backend is Active ✅'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))