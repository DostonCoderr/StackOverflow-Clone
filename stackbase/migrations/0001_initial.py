# Generated by Django 5.2 on 2025-04-21 12:44

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000)),
                ('content', django_ckeditor_5.fields.CKEditor5Field()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('tags', models.CharField(blank=True, max_length=200)),
                ('likes', models.ManyToManyField(related_name='question_post', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('content', django_ckeditor_5.fields.CKEditor5Field()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='stackbase.question')),
            ],
        ),
    ]
