from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Member, List, Issue, Assignee, Comment

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Member)
admin.site.register(List)
admin.site.register(Issue)
admin.site.register(Assignee)
admin.site.register(Comment)

