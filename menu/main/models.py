from django.db import models

# Create your models here.

class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    parent_id = models.IntegerField(null=True)
    class Meta:
       indexes = [models.Index(fields=['type'], name='main_menu_type_ix')]
