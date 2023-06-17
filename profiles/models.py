from django.conf import settings
from django.db import models

# Create your models here.
class ProfileUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )

class Layer(models.Model):
    layer_id = models.IntegerField(primary_key=True,)
    table_name = models.CharField()

class LayerAccess(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="layer_accsses")
    layer_id = models.ForeignKey("profiles.Layer", on_delete=models.CASCADE, related_name="layer_accsses")
    access_code = models.ForeignKey('profiles.Accsess', related_name="layer_accsses", null=True, blank=True,
                                    on_delete=models.SET_NULL)

class Accsess(models.Model):
    access_code = models.IntegerField(primary_key=True)
    name = models.CharField()