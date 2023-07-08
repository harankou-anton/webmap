import os.path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from geo.Geoserver import Geoserver


def uploading_style(file_name, style_name, layer_name):
    geo = Geoserver(service_url=f'http://{settings.GEOSERVER["HOST"]}:{settings.GEOSERVER["PORT"]}/geoserver',
                    username=settings.GEOSERVER["LOGIN_GEOSERVER"],
                    password=settings.GEOSERVER["PASSWORD_GEOSERVER"])
    fss = FileSystemStorage()
    fss.save(file_name.name, file_name)
    geo.upload_style(path=os.path.join(settings.MEDIA_ROOT, file_name.name), name=style_name, workspace='layers')
    geo.publish_style(layer_name=layer_name, style_name=style_name, workspace='layers', )
    os.remove(os.path.join(settings.MEDIA_ROOT, file_name.name))
    return
