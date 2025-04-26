from .models import Comment, Question
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' }),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']