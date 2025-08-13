# Grow More Analytics Backend

A Flask-based backend service for agricultural analytics using satellite data and AI-powered farm advisory.

## Features

- **Vegetation Indices Calculation**: NDVI, NDRE, GNDVI, MSI using Google Earth Engine
- **Farm Data Management**: Firebase Firestore integration
- **AI Advisory**: Google Gemini-powered farm recommendations
- **PDF Reports**: Automated farm health report generation

## Setup

### 1. Environment Variables

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Update `.env` with your actual values:
- `GEMINI_API_KEY`: Get from [Google AI Studio](https://ai.google.dev/)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your service account JSON file

### 2. Service Account Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Generate a service account key (JSON format)
3. Save it as `serviceAccount.json` in the project root
4. Enable Earth Engine API for the same service account

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

## API Endpoints

### `GET /`
Health check endpoint

### `GET /get-indices/<farmer_id>`
Returns vegetation indices for a specific farm

### `GET /generate-report/<farmer_id>`
Generates and downloads a PDF report for a farm

## Security Notes

⚠️ **Important**: 
- Never commit `serviceAccount.json` to version control
- Keep API keys secure and use environment variables
- The `.gitignore` file prevents accidental commits of sensitive files

## Deployment

Configured for [Render.com](https://render.com) deployment using `render.yaml`.

Set environment variables in your deployment platform:
- `GEMINI_API_KEY`
- Upload `serviceAccount.json` as a secret file

## Dependencies

- Flask: Web framework
- Firebase Admin: Firestore database access
- Google Earth Engine: Satellite data processing  
- ReportLab: PDF generation
- Google Gemini: AI advisory generation

## Error Handling

The application includes graceful error handling for:
- Missing credentials
- Database connection issues
- Earth Engine API failures
- PDF generation errors
