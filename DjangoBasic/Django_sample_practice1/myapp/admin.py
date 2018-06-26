from django.contrib import admin
from myapp import models

# Register your models here.
admin.site.register(models.Users)
admin.site.register(models.UserType)