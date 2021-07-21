# Generated by Django 3.2.5 on 2021-07-15 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=400)),
                ('url', models.URLField(unique=True, verbose_name='url')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='ShortDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='short', to='articles.article')),
                ('author', models.ForeignKey(auto_created=True, on_delete=django.db.models.deletion.PROTECT, related_name='short', to=settings.AUTH_USER_MODEL)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='sharticle_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='sharticle_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Краткое содержание',
                'verbose_name_plural': 'Краткие содержания',
            },
        ),
    ]
