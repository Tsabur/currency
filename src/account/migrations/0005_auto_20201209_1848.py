# Generated by Django 2.2.16 on 2020-12-09 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_avatar_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('full_edit', 'This permissions allows user to update all available fields in User model')]},
        ),
    ]