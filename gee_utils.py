import random
import time
from datetime import datetime, timedelta

def calculate_indices(farm_coordinates):
    """Calculate vegetation indices using Google Earth Engine (mock version for demo)"""
    # Simulate processing time for realistic experience
    time.sleep(2)
    
    # Generate realistic mock data based on typical farming conditions
    # These values are typical for healthy crop conditions in India
    
    # Base values with some randomization for realistic variation
    base_ndvi = 0.7 + random.uniform(-0.1, 0.1)  # Healthy vegetation range 0.6-0.8
    base_gndvi = 0.5 + random.uniform(-0.1, 0.1)  # Green vegetation index 0.4-0.6
    base_ndre = 0.35 + random.uniform(-0.05, 0.05)  # Nitrogen content 0.3-0.4
    base_msi = 0.6 + random.uniform(-0.2, 0.2)    # Water stress indicator 0.4-0.8
    
    # Ensure values stay within realistic bounds
    ndvi = max(0.3, min(0.9, base_ndvi))
    gndvi = max(0.2, min(0.7, base_gndvi))
    ndre = max(0.2, min(0.5, base_ndre))
    msi = max(0.3, min(1.0, base_msi))
    
    return {
        'NDVI': round(ndvi, 3),
        'NDRE': round(ndre, 3),
        'GNDVI': round(gndvi, 3),
        'MSI': round(msi, 3)
    }
