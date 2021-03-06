# Generated by Django 2.2.16 on 2020-10-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0004_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=128)),
                ('text', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
