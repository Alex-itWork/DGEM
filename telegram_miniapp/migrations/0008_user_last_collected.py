# Generated by Django 5.1 on 2024-08-30 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_miniapp', '0007_character_last_progress_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_collected',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
