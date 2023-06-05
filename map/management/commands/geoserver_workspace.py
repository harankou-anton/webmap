from django.core.management.base import BaseCommand
from django.conf import settings
from geo.Geoserver import Geoserver

def create_workspace():
    geo = Geoserver(service_url=f'http://{settings.GEOSERVER["HOST"]}:{settings.GEOSERVER["PORT"]}/geoserver',
                    username=settings.GEOSERVER["LOGIN_GEOSERVER"],
                    password=settings.GEOSERVER["PASSWORD_GEOSERVER"])
    geo.create_workspace(workspace=settings.GEOSERVER["WORKSPACES"])
    geo.create_featurestore(store_name=settings.GEOSERVER["STORE_NAME"],
                            workspace=settings.GEOSERVER["WORKSPACES"],
                            db=settings.DATABASES["default"]["NAME"],
                            host=settings.DATABASES["default"]["HOST"],
                            pg_user=settings.DATABASES["default"]["USER"],
                            pg_password=settings.DATABASES["default"]["PASSWORD"],
                            schema='geodata')


class Command(BaseCommand):
    help = "Crawl OMA catalog"

    def handle(self, *args, **options):
        create_workspace()
