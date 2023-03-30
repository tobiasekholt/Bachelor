import psycopg2
import psycopg2.extras
import geopandas as gpd
import json

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="postgresql-dev-kartai.postgres.database.azure.com",
    database="kartai_bachelor_2023",
    user="kartai_bachelor_2023@postgresql-dev-kartai",
    password="Io4$7M1e"
)
cursor = conn.cursor()

# Read the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file(r"C:\Users\nikla\Bachelor\Bachelor_2023\Bachelor\ngisopenapi\buildings.geojson")

# Add a properties column to the GeoDataFrame (if not already present)
if "properties" not in gdf.columns:
    gdf = gdf.rename(columns={'json': 'properties'})

# Add a geom column to the GeoDataFrame (if not already present)
if "geom" not in gdf.columns:
    gdf = gdf.rename(columns={'geometry': 'geom'})

# Create the table
create_table_sql = "CREATE TABLE IF NOT EXISTS buildings (properties json, geom geometry);"
cursor.execute(create_table_sql)
conn.commit()

# Convert the properties column to a Python dictionary
gdf['properties'] = gdf['properties'].apply(json.loads)

# Insert the data into the table
insert_sql = "INSERT INTO buildings (properties, geom) VALUES %s"
psycopg2.extras.execute_values(cursor, insert_sql, [(row['properties'], row['geom'].wkb_hex) for _, row in gdf.iterrows()])
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()