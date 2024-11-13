def dist_house(dataframe,tag,distance,monte): 
    # Define input arrays
    import geopandas as gpd
    import osmnx as ox
    import numpy as np
    import warnings
    B=ox.geometries.geometries_from_point((dataframe.geometry.y,dataframe.geometry.x),tags=tag,dist=distance);
    warnings.filterwarnings("ignore")
    B=B[B.geom_type!="Point"]
    if B.empty==1:
        return 0

    if B.geom_type[0]=='Polygon':
        points=gpd.sjoin(monte, B.to_crs("EPSG:3035"), predicate = 'within').index
        # If geometries are define by lines the lines get buffed with 6 meters to get the road to real size 12-18 m
    if B.geom_type[0]=="LineString":
        B=gpd.GeoDataFrame(geometry=B.to_crs("EPSG:3035").buffer(3),crs="EPSG:3035")
        points=gpd.sjoin(monte, B, predicate = 'within').index
    # Calculate the distance between the location and the points inside the areas or lines
    area=np.nansum(distance**2*np.pi*np.exp(-monte.r[points]*5/(distance))/len(monte))        
    return area

def extrapoltion(adress,N):
    import geopandas as gpd
    import numpy as np
    import pandas as pd
    data_location=gpd.tools.geocode(adress)
    r,theta=np.sqrt(np.random.rand(N))*1000,np.random.rand(N)*2*np.pi
    # Convert the generated points back to cartitian coordiantes 
    # 10^3 m tags   
    for i in range(len(data_location)):
        location=data_location.iloc[i]
        if location.address==None:
            data=pd.DataFrame([[np.nan, np.nan,np.nan,np.nan,np.nan,np.nan]], columns=np.array(["powerplant","roads","highway","forest","water","airport"]))
            data1=pd.concat([data1,data],ignore_index=True)
            continue
        x,y=data_location.geometry.to_crs("EPSG:3035").values[i].x,data_location.geometry.to_crs("EPSG:3035").values[i].y
        x0=x+r*np.cos(theta)
        y0=y+r*np.sin(theta)
        # 10^4 m tags
        x1=x+r*10*np.cos(theta)
        y1=y+r*10*np.sin(theta)
        monte0=gpd.GeoDataFrame(geometry=gpd.points_from_xy(x0,y0),crs="EPSG:3035")
        monte0=monte0.assign(r=r)
        monte1=gpd.GeoDataFrame(geometry=gpd.points_from_xy(x1,y1),crs="EPSG:3035")
        monte1=monte1.assign(r=r*10)
        powerplant=dist_house(location,{"power":"plant"},10000,monte1);
        Roads=dist_house(location,{'highway':['primary','secondary','tertiary']},1000,monte0);
        highway=dist_house(location,{'highway':['trunk', 'motorway']},1000,monte0);
        forest=dist_house(location,{"landuse":"forest"},1000,monte0);
        water=dist_house(location,{"natural":"water"},1000,monte0);
        airport=dist_house(location,{"aeroway":"aerodrome"},10000,monte1)
        farmland=dist_house(location,{"landuse":"farmland"},10000,monte1)
        industrial=dist_house(location,{"landuse":"industrial"},10000,monte1)
        if i==0:
            data1=pd.DataFrame([[powerplant, Roads,highway,forest,water,airport,farmland,industrial]], columns=np.array(["powerplant","roads","highway","forest","water","airport","farmland","industrial"]))
        else:
            data=pd.DataFrame([[powerplant, Roads,highway,forest,water,airport,farmland,industrial]], columns=np.array(["powerplant","roads","highway","forest","water","airport","farmland","industrial"]))
            data1=pd.concat([data1,data],ignore_index=True)
        
    return data1
    
def extrapoltion_one(adress,N):
    import geopandas as gpd
    import numpy as np
    import pandas as pd
    data_location=gpd.tools.geocode(adress)
    r,theta=np.sqrt(np.random.rand(N))*1000,np.random.rand(N)*2*np.pi
    # Convert the generated points back to cartitian coordiantes 
    # 10^3 m tags   
    x,y=data_location.geometry.to_crs("EPSG:3035").values.x,data_location.geometry.to_crs("EPSG:3035").values.y
    x0=x+r*np.cos(theta)
    y0=y+r*np.sin(theta)
    # 10^4 m tags
    x1=x+r*10*np.cos(theta)
    y1=y+r*10*np.sin(theta)
    monte0=gpd.GeoDataFrame(geometry=gpd.points_from_xy(x0,y0),crs="EPSG:3035")
    monte0=monte0.assign(r=r)
    monte1=gpd.GeoDataFrame(geometry=gpd.points_from_xy(x1,y1),crs="EPSG:3035")
    monte1=monte1.assign(r=r*10)
    powerplant=dist_house(data_location,{"power":"plant"},10000,monte1);
    Roads=dist_house(data_location,{'highway':['primary','secondary','tertiary']},1000,monte0);
    highway=dist_house(data_location,{'highway':['trunk', 'motorway']},1000,monte0);
    forest=dist_house(data_location,{"landuse":"forest"},1000,monte0);
    water=dist_house(data_location,{"natural":"water"},1000,monte0);
    airport=dist_house(data_location,{"aeroway":"aerodrome"},10000,monte1)
    farmland=dist_house(data_location,{"landuse":"farmland"},10000,monte1)
    industrial=dist_house(data_location,{"landuse":"industrial"},10000,monte1)
    data1=pd.DataFrame([[powerplant, Roads,highway,forest,water,airport,farmland,industrial]], columns=np.array(["powerplant","roads","highway","forest","water","airport","farmland","industrial"])) 
    return data1