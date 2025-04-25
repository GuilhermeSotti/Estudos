import geopandas as gpd

def enrich_with_shapefile(df, shapefile_path: str, lon_col: str, lat_col: str):
    """
    Converte df em GeoDataFrame e faz spatial join com shapefile.
    """
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326"
    )
    regions = gpd.read_file(shapefile_path)
    return gpd.sjoin(gdf, regions, how="left", op="within")
