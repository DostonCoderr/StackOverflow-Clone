from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field  # `RichTextField` o‘rniga `CKEditor5Field` ishlatamiz

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    content = CKEditor5Field(config_name='default')  # `RichTextField` o‘rniga `CKEditor5Field`
    likes = models.ManyToManyField(User, related_name='question_post')
    date_created = models.DateTimeField(default=timezone.now)   
    tags = models.CharField(max_length=200, blank=True)  # `blank=True` qo‘shdim, agar teglar bo‘lmasa bo‘sh qolishi uchun

    def __str__(self):
        return f'{self.user.username} - Question'
    
    def get_absolute_url(self):
        return reverse('stackbase:question-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    question = models.ForeignKey(Question, related_name="comment", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    content = CKEditor5Field(config_name='default')  # `RichTextField` o‘rniga `CKEditor5Field`
    date_created = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return '%s - %s' % (self.question.title, self.question.user)

    def get_absolute_url(self):  # `get_success_url` o‘rniga `get_absolute_url` ishlatamiz
        return reverse('stackbase:question-detail', kwargs={'pk': self.question.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)