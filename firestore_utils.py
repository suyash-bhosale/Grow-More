# Mock in-memory storage for demo purposes
farm_data_store = {}

def get_farm_data(uid, db):
    """Fetch farm coordinates and farmer name from mock storage"""
    if uid in farm_data_store:
        data = farm_data_store[uid]
        
        # Convert to GEE-compatible format: [[lng, lat], [lng, lat]]
        coordinates = []
        if 'boundary' in data:
            for point in data['boundary']:
                coordinates.append([point['lng'], point['lat']])
        else:
            # Default coordinates for Pune area if no boundary set
            coordinates = [
                [73.8540, 18.5180],
                [73.8540, 18.5230], 
                [73.8590, 18.5230],
                [73.8590, 18.5180]
            ]
        
        return {
            "coordinates": coordinates,
            "name": data.get('farmerName', 'Unknown Farmer')
        }
    else:
        # Return default farm data for demo
        return {
            "coordinates": [
                [73.8540, 18.5180],
                [73.8540, 18.5230],
                [73.8590, 18.5230], 
                [73.8590, 18.5180]
            ],
            "name": f"Demo Farmer {uid}"
        }

def save_farm_data(farmer_data, db):
    """Save farm data to mock storage"""
    try:
        # Use phone number as storage key
        farm_data_store[farmer_data['phone']] = farmer_data
        print(f"Saved farm data for farmer: {farmer_data.get('farmerName', 'Unknown')}")
        return True
    except Exception as e:
        print(f"Error saving farm data: {e}")
        return False
