from django.conf import settings
from profiles.models import Layer, LayerAccess
from sqlalchemy import create_engine
import geopandas as gpd
import uuid


def uploading_process(file_name, table_name, owner_layer):
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    name = settings.DATABASES['default']['NAME']
    conn = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(conn)

    uuid_table = str(uuid.uuid4())
    gdf = gpd.read_file(file_name)
    gdf.to_postgis(name=uuid_table, con=engine, schema='geodata')
    Layer.objects.create(layer_id=uuid_table, table_name=table_name)
    LayerAccess.objects.create(user_id_id=owner_layer, layer_id_id=uuid_table, access_code_id=0)
    return
