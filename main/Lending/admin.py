from django.contrib import admin
from django.utils.html import format_html

from .models import Settings,UploadInfo, Quiz, EndFrame, \
                    LendingPage, Icons, ImageForExampleOfWork, \
                    ImagesQuiz


@admin.register(ImageForExampleOfWork)
class ImageForExampleOfWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_link')

    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="#" onclick="navigator.clipboard.writeText(\'{}\'); alert(\'Ссылка скопирована!\'); return false;">📋 Скопировать ссылку</a>',
                obj.file.url
            )
        return "-"
    file_link.short_description = "Скопировать ссылку"


@admin.register(Icons)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title','file') 
    search_fields = ('title',) 

@admin.register(LendingPage)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('domain','title', 'number') 
    search_fields = ('domain',)  
    filter_horizontal = ('icons',)
    
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title',) 
    search_fields = ('title',)  
    
@admin.register(EndFrame)
class EndFrameAdmin(admin.ModelAdmin):
    list_display = ('title','text_phone','text_telegram', 'text_whatsapp','text_button') 
    search_fields = ('title',)  

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'excelTable', 'id_app', 'id_title', 'id_subtitle', 'min_rows', 'max_rows')

    def has_add_permission(self, request):
        if Settings.objects.exists():
            return False  
        return True 
@admin.register(ImagesQuiz)
class ImageQuizAdmin(ImagesQuiz):
    list_display = ('title',) 
    search_fields = ('title',)  

admin.site.register(UploadInfo)