# Generated by Django 3.2.6 on 2021-08-17 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cow', '0003_alter_cow_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cow',
            name='age_when_brought',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
