def get_farm_data(uid, db):
    """Fetch farm coordinates and farmer name from Firestore"""
    doc_ref = db.collection('farms').document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict()
    if 'boundary' not in data:
        return None

    # Convert to GEE-compatible format: [[lng, lat], [lng, lat]]
    coordinates = []
    for point in data['boundary']:
        coordinates.append([point['lng'], point['lat']])
    
    return {
        "coordinates": coordinates,
        "name": data.get('farmerName', 'Unknown Farmer')
    }