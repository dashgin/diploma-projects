from django.contrib import admin

from .models import Company, CompanyAdmin, CompanyPictures

admin.site.register(Company)
admin.site.register(CompanyAdmin)
admin.site.register(CompanyPictures)
