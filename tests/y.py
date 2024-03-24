from osgeo import ogr
import os

def copy_layer_to_postgres(input_file, database_name, schema_name, user, password, host='localhost', port=5432, srs='EPSG:4326'):
    # Open the input file
    input_ds = ogr.Open(input_file)
    if input_ds is None:
        print("Could not open file:", input_file)
        return
    
    input_layer = input_ds.GetLayer()

    # Extract table name from input file
    table_name = os.path.splitext(os.path.basename(input_file))[0]

    # Connect to the PostgreSQL database
    conn_str = f"PG:host={host} user={user} port={port} password={password} dbname={database_name}"
    conn = ogr.Open(conn_str)
    if conn is None:
        print("Could not connect to the database.")
        return
    
    # Set the SRS
    target_srs = ogr.osr.SpatialReference()
    target_srs.SetFromUserInput(srs)

    # Get the PostgreSQL driver
    ogr_pg = ogr.GetDriverByName('PostgreSQL')
    if ogr_pg is None:
        print("PostgreSQL driver not available.")
        return
    
    # Create a new data source in PostgreSQL
    out_ds = ogr_pg.CreateDataSource(conn_str)
    if out_ds is None:
        print("Could not create data source in PostgreSQL.")
        return
    
    # Create a new layer in the PostgreSQL data source
    out_layer = out_ds.CreateLayer(table_name, srs=target_srs, geom_type=input_layer.GetGeomType(), options=[f'OVERWRITE=YES', f'SCHEMA={schema_name}'])
    if out_layer is None:
        print("Could not create layer in PostgreSQL data source.")
        return
    
    # Copy fields from input layer to output layer
    for i in range(input_layer.GetLayerDefn().GetFieldCount()):
        field_defn = input_layer.GetLayerDefn().GetFieldDefn(i)
        out_layer.CreateField(field_defn)

    # Copy features from input layer to output layer
    for feature in input_layer:
        out_layer.CreateFeature(feature)

    # Clean up
    out_ds = None
    input_ds = None
    conn = None


# Usage example
input_file = "/Users/aman/mnt/vol/Code/Python/ADAS_DELIVERY/Others/CH_ROAD_NETWORK.tab"  # Change this to the path of your TAB or Shapefile
database_name = "adas"
user = "postgres"
schema_name = "aman"
password = "postgres"
host = "localhost"  # Change this to your database host if needed
port = 5432  # Change this to your database port if needed
srs = "EPSG:4326"

copy_layer_to_postgres(input_file, database_name, schema_name, user, password, host, port, srs)
