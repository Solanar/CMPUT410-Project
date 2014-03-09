from django.contrib import admin
from data import models

# Register your models here.
admin.site.register(models.Post)
#admin.site.register(models.User)
#admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Friends)
