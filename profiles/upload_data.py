from django.conf import settings
from profiles.models import Layer, LayerAccess
from sqlalchemy import create_engine
import geopandas as gpd
import uuid
from geo.Geoserver import Geoserver


def uploading_process(file_name, table_name, owner_layer):
    # Create connection to database
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    name = settings.DATABASES['default']['NAME']
    conn = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(conn)

    # Upload data to database's tables
    uuid_table = str(uuid.uuid4())
    gdf = gpd.read_file(file_name)
    column_names = gdf.columns.to_list()
    gdf.to_postgis(name=uuid_table, con=engine, schema='geodata')
    Layer.objects.create(layer_id=uuid_table, table_name=table_name, table_fields=column_names)
    LayerAccess.objects.create(user_id_id=owner_layer, layer_id_id=uuid_table, access_code_id=0)

    # Publish layer on geoserver
    geo = Geoserver(service_url=f'http://{settings.GEOSERVER["HOST"]}:{settings.GEOSERVER["PORT"]}/geoserver',
                    username=settings.GEOSERVER["LOGIN_GEOSERVER"],
                    password=settings.GEOSERVER["PASSWORD_GEOSERVER"])
    geo.publish_featurestore(store_name='geo_data', pg_table=uuid_table, workspace='layers')
    return
