from django.contrib import admin

# Register your models here.

from APICloud import models

admin.site.register(models.UserInfo)
admin.site.register(models.Sign)
admin.site.register(models.Project)
admin.site.register(models.Environment)
admin.site.register(models.Interface)
admin.site.register(models.Case)
admin.site.register(models.Plan)
admin.site.register(models.Report)