# Generated by Django 2.2.16 on 2020-12-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20201202_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatar',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
