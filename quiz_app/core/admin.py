from django.contrib import admin

from .models import Quiz, User, Question, QuestionOption


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "created_at")


class QuizAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "state", "created_at")


class QuestionOptionAdminInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "description", "correct_answer_points")
    inlines = (QuestionOptionAdminInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
