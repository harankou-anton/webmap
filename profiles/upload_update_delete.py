import geopandas as gpd
import os.path
import uuid
from django.conf import settings
from profiles.models import Layer, LayerAccess
from sqlalchemy import create_engine
from geo.Geoserver import Geoserver
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from django.core.files.storage import FileSystemStorage


def create_db_connection():
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    name = settings.DATABASES['default']['NAME']
    conn = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(conn)
    return engine


def create_geoserver_connection():
    geo = Geoserver(service_url=f'http://{settings.GEOSERVER["HOST"]}:{settings.GEOSERVER["PORT"]}/geoserver',
                    username=settings.GEOSERVER["LOGIN_GEOSERVER"],
                    password=settings.GEOSERVER["PASSWORD_GEOSERVER"])
    return geo


def uploading_process(file_name, table_name, owner_layer):
    # Create connection to database
    engine = create_db_connection()

    # Upload data to database's tables
    uuid_table = str(uuid.uuid4())
    gdf = gpd.read_file(file_name)
    column_names = gdf.columns.to_list()
    gdf.to_postgis(name=uuid_table, con=engine, schema='geodata')
    Layer.objects.create(layer_id=uuid_table, table_name=table_name, table_fields=column_names)
    LayerAccess.objects.create(user_id_id=owner_layer, layer_id_id=uuid_table, access_code_id=0)

    # Publish layer on geoserver
    geo = create_geoserver_connection()
    geo.publish_featurestore(store_name='geo_data', pg_table=uuid_table, workspace='layers')
    geo.publish_style(layer_name=uuid_table, style_name='default_style', workspace='layers')
    return


def updating_process(file_name, uuid_table):
    # Create connection to database
    engine = create_db_connection()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Update data in database
    statement = text(f'DELETE FROM geodata."{uuid_table}";')
    session.execute(statement)
    session.commit()
    gdf = gpd.read_file(file_name)
    gdf.to_postgis(name=uuid_table, con=engine, schema='geodata', if_exists='append')
    return


def uploading_style(file_name, style_name, layer_name):
    geo = create_geoserver_connection()
    fss = FileSystemStorage()
    fss.save(file_name.name, file_name)
    geo.upload_style(path=os.path.join(settings.MEDIA_ROOT, file_name.name), name=style_name, workspace='layers')
    geo.publish_style(layer_name=layer_name, style_name=style_name, workspace='layers', )
    os.remove(os.path.join(settings.MEDIA_ROOT, file_name.name))
    return


def delete_layer(layer_id):
    # Create connection to database and geoserver
    engine = create_db_connection()
    Session = sessionmaker(bind=engine)
    session = Session()

    geo = create_geoserver_connection()

    # Delete layer from geoserver
    geo.delete_layer(layer_name=layer_id, workspace='layers')

    # Delete layer from database
    statement = text(f'DROP TABLE geodata."{layer_id}";')
    session.execute(statement)
    session.commit()

    # Delete data about layer from other tables
    Layer.objects.filter(layer_id=layer_id).delete()
