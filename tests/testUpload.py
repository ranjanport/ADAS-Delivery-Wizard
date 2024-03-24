from osgeo import ogr
import psycopg2



def list_ogr_drivers():
    drivers = ogr.GetDriverCount()
    driver_list = []
    for i in range(drivers):
        driver = ogr.GetDriver(i)
        driver_name = driver.GetName()
        driver_list.append(driver_name)
    return driver_list

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

def upload_file_to_postgres(input_file, table_name, database_name, user, password, host='localhost', port=5432):
    # Open the input Shapefile or TAB file
    
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

    # print(field_names)
    # print(field_types)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database=database_name, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    
    # Build column definitions for the PostgreSQL table
    column_definitions = ', '.join([f"{field_name} {map_ogr_type_to_pgsql(field_type)}" for field_name, field_type in zip(field_names, field_types)])

    # Create a new table to store the data
    cursor.execute(f"drop TABLE if exists {table_name} cascade;")
    cursor.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, geom GEOMETRY, {column_definitions});")

    # Loop through the features and insert them into the database
    for feature in layer:
        geometry = feature.GetGeometryRef().ExportToWkb()
        field_values = [feature.GetField(field_name) for field_name in field_names]
        # Insert into the database
        cursor.execute(f"INSERT INTO {table_name} (geom, {', '.join(field_names)}) VALUES (ST_GeomFromWKB(%s), {', '.join(['%s' for _ in field_names])});", [geometry] + field_values)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()




def upload_shape_or_tab_file(input_file, table_name, database_name, user, password, host='localhost', port=5432):
    if input_file.endswith('.shp') or input_file.endswith('.tab'):
        upload_file_to_postgres(input_file, table_name, database_name, user, password, host, port)
    else:
        print("Unsupported file format. Only Shapefile (.shp) and TAB file (.tab) are supported.")







# Usage example
input_file = "/Users/aman/mnt/vol/Code/Python/ADAS_DELIVERY/Others/CH_ROAD_NETWORK.tab"  # Change this to the path of your TAB or Shapefile
table_name = "testUpload"  # Change this to your desired table name
database_name = "adas"
user = "postgres"
password = "postgres"
host = "localhost"  # Change this to your database host if needed
port = 5432  # Change this to your database port if needed

# print(list_ogr_drivers())

# upload_shapefile_to_postgres(input_file, table_name, database_name, user, password, host, port)
upload_shape_or_tab_file(input_file, table_name, database_name, user, password, host, port)
