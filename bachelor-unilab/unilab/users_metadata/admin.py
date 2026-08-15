from django.contrib import admin

from unilab.users_metadata.models import (
    Certification,
    EducationData,
    ExperienceData,
    ExternalProfile,
    SkillData,
    UniversityCourse,
    UserData,
)

admin.site.register(Certification)
admin.site.register(EducationData)
admin.site.register(ExperienceData)
admin.site.register(ExternalProfile)
admin.site.register(SkillData)
admin.site.register(UserData)
admin.site.register(UniversityCourse)
