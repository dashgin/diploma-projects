from django.contrib import admin

from unilab.jobs.models import Application, Job

admin.site.register(Job)
admin.site.register(Application)
