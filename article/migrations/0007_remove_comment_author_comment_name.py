# Generated by Django 5.1 on 2024-08-31 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_article_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default='Dems', max_length=100),
            preserve_default=False,
        ),
    ]
