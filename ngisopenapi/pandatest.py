import geopandas as gpd
import psycopg2

# Load the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file("C:\\Users\\nikla\\Bachelor\\Bachelor_2023\\Bachelor\\ngisopenapi\\buildings.geojson")

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="postgresql-dev-kartai.postgres.database.azure.com",
    database="kartai_bachelor_2023",
    user="kartai_bachelor_2023@postgresql-dev-kartai",
    password="Io4$7M1e"
)

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Create a table in the database to store the GeoJSON data
table_name = "geojson_table"
gdf.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()
