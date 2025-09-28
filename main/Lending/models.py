from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import openpyxl
import os
import uuid


def get_unique_filename(instance, filename, upload_dir):

    ext = filename.split('.')[-1].lower() 

    for _ in range(10): 
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        full_path = os.path.join(upload_dir, unique_name)

        if hasattr(instance, 'file'):
            media_root = os.path.dirname(instance.file.storage.path(''))  # определяем MEDIA_ROOT из storage
        else:
            media_root = ''

        absolute_path = os.path.join(media_root, full_path)

        if not os.path.exists(absolute_path):
            return full_path

def random_quiz_filename(instance, filename):
    return get_unique_filename(instance, filename, 'lending/data/quizPhotos')

def random_icon_filename(instance, filename):
    return get_unique_filename(instance, filename, 'lending/data/icons')

def random_example_filename(instance, filename):
    return get_unique_filename(instance, filename, 'lending/data/examplesOfWork')

class UtmExampleWork(models.Model):
    examplesOfWork = models.JSONField(
        verbose_name = "Примеры работ"
    )
    utm_content = models.JSONField(
        verbose_name="UTM контент метка",
        default=list
    )
    class Meta:
        verbose_name = "UTM примеры работы"
        verbose_name_plural = "UTM примеры работ"


    def __str__(self):
        return f"Пример работ #{self.id}"
    
class Settings(models.Model):
    excelTable = models.FileField(
        upload_to="lending/settings/",
        verbose_name="Эксель таблица"
    )

    id_app = models.IntegerField(
        verbose_name = "Номер колонки excel с app_id",
        default = 2
    )

    id_title = models.IntegerField(
        verbose_name = "Номер колонки excel с заголовками",
        default=  3
    )

    id_subtitle = models.IntegerField(
        verbose_name = "Номер колонки excel с под заголовками",
        default = 4
    )

    min_rows =  models.IntegerField(
        verbose_name = "Номер строки с, которой начинается порядок"
    )

    max_rows =  models.IntegerField(
        verbose_name = "Номер конечной строки"
    )

    botTelegramToken = models.CharField(
        max_length  = 255,
        verbose_name = "Api token telegram bot"
    )
    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    def save(self, *args, **kwargs):
        workbook = openpyxl.load_workbook(self.excelTable, data_only=True)
        sheet = workbook.active  
        objects_create = []
        UploadInfo.objects.all().delete()

        for i, row in enumerate(sheet.iter_rows(min_row=self.min_rows, max_row=self.max_rows), start=self.min_rows):
            try:
                app = row[self.id_app - 1].value if self.id_app <= len(row) else None
                title = row[self.id_title - 1].value if self.id_title <= len(row) else None
                subtitle = row[self.id_subtitle - 1].value if self.id_subtitle <= len(row) else None
                if app.isdigit() and title != None and subtitle != None:
                    objects_create.append(
                        UploadInfo(
                            app = int(app),
                            title = title,
                            subtitle = subtitle
                        )
                    )   
            except:
                pass

        if len(objects_create) > 0 :
            UploadInfo.objects.bulk_create(
                    objects_create
                )

        super().save(*args, **kwargs)

    def __str__(self):
        return "Настройки"

class ImagesQuiz(models.Model):
    file = models.FileField(
        upload_to=random_quiz_filename,
        verbose_name="Файл квиза"
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название файла"
    )

    utm_content = models.JSONField(
        verbose_name="UTM контент метка",
        default=list
    )

    def save(self, *args, **kwargs):
        if not self.title and self.file:
            try:
                original_name = self.file.file.name  #
            except Exception:
                original_name = self.file.name 

            self.title = os.path.basename(original_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.file.url

    class Meta:
        verbose_name = "Изображение квиза"
        verbose_name_plural = "Изображения квизов"
        
class UploadInfo(models.Model):
    app = models.IntegerField()

    title = models.CharField(
        max_length = 255
    )

    subtitle = models.CharField(
        max_length = 255
    )

    class Meta:
        verbose_name = "Информация Excel"
        verbose_name_plural = "Информация Excel"

    def __str__(self):
        return f"{self.title} : {self.subtitle}"

class Quiz(models.Model):
    title = models.CharField(max_length=255)  
    endFrame = models.ForeignKey(
        'EndFrame', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='endFrame'
    )

    questionJson = models.JSONField(
        verbose_name = "Вопросы"
    )

    utm_content = models.JSONField(
        verbose_name = "UTM контент метка",
        blank = True,
        null = True,
        default=list
    )
    
    class Meta:
        verbose_name = "Квизы"
        verbose_name_plural = "Квиз"
        
    def __str__(self):
        return self.title
    
class EndFrame(models.Model):
    title = models.CharField(max_length=255) 
    text_phone = models.CharField(max_length=255)
    text_telegram = models.CharField(max_length=255)
    text_whatsapp = models.CharField(max_length=255)
    text_button = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Конечные frame квизов"
        verbose_name_plural = "Конечный frame квиза"
    
    
    def __str__(self):
        return self.title

class Icons(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название логотипа"
    )

    file = models.FileField(
        upload_to=random_icon_filename,
        verbose_name="Файл иконки"
    )

    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"

    def __str__(self):
        return self.title

class ImageForExampleOfWork(models.Model):
    file = models.FileField(
        upload_to=random_example_filename,
        verbose_name="Файл примера работ"
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название файла"
    )

    def save(self, *args, **kwargs):
        if not self.title and self.file:
            try:
                original_name = self.file.file.name  #
            except Exception:
                original_name = self.file.name 

            self.title = os.path.basename(original_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.file.url

    class Meta:
        verbose_name = "Изображение примера работы"
        verbose_name_plural = "Изображения примеров работ"

class LendingPage(models.Model):
    
    domain = models.CharField(
        max_length=255,
        verbose_name="Доменное имя, вместе с под доменном."
    )

    title = models.CharField(
        max_length = 255,
        verbose_name = "Название"
    )
    
    title_meta = models.CharField(
        max_length = 255,
        verbose_name = "Мета название сайта ( нельзя использовать html теги )"
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Описание"
    )

    description_meta = models.CharField(
        max_length = 255,
        verbose_name = "Мета описание сайта ( нельзя использовать html теги )"
    )

    logo = models.FileField(
        upload_to = 'lending/data/logo/',
        verbose_name = "Логитип"
    )
    
    number = models.CharField(
        max_length = 255,
        verbose_name = "Номер телефона"
    )
    
    title_slider = models.CharField(
        max_length = 255,
        verbose_name="Название блока с слайдом"
    )
    
    preview_slider = models.FileField(
        upload_to = "lending/data/slider/",
        verbose_name = "Картинка слайда"
    )
    
    icons = models.ManyToManyField(
        'Icons',
        related_name='LendingPage',
        verbose_name="Иконки"
    ) 

    blackout = models.FloatField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(1)
        ],
        verbose_name= "затемнение"
        
    )

    title_swaper = models.CharField(
        max_length=255,
        verbose_name="Название блока  с примерами работ"
    )
    
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='Quiz')

    number_whatsap = models.CharField(
        max_length=255,
        verbose_name="Номер whatsapp"
    )

    username_telegram = models.CharField(
        max_length=255,
        verbose_name="Username телеграмм"
    )
    
    chatid = models.IntegerField(
        verbose_name = "Chat id телеграмм канала"
    )

    head = models.TextField(
        verbose_name = "Head сайта, для метрики",
        null = True,
        blank = True,
    )
    
    examplesOfWork = models.JSONField(
        verbose_name = "Примеры работ"
    )

    target_feedback = models.TextField(
        verbose_name = "Цель для формы обратной связи",
        max_length = 255,
        blank =  True,
        null = True,
    )

    target_quiz = models.TextField(
        verbose_name = "Цель для формы квиза",
        max_length = 255,
        blank =  True,
        null = True,
    )

    target_quiz_set = models.TextField(
        verbose_name = "Цель для формы квиза в процессе",
        max_length = 255,
        blank =  True,
        null = True,
    )

    imageCheckBox = models.FileField(
        upload_to = 'lending/data/images/',
        verbose_name = "Изображение чек бокс"
    )
    
    imageCheckBoxPolit = models.FileField(
        upload_to = 'lending/data/images/',
        verbose_name = "Изображение чек бокс политики"
    )
    
    imageArrow = models.FileField(
        upload_to = 'lending/data/images/',
        verbose_name = "Изображение стрелка"
    )

    accentColor = models.CharField(
        max_length = 255,
        verbose_name = "Основной цвет"
    )
    
    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


    def __str__(self):
        return self.domain