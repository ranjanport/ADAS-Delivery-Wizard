from osgeo import ogr, osr
import os.path
import psycopg2
from tqdm import tqdm

def upload_file_to_postgres(input_file, schema_name, database_name, user, password, host='localhost', port=5432):
    # Open the input file
    driver = ogr.GetDriverByName('ESRI Shapefile' if input_file.endswith('.shp') else 'MapInfo File')
    if driver is None:
        print("Driver not available for the input file format.")
        return

    datasource = driver.Open(input_file, 0)
    if datasource is None:
        print("Could not open file:", input_file)
        return
    
    layer = datasource.GetLayer()

    # Get field names and types from input file
    layer_defn = layer.GetLayerDefn()
    field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
    field_types = [layer_defn.GetFieldDefn(i).GetType() for i in range(layer_defn.GetFieldCount())]

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database=database_name, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    # Build column definitions for the PostgreSQL table
    column_definitions = ', '.join([f"{field_name} {map_ogr_type_to_pgsql(field_type)}" for field_name, field_type in zip(field_names, field_types)])

    # Create a new table in the specified schema to store the data
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
    table_name = os.path.splitext(os.path.basename(input_file))[0]  # Use base name of input file as table name
    
    # Drop table if it already exists
    cursor.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name};")
    
    cursor.execute(f"CREATE TABLE {schema_name}.{table_name} (id SERIAL PRIMARY KEY, geom GEOMETRY, {column_definitions});")

    # Get total number of features
    total_features = layer.GetFeatureCount()

    # Initialize progress bar
    with tqdm(total=total_features, desc="Uploading data", unit=" features") as pbar:
        # Loop through the features and insert them into the database
        for feature in layer:
            # Reproject geometry to EPSG:4326
            geometry = feature.GetGeometryRef()
            source_srs = geometry.GetSpatialReference()
            target_srs = osr.SpatialReference()
            target_srs.ImportFromEPSG(4326)
            transform = osr.CoordinateTransformation(source_srs, target_srs)
            geometry.Transform(transform)
            geometry_wkb = geometry.ExportToWkb()

            field_values = [feature.GetField(field_name) for field_name in field_names]
            # Insert into the database
            cursor.execute(f"INSERT INTO {schema_name}.{table_name} (geom, {', '.join(field_names)}) VALUES (ST_GeomFromWKB(%s), {', '.join(['%s' for _ in field_names])});", [geometry_wkb] + field_values)
            pbar.update(1)  # Update progress bar

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    
    
    
def map_ogr_type_to_pgsql(ogr_type):
    if ogr_type == ogr.OFTInteger:
        return 'INTEGER'
    elif ogr_type == ogr.OFTReal:
        return 'DOUBLE PRECISION'
    elif ogr_type == ogr.OFTString:
        return 'VARCHAR'
    elif ogr_type == ogr.OFTDateTime:
        return 'TIMESTAMP'
    else:
        return 'VARCHAR'  # Default to VARCHAR for unsupported types

# Function to determine file format and call upload function
def upload_shape_or_tab_file(input_file, schema_name, database_name, user, password, host='localhost', port=5432):
    if input_file.endswith('.shp') or input_file.endswith('.tab'):
        upload_file_to_postgres(input_file, schema_name, database_name, user, password, host, port)
    else:
        print("Unsupported file format. Only Shapefile (.shp) and TAB file (.tab) are supported.")


# Usage example
input_file = "/Users/aman/mnt/vol/Code/Python/ADAS_DELIVERY/Others/CH_ROAD_NETWORK.tab"  # Change this to the path of your TAB or Shapefile
database_name = "adas"
user = "postgres"
schema_name = "aman"
password = "postgres"
host = "localhost"  # Change this to your database host if needed
port = 5432  # Change this to your database port if needed

# print(list_ogr_drivers())

# upload_shapefile_to_postgres(input_file, table_name, database_name, user, password, host, port)
upload_shape_or_tab_file(input_file, schema_name, database_name, user, password, host, port)
