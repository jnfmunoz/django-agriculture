# Generated by Django 5.1.6 on 2025-02-16 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='occupation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
