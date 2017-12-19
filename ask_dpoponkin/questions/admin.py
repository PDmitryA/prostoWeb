from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

# Register your models here.
from questions.models import Question, UserImaged, Answer, Tag, LikeToAnswer, LikeToQuestion

admin.site.register(Question)
admin.site.register(UserImaged, UserAdmin)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(LikeToAnswer)
admin.site.register(LikeToQuestion)