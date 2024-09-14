from netCDF4 import Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import iso8601
import cartopy.crs as ccrs
import cartopy.feature as cf
from shapely import Polygon, Point
from gpx import GPX
import gpxpy
from tqdm import tqdm
import geopandas as gpd

class BorderMask:
    
    """ class object refers to defined border"""
    
    def __init__(self,border): 
        # border - list of points (longitude,latitude) 
        self.Border = border 
        # define Polygon by border 
        self.polys = Polygon(border)
        # gdf - GeoDataFrame, here is two columns - mask = True and geometry
        self.d = {'mask':[True],'geometry': [self.polys]} 
        # define GeoDataFrame from points, which we would like to mask   
        self.gdf = gpd.GeoDataFrame(self.d) 
        
    def Mask(self,long, lat):
         # long - 2d (latsize, longsize), lat - 2d (latsize, longsize) 
        shape = long.shape
        
        df = pd.DataFrame({'lon': long.reshape(-1), 'lat': lat.reshape(-1)})
        df['coords'] = list(zip(df['lon'],df['lat']))
        df['coords'] = df['coords'].apply(Point)
        data = gpd.GeoDataFrame(df, geometry='coords')
    
        masked_data = gpd.tools.sjoin(data, self.gdf, predicate="within", how='left').fillna(False)
        mask = np.array(masked_data['mask']).reshape(shape)
    
        return mask
