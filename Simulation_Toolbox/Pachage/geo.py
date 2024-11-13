def dist_sources_area(dataframe,tag,N,distance,error): 
    # Define input arrays
    import geopandas as gpd
    import osmnx as ox
    import numpy as np
    import warnings
    area=[]
    area2=[]
    err1=[]
    # Define an array to store errors and make a buffer to calculate the error
    X1=dataframe.to_crs("EPSG:3035").buffer(distance);
    # Define x,y longitudes and latitudes
    x1,y1=dataframe.geometry.to_crs("EPSG:3035").values.x,dataframe.geometry.to_crs("EPSG:3035").values.y
    for j in range(0,len(dataframe)):
        # The osmnx takes latitude and longitudes as input instead
        B=ox.geometries.geometries_from_point((dataframe.geometry.values.y[j],dataframe.geometry.values.x[j]),tags=tag,dist=distance);
        warnings.filterwarnings("ignore")
        # If no sources is near area is zero and continue to next location
        if B.empty==1:
            area.append(0)
            err1.append(0)
            continue
        # Generate points with a radius r and at angle theta 
        r,theta=np.sqrt(np.random.rand(N))*distance,np.random.rand(N)*2*np.pi
        # Convert the generated points back to cartitian coordiantes 
        x0=x1[j]+r*np.cos(theta)
        y0=y1[j]+r*np.sin(theta)
        # Upload points to geopandas
        X2=gpd.GeoDataFrame(geometry=gpd.points_from_xy(x0,y0),crs="EPSG:3035")
        # If geometries are defined by polygons 
        if B.geom_type[0]=='Polygon':
            points=gpd.sjoin(X2, B.to_crs("EPSG:3035"), predicate = 'within').geometry
            if error==True:
                B_area=B.to_crs("EPSG:3035").intersection(X1.iloc[j]).area.sum()
                err1.append((len(points)/(N)*distance**2*np.pi-B_area)/(B_area))

        # If geometries are defined by lines the lines get buffed with 6 meters to get the road to real size 12-18 m
        if B.geom_type[0]=="LineString":
            B=gpd.GeoDataFrame(geometry=B.to_crs("EPSG:3035").buffer(3),crs="EPSG:3035")
            points=gpd.sjoin(X2, B, predicate = 'within').geometry
            if error==True:
                B_area=B.intersection(X1.iloc[j]).area.sum()
                err1.append((len(points)/(N)*distance**2*np.pi-B_area)/(B_area))
        
        # Calculate the distance between the location and the points inside the areas or lines  
        dist=np.sqrt((points.geometry.x.values-x1[j])**2+(points.geometry.y.values-y1[j])**2)
        # Calulate the p/N *1/exp(dist*alpha))
        area.append(np.nansum(distance**2*np.pi*np.exp(-dist*5/(distance))/N))        
    return area,err1