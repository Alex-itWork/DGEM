# Generated by Django 5.1 on 2024-09-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_miniapp', '0011_user_points_per_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='points_per_hour',
            field=models.PositiveIntegerField(default=100),
        ),
    ]