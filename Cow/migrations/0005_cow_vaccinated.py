# Generated by Django 3.2.6 on 2021-08-17 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cow', '0004_alter_cow_age_when_brought'),
    ]

    operations = [
        migrations.AddField(
            model_name='cow',
            name='vaccinated',
            field=models.BooleanField(default=False),
        ),
    ]
