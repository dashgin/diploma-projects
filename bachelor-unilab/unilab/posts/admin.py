from django.contrib import admin
from .models import Post, Vote, Comment, PostReport, FeedbackForm


admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(PostReport)
admin.site.register(FeedbackForm)
