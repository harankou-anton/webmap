from django.conf import settings
from sqlalchemy import create_engine
import geopandas as gpd


def uploading_process(file_name, name_table):
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    name = settings.DATABASES['default']['NAME']
    conn = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(conn)

    gdf = gpd.read_file(file_name)
    gdf.to_postgis(name=name_table, con=engine, schema='geodata')
    return
