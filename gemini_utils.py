import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_prompt(index_values):
    return f"""
You are an agricultural advisor. Analyze these vegetation indices:
NDVI: {index_values.get('ndvi', 'N/A')} (Vegetation Health)
NDRE: {index_values.get('ndre', 'N/A')} (Nitrogen Content)
GNDVI: {index_values.get('gndvi', 'N/A')} (Chlorophyll)
MSI: {index_values.get('msi', 'N/A')} (Water Stress)

Provide concise recommendations in this format:
1. Crop health summary (1 sentence)
2. Top 3 actionable suggestions
3. Water management advice
4. Nutrient management tips
Use simple language suitable for farmers.
"""

def generate_farm_advisory(index_values):
    if not GEMINI_API_KEY:
        return "Gemini API key not configured. Please contact support."
    
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        prompt = generate_prompt(index_values)

        body = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, params=params, json=body, timeout=30)
        response.raise_for_status()
        
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"AI advisory unavailable: {str(e)}. Please try again later."