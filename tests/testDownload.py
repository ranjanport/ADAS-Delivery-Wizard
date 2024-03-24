from osgeo import ogr
import os

def download_table_from_postgres(table_name, output_file, database_name, user, password, host='localhost', port=5432, schema_name='public', srs='EPSG:4326'):
    # Connect to the PostgreSQL database
    conn_str = f"PG:host={host} user={user} port={port} password={password} dbname={database_name}"
    conn = ogr.Open(conn_str)
    if conn is None:
        print("Could not connect to the database.")
        return

    # Get the PostgreSQL driver
    ogr_pg = ogr.GetDriverByName('PostgreSQL')
    if ogr_pg is None:
        print("PostgreSQL driver not available.")
        return

    # Create a new data source for the output file
    out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(output_file)
    if out_ds is None:
        print("Could not create output data source.")
        return
    
    # Set the SRS
    target_srs = ogr.osr.SpatialReference()
    target_srs.SetFromUserInput(srs)

    # Create a new layer in the output data source
    out_layer = out_ds.CreateLayer(table_name, srs=target_srs, geom_type=ogr.wkbUnknown)
    if out_layer is None:
        print("Could not create output layer.")
        return

    # Connect to the input table in PostgreSQL
    input_layer = conn.GetLayerByName(f"{schema_name}.{table_name}")
    if input_layer is None:
        print("Input table not found in PostgreSQL.")
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
    conn = None
    
    
# Usage example
output_path = "/Users/aman/mnt/vol/Code/Python/ADAS_DELIVERY/Others/"  # Change this to the path where you want to save the Shapefile
table_name = "yrr"  # Change this to the name of the table you want to download
database_name = "adas"
user = "postgres"
schema_name = "aman"
password = "postgres"
host = "localhost"  # Change this to your database host if needed
port = 5432  # Change this to your database port if needed
srs = "EPSG:4326"
output_file = os.path.join(output_path,"file.shp")
print(output_file)
download_table_from_postgres(table_name, output_file, database_name, user, password, host, port, schema_name, srs)
