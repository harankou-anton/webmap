from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import geopandas as gpd


def updating_process(file_name, uuid_table):
    # Create connection to database
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    name = settings.DATABASES['default']['NAME']
    conn = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    engine = create_engine(conn)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Update data in database
    statement = text(f'DELETE FROM geodata."{uuid_table}";')
    session.execute(statement)
    session.commit()
    gdf = gpd.read_file(file_name)
    gdf.to_postgis(name=uuid_table, con=engine, schema='geodata', if_exists='append')
    return
