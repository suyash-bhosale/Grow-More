import ee
import datetime
from datetime import timedelta 

def calculate_indices(farm_coordinates):
    farm_geom = ee.Geometry.Polygon(farm_coordinates)
    today = datetime.datetime.utcnow().date()
    past = today - timedelta(days=30)  # Wider date range for better coverage

    # Get least cloudy image
    s2 = ee.ImageCollection("COPERNICUS/S2_HARMONIZED") \
        .filterBounds(farm_geom) \
        .filterDate(str(past), str(today)) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first()

    if s2 is None:
        raise Exception("No suitable Sentinel-2 image found")

    # Calculate indices
    ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndre = s2.normalizedDifference(['B8', 'B5']).rename('NDRE')
    gndvi = s2.normalizedDifference(['B8', 'B3']).rename('GNDVI')
    msi = s2.select('B11').divide(s2.select('B8')).rename('MSI')

    # Calculate mean values
    stats = ndvi.addBands([ndre, gndvi, msi]) \
        .reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=farm_geom,
            scale=10,
            maxPixels=1e9
        ).getInfo()

    return {
        'NDVI': round(stats['NDVI'], 4) if 'NDVI' in stats else None,
        'NDRE': round(stats['NDRE'], 4) if 'NDRE' in stats else None,
        'GNDVI': round(stats['GNDVI'], 4) if 'GNDVI' in stats else None,
        'MSI': round(stats['MSI'], 4) if 'MSI' in stats else None
    }