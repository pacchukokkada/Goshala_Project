# Generated by Django 3.2.6 on 2021-08-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cow', '0008_alter_breeding_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breeding',
            name='result',
            field=models.CharField(blank=True, choices=[('Successful', 'Successful'), ('Unsuccessful', 'Unsuccessful')], max_length=15, null=True),
        ),
    ]