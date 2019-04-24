# Register your models here.
from django.contrib import admin

from asker.models import Answers, Profile, Question, User, Tag

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Answers)
admin.site.register(Profile)