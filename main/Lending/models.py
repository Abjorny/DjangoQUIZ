from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=255)  # Заголовок квиза
    description = models.TextField(blank=True, null=True)  # Описание квиза
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('radio', 'Radio Button'),  # Радио-кнопки (Один из множества)
        ('dropdown', 'Dropdown'),    # Выпадающий список
        ('text', 'Text Input'),     # Ввод текста
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions') 
    text = models.TextField() 
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)  

    def __str__(self):
        return self.text

    def add_option(self, option_text):
        if self.question_type == 'radio' or self.question_type == 'dropdown':
            Option.objects.create(question=self, text=option_text)

    def remove_option(self, option_id):
        if self.question_type == 'radio' or self.question_type == 'dropdown':
            option = Option.objects.filter(id=option_id, question=self).first()
            if option:
                option.delete()

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options') 
    text = models.CharField(max_length=255)  

    def __str__(self):
        return self.text
