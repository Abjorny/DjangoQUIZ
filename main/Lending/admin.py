from django.contrib import admin
from .models import Quiz, Question, Option

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at') 
    search_fields = ('title', 'description')  
    list_filter = ('created_at',)  

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type') 
    search_fields = ('text',)  
    list_filter = ('quiz', 'question_type')  

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')  
    search_fields = ('text',)  
    list_filter = ('question__quiz',)  
